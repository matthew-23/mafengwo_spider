import os
import json

import requests
import shutil


def download_pics(pic_urls, path):
    index = 1
    for pic_url in pic_urls:
        try:
            r = requests.get(pic_url, stream=True)
        except Exception:
            continue
        pic_name = str(index) + '.jpeg'
        if r.status_code == 200:
            with open(os.path.join(path, pic_name), 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        index += 1


def write_gender(gender, path):
    with open(os.path.join(path, gender), 'a') as f:
        os.utime(path, None)


def main():
    file_names = os.listdir(os.path.join(os.getcwd(), 'data'))
    for file_name in file_names:
        print(file_name)
        with open(os.path.join(os.getcwd(), 'data', file_name), 'r') as f:
            posts = json.loads(f.read())
            city_name = file_name.split('.')[0]
            city_dir = os.path.join(os.getcwd(), 'pics', city_name)

            try:
                os.mkdir(city_dir)
            except Exception:
                pass

            index = 1
            for post in posts:
                for k in post:
                    if k != 'gender':
                        print(index)
                        path = os.path.join(city_dir, str(index))
                        try:
                            os.mkdir(path)
                        except Exception:
                            pass

                        print(path)
                        # download_pics(post[k], path)
                    else:
                        print(index)
                        path = os.path.join(city_dir, str(index))
                        write_gender(post[k], path)

                index += 1


if __name__ == '__main__':
    main()
