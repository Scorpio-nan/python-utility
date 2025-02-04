import numpy as np
from numpy import dot
from numpy.linalg import norm
from openai import OpenAI
import os

BASE_URL = 'https://api.openai-hk.com/v1'

client = OpenAI(api_key=os.getenv('OPEN_API_KEY'), base_url=BASE_URL)

def cos_sim(a,b):
    """
    计算余弦距离 -- 距离越大越相似
    :param a:
    :param b:
    :return:
    """
    return dot(a,b)/(norm(a)*norm(b))

def l2(a,b):
    """
    计算欧氏距离 -- 距离越小越相似
    :param a:
    :param b:
    :return:
    """
    x = np.asarray(a) - np.asarray(b)
    return norm(x)

def get_embedding(texts, model='text-embedding-ada-002', dimensions=None):
    """
    封装 OpenAi 的 embedding 接口
    :param texts:
    :param model:
    :param dimensions:
    :return:
    """
    if model == 'text-embedding-ada-002':
        dimensions = None
    if dimensions:
        data = client.embeddings.create(input=texts, model=model, dimensions=dimensions).data
    else:
        data = client.embeddings.create(input=texts, model=model).data
    return [x.embedding for x in data]

query = "国际争端"

documents = [
    '联合国就苏丹达尔富尔地区的大规模暴利事件发出警告',
    '土耳其,芬兰,瑞典与北约代表将继续就瑞典入约问题进行谈判',
    '日本岐阜市陆上自卫队射击场内发生枪击事件, 至5人死亡, 3人受伤',
    '我国首次在空间站外展开探月行动',
    '美国坠机事故遇难的花滑少年刚入驻小红书',
    '中央气象台：今起到初五我国中东部大范围雨雪来袭'
]

query_vec = get_embedding([query])[0]
doc_vec = get_embedding(documents)

print('query 与自己的余弦距离: {:.2f}'.format(cos_sim(query_vec, query_vec)))
print('query 的余弦与查询文档余弦的距离:')
for vec in doc_vec:
    print(cos_sim(query_vec, vec))

print()

print('query 与自己的欧氏距离: {:.2f}'.format(l2(query_vec, query_vec)))
print('query 的余弦与查询文档的欧氏距离:')
for vec in doc_vec:
    print(l2(query_vec, vec))



