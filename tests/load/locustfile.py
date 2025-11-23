# tests/load/locustfile.py
import contextlib
import os
import socket
from datetime import datetime, timezone

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from locust import HttpUser, between, events, task

# --- InfluxDB 설정 (Docker 환경변수에서 로드) ---
INFLUX_URL = f"http://{os.getenv('LOCUST_INFLUXDB_HOST', 'influxdb')}:8086"
INFLUX_TOKEN = os.getenv("LOCUST_INFLUXDB_TOKEN", "my-token")
INFLUX_ORG = os.getenv("LOCUST_INFLUXDB_ORG", "my-org")
INFLUX_BUCKET = os.getenv("LOCUST_INFLUXDB_BUCKET", "locust-bucket")

write_api = None
hostname = socket.gethostname()


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global write_api
    try:
        client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
        write_api = client.write_api(write_options=SYNCHRONOUS)
    except Exception:
        pass  # 연결 실패 처리 생략


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    if write_api:
        point = (
            Point("locust_requests")
            .tag("result", "failure" if exception else "success")
            .field("response_time", response_time)
            .time(datetime.now(timezone.utc))
        )
        # try:
        #     write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        # except:
        #     pass
        with contextlib.suppress(Exception):
            write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)


class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        # 로컬 백엔드 서버 호출
        self.client.get("/")
