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
