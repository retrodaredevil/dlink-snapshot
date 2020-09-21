#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path
from time import sleep
import requests
from requests.auth import HTTPBasicAuth
import datetime


def main(args):
    url = args[0]
    username = args[1] if len(args) >= 2 else "admin"
    password = args[2] if len(args) >= 3 else "123456"
    storage_directory = Path("./images")
    recent_image = Path(storage_directory, "recent.jpg")

    while True:
        response = requests.get(url, stream=True, auth=HTTPBasicAuth(username, password), timeout=20)
        print(response.status_code)
        if response.status_code != 200:
            print("Unsuccessful")
            sleep(5)
            continue

        now = datetime.datetime.now()
        write_path = Path(storage_directory, "{}.{:02d}.{:02d} {:02d}:{:02d}.jpg"
                          .format(now.year, now.month, now.day, now.time().hour, now.time().minute))
        with write_path.open('wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        shutil.copyfile(write_path, recent_image)
        sleep(5)


if __name__ == '__main__':
    main(sys.argv[1:])
