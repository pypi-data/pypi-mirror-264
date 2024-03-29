import abc
from typing import Union, Tuple, Optional, List, NoReturn

from starbot_executor import executor

from .event import EventType
from .model import MessageSend, MessageReceive


class MessageHandler(metaclass=abc.ABCMeta):
    """
    消息处理器基类，较简单的消息处理器实现请直接继承本类，在构造方法中初始化，并实现消息发送与接收，示例：example/simple.py
    """
    platform: str
    """推送平台唯一标识符，请使用 平台名称/自定义名称(建议使用推送平台实现所在的代码仓库名) 的格式，并注意唯一性，例：QQ/StarBot"""

    account: Union[int, str]
    """机器人账号"""

    def __init__(self, platform: str, account: Union[int, str]):
        """
        请在子类中重写构造方法，在其中使用 super().__init__("平台名称/自定义名称", account) 进行父类构造
        """
        if platform is None or account is None:
            raise ValueError("消息处理器的推送平台标识符及账号不能为空")

        self.platform = platform
        self.account = account

    @abc.abstractmethod
    async def run(self) -> NoReturn:
        """
        在所有消息处理器注册完毕后，此方法会被依次自动调用，若不需要使用可保留为空实现
        """
        pass

    @abc.abstractmethod
    async def send(self, message: MessageSend) -> Tuple[bool, Optional[str]]:
        """
        发送消息，需实现 MessageSend 类型到平台消息类型的转换，并将消息发送至对应平台

        Args:
            message: 原始发送消息实例

        Returns:
            由 (是否发送成功, 发送失败原因) 组成的元组，当消息发送成功时忽略第二个返回值
        """
        pass

    @classmethod
    def received(cls, message: MessageReceive) -> NoReturn:
        """
        请自行实现消息接收方法，并在接收到消息后，将平台消息类型转换为 MessageReceive 类型后调用此方法，以触发命令

        Args:
            message: 接收消息实例
        """
        executor.dispatch(message, EventType.ReceiveMessageEvent)


class AbstractMessageHandlerFactory(metaclass=abc.ABCMeta):
    """
    消息处理器工厂，较复杂的消息处理器实现请继承本类，实现生产方法，可返回一个或多个 MessageHandler 实例，示例：example/complex.py
    """

    @abc.abstractmethod
    async def produce(self, account: Union[int, str]) -> Union[MessageHandler, List[MessageHandler]]:
        """
        用于创建复杂的 MessageHandler 实例
        例如为某平台的好友推送与群推送分别实现消息处理器，可在此初始化后，生成两个对应的 MessageHandler 实例，封装在列表中返回
        """
        pass
