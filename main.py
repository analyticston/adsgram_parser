from parse_adsgram import get_auth_token_adsgram, get_all_campaing_ids, get_campaign_url, download_campaign_data_to_df
from auth_data.adsgram import login, password
from auth_data.postgresql import postgresql_data
from auth_data.tg_alert_bot import tg_support_account
from parse_url import custom_parse_url
from database import PostgresqlConn
from alerter import send_alert


def main():
    # Authorization on the site and get an auth_token for further work in the authorized zone
    auth_token = get_auth_token_adsgram(login=login, password=password)

    # Get a list of all active campaigns for yesterday
    campaign_ids = get_all_campaing_ids(auth_token)

    # Get statistics on all active campaigns for yesterday
    campaign_urls = []
    campaign_data = []
    for ids in campaign_ids:
        # Get a campaign UTM-link
        url = get_campaign_url(campaign_id=ids, auth_token=auth_token)
        url = custom_parse_url(url)
        campaign_urls.append(url)

        # Get campaign statistics
        df = download_campaign_data_to_df(campaign_id=ids, auth_token=auth_token)
        campaign_data.append(df)

    if len(campaign_ids) == len(campaign_urls) and len(campaign_ids) == len(campaign_data):
        # Connecting to PostgreSQL and uploading data
        conn = PostgresqlConn(postgresql_data=postgresql_data['connect'],
                              campaign_ids=campaign_ids,
                              campaign_urls=campaign_urls,
                              campaign_data=campaign_data)
        conn.collect_and_insert_into_database()
    else:
        send_alert(alert_text=f'*__Program execution logic error\.__*\n\n'
                              f'To write about the error\: \@{tg_support_account}', )


if __name__ == "__main__":
    main()
