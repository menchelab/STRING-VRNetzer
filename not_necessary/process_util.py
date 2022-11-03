import time

import psutil
import requests


def get_pid_of_process(process_names: list):
    """Get the PID of a running process addressed by name."""
    processes = [proc for proc in psutil.process_iter()]
    for p in processes:
        for name in process_names:
            if p.name().lower() == name:
                pid = p.pid
                return pid
    return None


def wait_until_ready(url, time_limit=30) -> bool:
    """Waits until an response is successful. Waits repeats until a certain time limit has passed."""
    response = requests.Response()
    start = time.time()
    while response.status_code != 200:
        try:
            response = requests.get(url)
        except ConnectionError as e:
            pass
        if time.time() - start > time_limit:
            raise TimeoutError
        # time.sleep(1)
    return True
