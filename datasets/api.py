import requests
import time

# Config — consider moving these to Django settings later
DREMIO_BASE_URL = "https://your-dremio-host.com"
LOGIN_ENDPOINT = f"{DREMIO_BASE_URL}/apiv2/login"
API_BASE_URL = f"{DREMIO_BASE_URL}/api/v3"

USERNAME = "your_username"
PASSWORD = "your_password"


def get_dremio_token():
    """Authenticate to Dremio and return a bearer token."""
    response = requests.post(
        LOGIN_ENDPOINT,
        json={"userName": USERNAME, "password": PASSWORD}
    )
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.text}")
    
    return response.json()["token"]


def run_dremio_sql_job(sql_query):
    """Submit a SQL job to Dremio and return the result rows."""
    token = get_dremio_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. Submit the job
    submit_url = f"{API_BASE_URL}/sql"
    response = requests.post(submit_url, json={"sql": sql_query}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Job submission failed: {response.text}")
    
    job_id = response.json()["id"]

    # 2. Poll the job status until it's completed
    status_url = f"{API_BASE_URL}/job/{job_id}"
    while True:
        status_resp = requests.get(status_url, headers=headers)
        status = status_resp.json().get("jobState")
        if status == "COMPLETED":
            break
        elif status in ("FAILED", "CANCELED"):
            raise Exception(f"Job failed or canceled: {status}")
        time.sleep(1)

    # 3. Fetch the result
    result_url = f"{API_BASE_URL}/job/{job_id}/results"
    result_resp = requests.get(result_url, headers=headers)
    return result_resp.json().get("rows", [])
