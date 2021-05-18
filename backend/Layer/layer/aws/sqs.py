import logging
import uuid
import json

# ログ出力の設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_messages(sqs, sqs_dict):
    """
    SQSキューにメッセージを送信する

    Parameters
    ----------
    sqs : sqs
        SQSオブジェクト
    sqs_dict : dict
        送信するメッセージ群

    Returns
    -------
    なし
    """
    queue = create_queue(sqs, sqs_dict['queue_name'])
    msg = create_message(sqs_dict['sqs_body'],
                     sqs_dict['event_type'],
                     sqs_dict['delay_seconds'])
    sqs_response = queue.send_messages(Entries=msg)
    logger.debug('sqs_response: %s', sqs_response)


def create_queue(sqs, queue_name):
    """
    SQSキューを作成する

    Parameters
    ----------
    sqs : sqs
        SQSオブジェクト
    queue_name : str
        SQSキュー名

    Returns
    -------
    queue : sqs.queue
        SQSキューオブジェクト

    """
    try:
        # キューの名前を指定してインスタンスを取得
        queue = sqs.get_queue_by_name(QueueName=queue_name)
    except Exception:
        # 指定したキューがない場合はexceptionが返るので、キューを作成
        queue = sqs.create_queue(QueueName=queue_name)

    return queue


def create_message(sqs_body, event_type, delay_seconds):
    """
    sqs.send_messages用のパラメータを作成する

    Parameters
    ----------
    sqs_body : dict
        sqs_bodyオブジェクト
    event_type : str
        メッセージ属性
    delay_seconds : int
        メッセージ遅延時間

    Returns
    -------
    msg : dict
        send_messages用のパラメータ
    """
    msg = [{'Id': '{}'.format(uuid.uuid4()),
            'MessageBody': json.dumps(sqs_body),
            'MessageAttributes': {
                'EventType': {
                    'StringValue': event_type,
                    'DataType': 'String'}},
            'DelaySeconds': delay_seconds}]

    return msg
