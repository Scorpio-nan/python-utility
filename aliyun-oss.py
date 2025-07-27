# -*- coding: utf-8 -*-

"""  阿里云 oss 操作  """

import alibabacloud_oss_v2 as oss
from datetime import datetime, timedelta
import uuid


class OssService:

    access_key_id = 'xxxxxxx'
    access_key_secret = 'xxxxxxxxxxx'
    region = 'xxxxxxxxxx'
    bucket = 'xxxxxxxxxxxxxx'
    endpoint = 'xxxxxxxxx'
    client: oss.client.Client
    domain = 'xxxxxxx'

    def __init__(self):
        credentials_provider = oss.credentials.StaticCredentialsProvider(self.access_key_id, self.access_key_secret)
        cfg = oss.config.load_default()
        cfg.credentials_provider = credentials_provider
        cfg.region = self.region
        cfg.endpoint = self.endpoint
        self.client = oss.Client(cfg)

    def upload_file(self, raw_data, file_name):
        """ 上传文件 """
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket,
            key=file_name,
            body=raw_data,
            content_type='application/octet-stream',
            content_disposition='inline'
        ))
        return result


oss_service = OssService()
p = 'C:/Users/26393/Pictures/Camera Roll/asset.jpeg'

with open(p, 'rb') as file:
    raw_data = file.read()

res = oss_service.upload_file(raw_data, f"{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())}.png")
