from boto3 import client
from os import environ
from typing import Optional

def add(queue:str, message:str, delay:Optional[int]=0):
    ''' adds message to specified queue with optional delay

    Args:
        queue: the url of the queue
        message: the message to add to the queue
        delay: number of seconds to delay the message for
    '''

    # add the message to the queue
    client('sqs').send_message(
        QueueUrl = f'{environ["QUEUE_BASE_URL"]}/{queue}',
        MessageBody = message,
        DelaySeconds = delay,
    )

def remove(queue:str, receipt_handle:str):
    ''' removes message with given receipt handle from the queue

    Args:
        queue: the url of the queue
        receipt_handle: the receipt handle for the message to remove
    '''

    # delete the message to the queue
    client('sqs').delete_message(
        QueueUrl = f'{environ["QUEUE_BASE_URL"]}/{queue}',
        ReceiptHandle = receipt_handle,
    )
