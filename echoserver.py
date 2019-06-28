# coding=utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import random
app = Flask(__name__)

line_bot_api = LineBotApi('your token')
handler = WebhookHandler('your handler')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'




@handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

def handle_message(event):
    if event.message.text == "沒事啦":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="OK"))
        return 0
    if event.message.text == "回傳數值":
        data = random.randint(0,100)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=data))
        return 0
    if event.message.text == "控制指令":
        buttons_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ButtonsTemplate(
                title='安安',
                text='我是志偉',
                thumbnail_image_url='https://imgur.com/WuCndWo.jpg',
                actions=[
                    MessageTemplateAction(
                        label='抽水馬達',
                        text='抽水馬達'
                    ),
                    MessageTemplateAction(
                        label='循環馬達',
                        text='循環馬達'
                    ),
                    MessageTemplateAction(
                        label='LED燈',
                        text='LED燈'
                    ),

                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    buttons_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ButtonsTemplate(
            title='安安',
            text='我是志偉',
            thumbnail_image_url='https://imgur.com/WuCndWo.jpg',
            actions=[
                MessageTemplateAction(
                    label='回傳數值',
                    text='回傳數值'
                ),
                URITemplateAction(
                    label='定估隻',
                    uri='https://www.youtube.com/watch?v=UftRC4HoSbA'
                ),
                URITemplateAction(
                    label='github',
                    uri='https://github.com/zhu913104'
                ),
                URITemplateAction(
                    label='聯絡作者',
                    uri='https://www.facebook.com/chan.c.wei.9'
                ),

            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template)

if __name__ == "__main__":
    app.run()