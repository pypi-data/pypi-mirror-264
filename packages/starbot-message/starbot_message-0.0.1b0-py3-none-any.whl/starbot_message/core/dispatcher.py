from typing import List, Union, Dict, NoReturn

from loguru import logger
from starbot_executor import executor


from .event import EventType
from .. import MessageHandler, Command, MessageSend, MessageReceive


class MessageDispatcher:
    """
    消息调度器
    """

    handlers: List[MessageHandler]
    """已注册的消息处理器"""

    commands: List[Command]
    """已注册的命令"""

    handlers_mapping: Dict[str, MessageHandler]
    """消息处理器映射表"""

    def __init__(self):
        self.handlers = []
        self.commands = []
        self.handlers_mapping = {}

        @executor.on(EventType.SendMessageEvent)
        async def send(message: MessageSend):
            key = f"{message.platform}-{message.account}"
            if key not in self.handlers_mapping:
                logger.warning(f"无法向未注册的消息处理器推送消息: [{message.platform}]({message.account})")
                return

            handler = self.handlers_mapping[key]
            try:
                success, reason = await handler.send(message)
                if success:
                    logger.info(message)
                else:
                    logger.warning(f"平台 [{message.platform}]({message.account}) 消息推送失败, 原因: {reason}")
            except Exception as e:
                logger.exception(
                    f"平台 [{message.platform}]({message.account}) 消息推送异常, 消息元数据: {message.content}", e
                )

        @executor.on(EventType.ReceiveMessageEvent)
        async def receive(message: MessageReceive):
            for command in self.commands:
                if command.platform is None or command.platform == message.platform:
                    if await command.trigger(message):
                        logger.info(
                            f"平台 [{message.platform}]({message.account}) 触发命令: {command.name}, "
                            f"来源: {message.source}, 触发者: {message.sender}"
                        )
                        reply = await command.handler(message)
                        if reply:
                            executor.dispatch(reply, EventType.SendMessageEvent)

    def register(self, *instances: Union[MessageHandler, Command]) -> NoReturn:
        """
        将消息处理器或命令注册至消息调度器

        Args:
            instances: 消息处理器或命令实例
        """
        for instance in instances:
            if isinstance(instance, MessageHandler):
                key = f"{instance.platform}-{instance.account}"
                if key in self.handlers_mapping:
                    raise ValueError(f"已存在平台为 {instance.platform} 且账号为 {instance.account} 的消息处理器, 不可重复注册")
                self.handlers.append(instance)
                self.handlers_mapping[key] = instance
                logger.success(f"消息处理器 [{instance.platform}]({instance.account}) 注册成功")
            elif isinstance(instance, Command):
                self.commands.append(instance)
                platform = "全平台" if instance.platform is None else instance.platform
                logger.success(f"命令 [{platform}]{instance.name} 注册成功")
            else:
                logger.warning(f"要注册的实例 {instance} 不为消息处理器或命令类型")


dispatcher: MessageDispatcher = MessageDispatcher()
