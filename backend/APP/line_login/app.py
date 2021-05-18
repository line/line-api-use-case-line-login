import os
import json
import logging

from common import (utils, line)
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from line_login.sent_user_info import SentUserInfo


# ログ出力の設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 環境変数の宣言
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LIFF_CHANNEL_ID = os.getenv('LIFF_CHANNEL_ID', None)

# 定数の宣言
MESSAGES_LOGGED_IN = {
    'ja':  'LINEログインが完了しました。'
}


# テーブル操作クラスの初期化
sent_user_info_controller = SentUserInfo()


def lambda_handler(event, context):
    """
    LINEログイン時、DynamoDBにUserIdが存在しない場合LINE Messageを送信する
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format
    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict
    """
    logger.debug('##START lambda_handler')
    logger.info('event: %s', event)

    req_param = json.loads(event['body'])
    # ユーザーID取得
    try:
        user_profile = line.get_profile(req_param['idToken'], LIFF_CHANNEL_ID)
        if 'error' in user_profile and 'expired' in user_profile['error_description']:  # noqa 501
            return utils.create_error_response('Forbidden', 403)
        else:
            req_param['userId'] = user_profile['sub']
    except Exception:
        logger.exception('不正なIDトークンが使用されています')
        return utils.create_error_response('Error')

    # DynamoDBデータ存在チェック
    user_id = req_param['userId']
    if not sent_user_info_controller.get_item(user_id):
        # DynamoDB登録
        try:
            sent_user_info_controller.put_item(user_id)
        except Exception:
            logger.error('DynamoDBデータ登録失敗 userId:{}'.format(user_id))

        # message送信(多言語対応用)
        locale = req_param.get('locale')
        if locale:
            send_push_message(user_id, MESSAGES_LOGGED_IN.get(locale))
        else:
            send_push_message(user_id, MESSAGES_LOGGED_IN.get('ja'))

    return utils.create_success_response('success')


def send_push_message(user_id, message):
    """
    MessagingAPIのpushメッセージを送信する
    Parameters
    ----------
    user_id :string
        送信先のuser id
    message :string
        送信するメッセージテキスト
    """
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    try:
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
    except LineBotApiError:
        logger.error('LINEメッセージ送信失敗 userId:{}'.format(user_id))
