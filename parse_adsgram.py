import json
from custom_requests import web_requests
import calendar
from datetime import date, timedelta
import pandas as pd
from io import StringIO


def get_auth_token_adsgram(login, password):
    # Authorization on the site and get an auth_token for further work in the authorized zone
    auth_data = {"email": login, "password": password}
    response = web_requests(url='https://api.adsgram.ai/api/public/user/auth',
                            json=auth_data,
                            request_type='post')
    response = response.headers.get('set-cookie')
    index = [i for i, x in enumerate(response.split(';')) if x[:10] == 'SessionId=']
    auth_token = response.split(';')[index[0]].split('=')[1]
    return auth_token


def collect_url_statistics_campaigns_csv(campaign_id):
    # Generates an API link to download a CSV file for a specific campaign in the context of all countries for yesterday
    yesterday = date.today() - timedelta(days=1)
    startdate = enddate = calendar.timegm(yesterday.timetuple())
    slice = 'COUNTRY'
    return (
            'https://api.adsgram.ai/api/statistics/campaigns/csv?' +
            "campaignIds=" + str(campaign_id) +
            "&enddate=" + str(enddate) +
            "&slice=" + slice +
            "&startdate=" + str(startdate)
    )


def collect_url_campaigns_yesterday():
    # Generates an API link to download the IDs of all campaigns active yesterday. Sorting - impressions desc
    startDate = calendar.timegm((date.today() - timedelta(days=1)).timetuple())
    endDate = calendar.timegm(date.today().timetuple()) - 1
    size = 2000
    sort = "impressions%2Cdesc"
    return (
            'https://api.adsgram.ai/api/campaigns?' +
            "startDate=" + str(startDate) +
            "&endDate=" + str(endDate) +
            "&size=" + str(size) +
            "&sort=" + str(sort)
    )


def get_campaign_url(campaign_id, auth_token):
    # Get a link to the adsgram campaign
    url = f'https://api.adsgram.ai/api/campaigns/{campaign_id}'
    cookies = {'SessionId': auth_token}
    response = web_requests(url=url, cookies=cookies)

    json_file = json.loads(response.text)
    return json_file['ads'][0]['link']


def get_all_campaing_ids(auth_token):
    # Open the API and download all campaigns from yesterday
    cookies = {'SessionId': auth_token}
    url = collect_url_campaigns_yesterday()
    response = web_requests(url=url, cookies=cookies)

    json_file = json.loads(response.text)

    campaign_ids = []

    for campaign in json_file['content']:
        if campaign['statistics']['impressions'] != 0:
            campaign_ids.append(campaign['id'])

    return campaign_ids


def download_campaign_data_to_df(campaign_id, auth_token):
    # Downloading a CSV file for a specific campaign in the context of all countries for yesterday.
    # The download takes place via the SessionID token
    cookies = {'SessionId': auth_token}
    url = collect_url_statistics_campaigns_csv(campaign_id=campaign_id)
    response = web_requests(url=url, cookies=cookies)
    return pd.read_csv(StringIO(str(response.content, 'utf-8')))
