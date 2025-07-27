"""  使用 openai 操作  """

import os
from openai import OpenAI
from pathlib import Path


class OpenaiService:

    api_key = ''
    base_url = ''

    def __init__(self, api_key: str = api_key, base_url: str = base_url) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def upload_file(self, file_path: str):
        """ 上传文件 """
        file_object = self.client.files.create(file=Path(file_path), purpose='fine-tune')
        return file_object

    def list_files(self):
        """ 列出文件 """
        file_list = self.client.files.list()
        return file_list.data

    def file_info(self, file_id: str):
        """ 获取文件信息 """
        file_info = self.client.files.retrieve(file_id=file_id)
        return file_info

    def download_batch_file(self, file_id: str):
        """ 批量下载文件 """
        content = self.client.files.content(file_id=file_id)
        content.write_to_file('batch_json.jsonl')

    def remove_file(self, file_id: str):
        """ 删除文件 """
        file_remove = self.client.files.delete(file_id=file_id)
        return file_remove

openai_service = OpenaiService()

# print(openai_service.remove_file('file-fe-d23c70cf43c543939730ed52'))

openai_service.list_files()
