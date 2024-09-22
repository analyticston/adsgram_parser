import requests
import time
import psycopg2

from alerter import send_alert
from auth_data.tg_alert_bot import tg_support_account

# The delay time between code execution attempts in case of errors
retry_timeout = 600


def web_requests(url, cookies=None, json=None, request_type='get', timeout=retry_timeout):
    # Trouble-free sending of requests to sites
    response = None
    while True:
        try:
            if request_type == 'get':
                response = requests.get(url=url, cookies=cookies)
            elif request_type == 'post':
                response = requests.post(url=url, json=json)
            if response.status_code == 403 and request_type == 'post':
                send_alert(alert_text=f'*__Adsgram authorization error\.__*\n\n'
                                      f'Check the correctness of the username and password from adsgram\.\n\n'
                                      f'📂 Change the data: `\\\\auth\_data\\\\adsgram\.py`\n\n'
                                      f'To write about the error\: \@{tg_support_account}',
                           alert_type='Login error')
                exit(0)
            elif response.status_code != 200:
                send_alert(alert_text=f'Requests status code \({request_type}\)\: {response.status_code}\.\n\n'
                                      f'⏳ Retrying\.\.\. \n\n'
                                      f'To write about the error\: \@{tg_support_account}')
                time.sleep(timeout)
            else:
                break
        except requests.exceptions.RequestException as err:
            send_alert(alert_text=f'Data request error.\n\n'
                                  f'Error text: "{err}"\n\n'
                                  f'To write about the error\: \@{tg_support_account}',
                       parse_mode='')
            time.sleep(timeout)

    return response


def db_connect(db_params, sql_code, sql_data=None, mod='single', timeout=retry_timeout):
    conn = None
    cursor = None
    while True:
        try:
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()
            if mod == 'single':
                cursor.execute(sql_code)
            elif mod == 'many':
                cursor.executemany(sql_code, sql_data)
            conn.commit()
            cursor.close()
            conn.close()
            break
        except psycopg2.OperationalError as err:
            send_alert(alert_text=f'Database connection error.\n\n'
                                  f'Error text: "{err}"\n\n'
                                  f'To write about the error\: \@{tg_support_account}',
                       alert_type='DB Error',
                       parse_mode='')
            time.sleep(timeout)
    return conn, cursor
