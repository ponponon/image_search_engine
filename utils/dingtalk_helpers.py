import requests
import settings
import os
from loguru import logger

run_mode = os.environ['RUN_MODE']


class DingTalk:
    webhook_url = settings.WEBHOOK_URL
    keyword = '报警'

    @classmethod
    def waring(cls, message: str):
        try:
            data = {
                'msgtype': 'text',
                'at': {
                    "atMobiles": [
                        "17816094181"   # 刘佳星
                    ],
                    "isAtAll": False
                },
                'text': {
                    'content': f'{cls.keyword} ({run_mode}环境): {message}'
                }
            }
            response = requests.post(cls.webhook_url, json=data)
            assert response.json().get('errcode') == 0, response.text
        except Exception as error:
            logger.warning(error)
