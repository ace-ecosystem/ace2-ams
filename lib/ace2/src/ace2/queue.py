from boto3 import client
import json
from typing import Optional
import os

def add(queue:str, message:dict, delay:Optional[int]=0):
    ''' adds message to specified queue with optional delay

    Args:
        queue: the url of the queue
        message: the message to add to the queue
        delay: number of seconds to delay the message for
    '''

    # add the message to the queue
    client('sqs').send_message(
        QueueUrl = f'{os.environ["QUEUE_BASE_URL"]}/{queue}',
        MessageBody = json.dumps(message),
        DelaySeconds = delay,
    )

def remove(queue:str, receipt_handle:str):
    ''' removes message with given receipt handle from the queue

    Args:
        queue: the url of the queue
        receipt_handle: the receipt handle for the message to remove
    '''

    # add the message to the queue
    client('sqs').delete_message(
        QueueUrl = f'{os.environ["QUEUE_BASE_URL"]}/{queue}',
        ReceiptHandle = receipt_handle,
    )

def get(queue:str):
    ''' returns the next message on the queue

    Args:
        queue: the url of the queue
    '''

    # add the message to the queue
    messages = client('sqs').receive_message(
        QueueUrl = f'{os.environ["QUEUE_BASE_URL"]}/{queue}',
        VisibilityTimeout = 15 * 60, # 15 minutes
    )
    return messages[0] if messages else None
