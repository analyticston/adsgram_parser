from auth_data.postgresql import postgresql_data

sql_create_schema = f'''
CREATE SCHEMA IF NOT EXISTS {postgresql_data['table']['schema']}
'''

sql_create_table = f'''
CREATE TABLE IF NOT EXISTS {postgresql_data['table']['schema']}.{postgresql_data['table']['table']} 
(
    date        DATE,
    campaign_id INTEGER,
    UTM         VARCHAR(255),
    country     VARCHAR(255),
    impressions INTEGER,
    clicks      INTEGER,
    spent       NUMERIC,
    CPM         NUMERIC,
    CPC         NUMERIC,
    CTR         NUMERIC
)
'''

sql_insert_into = f'''
INSERT INTO {postgresql_data['table']['schema']}.{postgresql_data['table']['table']} 
(
    date,
    campaign_id,
    UTM,
    country,
    impressions,
    clicks,
    spent,
    CPM,
    CPC,
    CTR
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''
