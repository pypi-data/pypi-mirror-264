import json
import requests


def seatalk_notification(
        group_id: str,
        text: str,
        markdown: bool = True,
        mention_lst: list = None
):
    content_type = 'markdown' if markdown else 'text'
    data = {
        'tag': content_type,
        content_type: {
            'content': text,
            'mentioned_email_list': mention_lst,
            'at_all': False,
            'format': 1  # 1: markdown | 2: text
        }
    }

    response = requests.post(
        group_id,
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise ValueError(f'Request returned an error {response.status_code}, the response is:\n{response.text}')


# group_id = 'https://openapi.seatalk.io/webhook/group/_3ek_iqGTvu_-jnOuZ7yjA'  # Survey
# text = 'aaa [download](https://openapi.seatalk.io)'
# seatalk_notification(group_id, text=text, markdown=True)
