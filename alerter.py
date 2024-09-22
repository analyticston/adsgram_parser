import requests
from auth_data.tg_alert_bot import is_tg_alert_enabled, tg_access_token, tg_chat_id, tg_support_account

alert_images = {
    'Error': 'https://i.ibb.co/BzFNm13/script-handling.png',
    'Success': 'https://i.ibb.co/7nbzqFJ/success.webp',
    'Login error': 'https://i.ibb.co/THbrxVd/User-errors-min-png.webp',
    'DB Error': 'https://i.ibb.co/56WYkbc/DB-Error.jpg'
}


def send_alert(alert_text, alert_type='Error', parse_mode='MarkdownV2'):
    # Send messages about code execution statuses
    if is_tg_alert_enabled:
        url = f'https://api.telegram.org/bot{tg_access_token}/sendPhoto'
        data = {
            'chat_id': tg_chat_id,
            'caption': alert_text,
            'photo': alert_images[alert_type],
            'parse_mode': parse_mode
        }
        response = requests.post(url, data=data)

        if response.status_code != 200:
            print('send_alert error')
    else:
        print(f'{alert_type}: {alert_text}')
