from datetime import date, timedelta

from alerter import send_alert
from sql_config import sql_create_table, sql_insert_into, sql_create_schema
from custom_requests import db_connect
from auth_data.tg_alert_bot import tg_support_account


class PostgresqlConn():
    def __init__(self, postgresql_data, campaign_ids, campaign_urls, campaign_data):
        self.postgresql_data = postgresql_data
        self.campaign_ids = campaign_ids
        self.campaign_urls = campaign_urls
        self.campaign_data = campaign_data

    def create_table(self):
        # CREATE SCHEMA IF NOT EXISTS
        db_connect(db_params=self.postgresql_data,
                   sql_code=sql_create_schema)
        # CREATE TABLE IF NOT EXISTS
        db_connect(db_params=self.postgresql_data,
                   sql_code=sql_create_table)

    def prepare_data(self, campaign_id, campaign_url, campaign_data):
        # To collect data into a single whole
        data = []
        yesterday_dt = date.today() - timedelta(days=1)
        for row in campaign_data.itertuples():
            data.append((yesterday_dt,
                         campaign_id,
                         campaign_url,
                         row.Country,
                         row.Impressions,
                         row.Clicks,
                         row.Spent,
                         row.CPM,
                         row.CPC,
                         row.CTR))
        return data

    def insert_into(self, campaigns_data):
        # Writing to the postgresql database
        db_connect(db_params=self.postgresql_data,
                   sql_code=sql_insert_into,
                   sql_data=campaigns_data,
                   mod='many')

    def collect_and_insert_into_database(self):
        # The main function.
        # Collects all data uploaded from Adsgram. Prepares the database for loading and loads the data.
        self.create_table()

        adsgram_data = []
        for i in range(len(self.campaign_ids)):
            id = self.campaign_ids[i]
            url = self.campaign_urls[i]
            df = self.campaign_data[i]

            campaign = self.prepare_data(id, url, df)
            adsgram_data = adsgram_data + campaign

        if len(adsgram_data) != 0:
            self.insert_into(adsgram_data)
            send_alert(alert_text=f'*__Successfully downloaded and uploaded\.__*\n\n'
                                  f'•  Total active campaigns yesterday\: *{len(self.campaign_ids)}*\n'
                                  f'•  Total rows loaded into the table\: *{len(adsgram_data)}*\n\n'
                                  f'To write about the error\: \@{tg_support_account}',
                       alert_type='Success')
        else:
            send_alert(alert_text=f'*__There were no active campaigns yesterday\.__*\n\n'
                                  f'To write about the error\: \@{tg_support_account}',
                       alert_type='Success')
