from io import BufferedReader
from typing import Union

import boto3
from botocore.config import Config

default_signed_url_expires = 3600


class ObjectStorage:
  def __init__(self, provider: str, config: dict[str, Union[str, None]]):
    if provider == 'OSS':
      self.client = boto3.client(
        's3',
        aws_access_key_id=config['access_key_id'],
        aws_secret_access_key=config['access_key_secret'],
        endpoint_url=f"https://{config['region']}.aliyuncs.com",
        config=Config(s3={'addressing_style': 'virtual', 'signature_version': 's3v4'}),
      )
    elif provider == 'MINIO':
      self.client = boto3.client(
        's3',
        aws_access_key_id=config['access_key_id'],
        aws_secret_access_key=config['access_key_secret'],
        endpoint_url=config['endpoint'],
        config=Config(s3={'addressing_style': 'path', 'signature_version': 's3v4'}),
      )
    else:
      self.client = boto3.client('s3')

  def download_file(self, local_file: str, bucket: str, key: str) -> None:
    with open(local_file, 'wb') as data:
      self.client.download_fileobj(Bucket=bucket, Key=key, Fileobj=data)

  def put_object(self, bucket: str, key: str, body: Union[bytes, str, BufferedReader]) -> str:
    res = self.client.put_object(Bucket=bucket, Key=key, Body=body)
    return res['ETag']

  def get_object(self, bucket: str, key: str) -> bytes:
    res = self.client.get_object(Bucket=bucket, Key=key)
    return res['Body'].read()

  def get_object_signed_url(self, bucket: str, key: str, expires: int = default_signed_url_expires) -> str:
    return self.client.generate_presigned_url(
      'get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=expires
    )
