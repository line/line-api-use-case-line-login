"""
SentUserInfo操作用モジュール

"""
import os
from datetime import datetime
from dateutil.tz import gettz

from aws.dynamodb.base import DynamoDB
from common import utils


class SentUserInfo(DynamoDB):
    """SentUserInfo操作用クラス"""
    __slots__ = ['_table']

    def __init__(self):
        """初期化メソッド"""
        table_name = os.environ.get("LOGIN_USERS_INFO_DB_NAME")
        super().__init__(table_name)
        self._table = self._db.Table(table_name)

    def get_item(self, user_id):
        """
        データ取得

        Parameters
        ----------
        user_id : str
            LINEユーザーID

        Returns
        -------
        item : dict
            ユーザー情報

        """
        key = {'userId': user_id}

        try:
            item = self._get_item(key)
        except Exception as e:
            raise e
        return item

    def put_item(self, user_id):
        """
        データ登録

        Parameters
        ----------
        user_id : str
            LINEユーザーID

        Returns
        -------
        response : dict
            レスポンス情報

        """
        now = datetime.now()
        item = {
            'userId': user_id,
            "expirationDate": utils.get_ttl_time(now),
            'createdTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S")
        }

        try:
            response = self._put_item(item)
        except Exception as e:
            raise e
        return response
