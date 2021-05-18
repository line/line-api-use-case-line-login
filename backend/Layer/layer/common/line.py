import logging
import json
import requests
import json
from linebot import LineBotApi
from linebot.models import FlexSendMessage
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError)
from requests.models import Response

from common import common_const

# ログ出力の設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_notification_token(channel_access_token, access_token):
    """
    サービスメッセージ用のサービス通知トークンを取得する
    Parameters
    channel_access_token:str
        短期チャネルアクセストークン
    access_token:str
        フロントで取得したアクセストークン
    Returns
    -------
    notification_token:str
        サービス通知トークン
    """
    # 通知アクセストークンを発行する
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token
    }
    response = requests.post(
        common_const.const.API_NOTIFICATIONTOKEN_URL,
        headers=headers,
        data=access_token
    )
    logger.debug('notification_response %s', response.text)
    res_body = json.loads(response.text)
    notification_token = res_body['notificationToken']
    return notification_token


def send_push_message(channel_access_token, flex_obj, user_id):
    """
    プッシュメッセージ送信処理
    Parameters
    channel_access_token:str
        短期チャネルアクセストークン
    flex_obj:dict
        メッセージ情報
    user_id:str
        送信先のユーザーI
    Returns
    -------
    response:dict
        レスポンス情報
    """
    try:
        line_bot_api = LineBotApi(
            channel_access_token)
        # flexdictを生成する
        flex_obj = FlexSendMessage.new_from_json_dict(flex_obj)
        user_id = user_id
        response = line_bot_api.push_message(user_id, flex_obj)
    except LineBotApiError as e:
        logger.error(
            'Got exception from LINE Messaging API: %s\n' % e.message)
        for m in e.error.details:
            logger.error('  %s: %s' % (m.property, m.message))
        raise Exception
    except InvalidSignatureError as e:
        logger.error('Occur Exception: %s', e)
        raise Exception

    return response


def send_service_message(channel_access_token, template_name , params, notification_token):
    """
    サービスメッセージ送信処理

    Parameters
    ----------
    channel_access_token:str
        短期チャネルアクセストークン
    template_name:str
        テンプレート名
    params:dict
        メッセージ情報
    notification_token:str
        サービス通知トークン
    Returns
    -------
    response:dict
        レスポンス情報
    """

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + channel_access_token
    }
    data = {
        'templateName': template_name,
        'params': params,
        'notificationToken': notification_token
    }

    response = requests.post(
        common_const.const.API_SENDSERVICEMESSAGE_URL,
        headers=headers,
        data=json.dumps(data)
    )

    return response


def get_profile(id_token, channel_id):
    """
    プッシュメッセージ送信処理

    Parameters
    ----------
    id_token:str
        IDトークン
    channel_id:dict
        使用アプリのLIFFチャネルID
    Returns
    -------
    res_body:dict
        レスポンス情報
    """

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {
        'id_token': id_token,
        'client_id': channel_id
    }

    response = requests.post(
        common_const.const.API_USER_ID_URL,
        headers=headers,
        data=body
    )

    res_body = json.loads(response.text)
    return res_body