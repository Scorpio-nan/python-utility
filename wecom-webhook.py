import requests
import json

WEB_HOOK_KEY = '807f2a8e-8b9a-495b-9b4b-2d5e31a9a396'
WEB_HOOK_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}'.format(WEB_HOOK_KEY)

def send_message():
    """ 给企业微信发送消息通知 """
    headers = {
        'Content-Type': 'application/json',
    }

    msg = {
        'msgtype': 'markdown_v2',
        'markdown_v2': {
            'content': """
## 📌  新用户消息提醒
- **用户昵称**: nanxiangyuan
- **注册时间**: 2025-09-15
- **归属地**: 湖北武汉
- **性别**: 男 
            """,
            'mentioned_list': ['@all']
        }
    }

    res = requests.post(WEB_HOOK_URL.format(), headers=headers, data=json.dumps(msg))
    if res.status_code == 200:
        print('消息发送成功..')
    else:
        print('消息发送失败..')
    print(res)


send_message()





