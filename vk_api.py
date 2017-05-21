# coding=utf-8
import requests
from config import VK_API_URL, VK_WALL_SEARCH, VK_TOKEN


def get_train(_date):
    url = add_param(VK_API_URL + VK_WALL_SEARCH, 'owner_id', '-69673853', True)
    url = add_param(url, 'domain', '4722', False)
    url = add_param(url, 'query', _date, False)
    url = add_param(url, 'access_token', VK_TOKEN, False)
    response = requests.get(url)
    response_list = response.json()['response']
    if len(response_list) <= 1:
        return 'Тренировка по данной дате не найдена'
    else:
        for x in range(1, response_list[0] + 1):
            train = response_list[x]['text']
            if _date in train:
                return reformat_html_str(train.encode('utf-8'), _date)
    return 'Тренировка по данной дате не найдена'


def add_param(request, param_name, param_value, first):
    prefix = '?' if first else '&'
    return request + prefix + param_name + '=' + param_value


def reformat_html_str(html_str, date):
    result = html_str.replace('<br>', '\n')
    return result.replace(date, '<b>' + date + '</b>')


def add_info(html_str):
    return html_str + ''
