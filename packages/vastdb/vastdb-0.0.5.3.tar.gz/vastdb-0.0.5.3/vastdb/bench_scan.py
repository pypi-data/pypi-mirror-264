from vastdb import api

from logbook import Logger, StreamHandler
import sys
import time
import pprint

StreamHandler(sys.stdout).push_application()
log = Logger('Logbook')

# access_key_id=F3YUMQZDQB60ZZJ1PBAZ
# secret_access_key=9a9Q3if6IC5LjUexly/nXFv1UCANBnhGxi++Sw6p

a = api.VastdbApi(
    access_key='F3YUMQZDQB60ZZJ1PBAZ', 
    secret_key='9a9Q3if6IC5LjUexly/nXFv1UCANBnhGxi++Sw6p', 
    host='172.19.111.1:172.19.111.16')

kwargs = dict(
    bucket='tabular-slothful-jocular-jack',
    schema='tpcds_schema_create_as_select',
    table='store_sales',
    field_names=['ss_sold_date_sk', 'ss_sold_time_sk', 'ss_item_sk'],
    filters={'ss_item_sk': ['le 1']},
    num_sub_splits=8)

pprint.pprint(kwargs)

res = a.query_iterator(**kwargs)

total_bytes = 0
total_rows = 0
start = time.time()
last_log = None

for b in res: 
    total_bytes += b.get_total_buffer_size()
    total_rows += len(b)
    dt = time.time() - start
    if last_log != int(dt):
        log.info("{:.3f} Mrow/s, {:.3f} MB/s", (total_rows/dt) / 1e6, (total_bytes/dt) / 1e6)
        last_log = int(dt)

dt = time.time() - start
log.info("Done after {:.3f} seconds, {:.3f} Mrows, {:.3f} MB", dt, total_rows / 1e6, total_bytes / 1e6)