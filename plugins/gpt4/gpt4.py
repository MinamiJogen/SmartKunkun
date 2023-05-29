# encoding:utf-8

from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
import plugins
from plugins import *
from common.log import logger


@plugins.register(name="gpt4", desc="The plugin that use module gpt-4 to reply", version="0.1", author="Minami", desire_priority= 200)
class gpt4(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[gpt4] inited")

    def on_handle_context(self, e_context: EventContext):

        if e_context['context'].type != ContextType.TEXT:
            return
        
        prefix=["GPT-4", "gpt-4","GPT4","gpt4"]
        content = e_context['context'].content

        # 使用 split() 方法进行分割
        split_strings = content.split(" ", 1)

        # 获取分割后的两个子字符串
        content1 = split_strings[0]
        content2 = split_strings[1]

        logger.debug("[gpt4] on_handle_context. content: %s" % content)
        if content1 in prefix:
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply1 = Reply()
            reply1.type = ReplyType.TEXT
            if e_context['context']['isgroup']:
                reply1.content = "GPT-4模型暂不支持于群聊内使用。GPT-4 model currently does not support being called within a group chat."
            else:
                reply1.content = "正在通过GPT-4生成回复，请耐心等待。Generating response through GPT-4, please wait patiently."
            e_context['reply'] = reply
            e_context.action = EventAction.BREAK

    def get_help_text(self, **kwargs):
        help_text = "输入GPT-4/gpt-4/GPT4/gpt4以调用GPT-4模型回答问题。"
        return help_text
