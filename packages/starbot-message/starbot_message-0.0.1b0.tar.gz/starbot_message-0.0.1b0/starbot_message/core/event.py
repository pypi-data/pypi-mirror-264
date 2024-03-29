class EventType:
    """
    事件类型枚举，基于本项目开发时，可通过继承此类的方式扩展事件类型
    """
    SendMessageEvent = "SendMessageEvent"
    """发送消息事件"""

    ReceiveMessageEvent = "ReceiveMessageEvent"
    """接收消息事件"""
