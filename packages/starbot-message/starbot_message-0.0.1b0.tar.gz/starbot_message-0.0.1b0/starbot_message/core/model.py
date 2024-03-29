import abc
import base64
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Any, Optional, List, Type, NoReturn

import aiohttp


class Element:
    """
    消息中的子元素，仅作为父类使用
    """

    def __init__(self):
        raise NotImplementedError("Element 类不可直接实例化")


@dataclass
class Plain(Element):
    """
    消息中的文本元素
    """

    content: str
    """消息文本"""

    def __str__(self):
        return self.content


@dataclass
class At(Element):
    """
    消息中的 @ 元素
    """

    target: Union[int, str]
    """@ 目标"""

    def __str__(self):
        return f"@{self.target} "


@dataclass
class AtAll(Element):
    """
    消息中的 @全体成员 元素
    """

    def __str__(self):
        return "@全体成员 "


@dataclass
class Image(Element):
    """
    消息中的图片元素
    """

    byte: Optional[bytes] = None
    """图片原始数据"""

    path: Optional[Union[Path, str]] = None
    """图片本地路径，与其他两个参数三选一传入"""

    url: Optional[str] = None
    """图片 URL 地址，与其他两个参数三选一传入"""

    base64str: Optional[str] = None
    """图片 Base64 字符串，与其他两个参数三选一传入"""

    def __str__(self):
        return "[图片]"

    async def get_bytes(self) -> bytes:
        """
        获取图片内容

        Returns:
            图片原始字节数据
        """
        if self.byte:
            return self.byte

        if self.path:
            path = Path(self.path)
            if not path.exists():
                raise FileNotFoundError(f"图片文件 {path} 不存在")
            self.byte = path.read_bytes()
        elif self.url:
            async with aiohttp.request("GET", self.url) as response:
                response.raise_for_status()
                self.byte = await response.read()
        elif self.base64str:
            self.byte = base64.b64decode(self.base64str)
        else:
            raise ValueError("图片数据为空")

        return self.byte


@dataclass
class Quote:
    """
    引用或回复的消息
    """

    message_id: Union[int, str]
    """源消息 ID"""

    source: Optional["MessageReceive"] = None
    """源消息"""


class MessageSend:
    """
    从 StarBot 发送的消息类
    """

    platform: str
    """发送目标平台"""

    account: Union[int, str]
    """发送机器人账号"""

    target: Union[int, str]
    """发送目标账号/群号"""

    content: List[Element]
    """消息元素列表"""

    quote: Optional[Quote]
    """引用或回复的消息"""

    timestamp: int
    """消息创建时间戳，原始消息被创建时自动填入"""

    def __init__(self, platform: str, account: Union[int, str], target: Union[int, str],
                 content: List[Element], quote: Optional[Quote] = None):
        self.platform = platform
        self.account = account
        self.target = target
        self.content = content
        self.quote = quote
        self.timestamp = int(time.time())

    def __str__(self):
        return f"[{self.platform}]({self.account}) -> {self.target}: {self.display()}"

    def display(self) -> str:
        """
        将消息内容转换为可读字符串

        Returns:
            近似为消息日常所见的字符串表示形式
        """
        return "".join(map(lambda element: str(element), self.content))

    def remove(self, *types: Type[Element]) -> NoReturn:
        """
        从消息元素列表中移除指定类型的元素

        Args:
            *types: 要移除的消息元素类型
        """
        self.content = [element for element in self.content if type(element) not in types]

    @classmethod
    def create(cls, platform: str, account: Union[int, str], target: Union[int, str],
               content: str, quote: Optional[Quote] = None) -> List["MessageSend"]:
        """
        从包含 {next}、{atall} 等占位符的原始消息内容创建发送消息实例，自动进行占位符转换

        Args:
            platform: 发送目标平台
            account: 发送账号
            target: 发送目标账号/群号
            content: 可包含 {next}、{atall} 等占位符的原始消息内容
            quote: 需引用或回复的消息

        Returns:
            发送消息实例列表，返回结果列表长度 = 原始消息内容中 {next} 占位符的个数 + 1
        """
        messages = []

        for part in content.split("{next}"):
            messages.append(MessageSend(platform, account, target, cls.__convert(part), quote))

        return messages

    @classmethod
    def __convert(cls, content: str) -> List[Element]:
        """
        处理占位符至消息元素列表的转换

        Args:
            content: 可包含 {atall} 等占位符的原始消息内容，不再处理 {next} 占位符，请在调用前自行分割

        Returns:
            消息元素列表
        """
        elements = []

        code_start = content.find("{")
        while content != "":
            if code_start == -1:
                elements.append(Plain(content))
                content = ""
            elif code_start != 0:
                elements.append(Plain(content[:code_start]))
                content = content[code_start:]
                code_start = content.find("{")
            else:
                code_end = content.find("}")
                if code_end == -1:
                    elements.append(Plain(content))
                    content = ""
                else:
                    if content[1:6] == "atall":
                        elements.append(AtAll())
                    elif content[1:3] == "at":
                        at_target = content[4:code_end]
                        if at_target.isdigit():
                            elements.append((At(int(at_target))))
                            elements.append(Plain(" "))
                        else:
                            elements.append((At(at_target)))
                            elements.append(Plain(" "))
                    elif content[1:7] == "urlpic":
                        pic_url = content[8:code_end]
                        if pic_url != "":
                            elements.append(Image(url=pic_url))
                    elif content[1:8] == "pathpic":
                        pic_path = content[9:code_end]
                        if pic_path != "":
                            elements.append(Image(path=pic_path))
                    elif content[1:10] == "base64pic":
                        pic_base64 = content[11:code_end]
                        if pic_base64 != "":
                            elements.append(Image(base64str=pic_base64))
                    else:
                        elements.append(Plain(content[:code_end + 1]))
                    content = content[code_end + 1:]
                    code_start = content.find("{")

        return elements


class MessageReceive:
    """
    从各平台接收到的消息类
    """

    platform: str
    """消息来源平台"""

    account: Union[int, str]
    """消息来源机器人账号"""

    source: Union[int, str]
    """消息来源群号/账号"""

    sender: Union[int, str]
    """消息发送者账号"""

    content: List[Element]
    """消息元素列表"""

    quote: Optional[Quote]
    """引用或回复的消息"""

    message_id: Optional[Union[int, str]]
    """消息 ID，可用于触发命令时引用或回复触发命令的消息"""

    meta: Any
    """消息元数据，仅在为特定平台编写命令时使用，命令处理方法中依赖此字段会导致命令失去全平台适用性"""

    timestamp: int
    """消息创建时间戳，原始消息被创建时自动填入"""

    def __init__(self, platform: str, account: Union[int, str], source: Union[int, str],
                 sender: Union[int, str], content: List[Element], meta: Any,
                 quote: Optional[Quote] = None, message_id: Optional[Union[int, str]] = None):
        """
        各平台接收到消息时，请将各平台的消息实例转换为本消息实例，并触发接收消息事件，交由命令处理器处理命令

        Args:
            platform: 消息来源平台
            account: 消息来源机器人账号
            source: 消息来源群号/账号
            sender: 消息发送者账号
            content: 消息元素列表
            meta: 消息元数据
            quote: 引用或回复的消息
            message_id: 消息 ID
        """
        self.platform = platform
        self.account = account
        self.source = source
        self.sender = sender
        self.content = content
        self.meta = meta
        self.quote = quote
        self.message_id = message_id
        self.timestamp = int(time.time())

    def __str__(self):
        return f"[{self.platform}]({self.account}) <- [{self.source}]({self.sender}): {self.display()}"

    def display(self) -> str:
        """
        将消息内容转换为可读字符串

        Returns:
            近似为消息日常所见的字符串表示形式
        """
        return "".join(map(lambda element: str(element), self.content))


class Command(metaclass=abc.ABCMeta):
    """
    命令类
    """
    platform: Optional[str]
    """命令适用平台，None 代表全平台适用"""

    name: str
    """命令名称"""

    help: str
    """帮助文档"""

    author: str
    """命令作者，建议格式: Github用户名/Github仓库名"""

    @abc.abstractmethod
    async def trigger(self, message: MessageReceive) -> bool:
        """
        收到消息触发接收消息事件后，自动调用此方法，根据传入消息内容判断是否需要触发命令，返回 True 会触发 handler 方法

        Args:
            message: 接收消息实例

        Returns:
            是否需要触发命令
        """
        pass

    @abc.abstractmethod
    async def handler(self, message: MessageReceive) -> Optional[MessageSend]:
        """
        命令处理方法

        Args:
            message: 接收消息实例

        Returns:
            触发命令后需回复的消息，返回 None 不回复消息
        """
        pass
