"""
"""
import os
db_host = os.getenv('MYSQL_HOST_LSK_KE')
DATABASE = dict(
        username=db_host.split(',')[0],
        password=db_host.split(',')[1],
        host=db_host.split(',')[2],
        table='LSK'
        )
API = dict(
        port=6060,
        threads=200,
        logs="log-twistd-api.log"
        )
MESSAGES = dict(
        miss="No records found",
        one="{name} is a registured lawyer with license number {number}. Status: {value}. More details: {link}",
        count="Found {count} results matching your query\n",
        multi="{name} - {number} - {value} \n"
        )
SMS = dict(
        port=6066,
        threads=30,
        logs='log-twistd-sms.log'
        )
CLOUDSEARCH = dict(
        url=os.getenv("CLOUDSEARCH_URL"),
        parser="simple"
        )
