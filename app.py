import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    if(get_message=="組別"):
        reply_text = "第五組"
    elif(get_message=="組員"):
        reply_text = "黃啟洲 M10913017\n黃瀚緯 B10613005\n鐘竣耀 M10913021\n李永漢 M10913047"
    elif(get_message=="課程名稱"):
        reply_text = "人工智慧暨物聯網系統設計"
    else:
        reply_text = get_message
    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)
