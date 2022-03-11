import requests

import time

import json


class VKfoto:
    def __init__(self, token):
        self.token = token

    def search_photo(self, number_photo=5, album_id='profile'):
        url = 'https://api.vk.com/method/photos.get'
        param = {'extended': 'likes',
                 'album_id': album_id,
                 'access_token': self.token,
                 'v': '5.131'
                 }
        response = requests.get(url, params=param)
        items = response.json().get('response').get('items')
        photo_data = []
        photo_number = 0
        for item in items:
            sizes = item.get('sizes')
            max_size = 0
            index = 0
            for size in sizes:
                current_size = size.get('height') * size.get('width')
                if current_size > max_size:
                    max_size = current_size
                    index = sizes.index(size)
                if max_size == 0:
                    index = -1
            date = item.get('date')
            type = sizes[index].get('type')
            url = sizes[index].get('url')
            likes = item.get('likes').get('count')
            photo_data.append({'file_name': likes, 'file_url': url, 'type': type, 'date': date})
            photo_number += 1
            if photo_number == number_photo:
                break
        return photo_data



class Yadiskloader:
    def __init__(self, token: str):
        self.token = token

    def create_folder(self, path):
        headers = {'Accept': 'application/json',
                   'Authorization': 'OAuth {}'.format(self.token)}
        params = {'path': path}
        url = 'https://cloud-api.yandex.net/put/v1/disk/resources'
        create_folder = requests.put(url, headers=headers, params=params)
        if create_folder.status_code == 201:
            print(f'Папка {path} создана')
        elif create_folder.status_code == 409:
            print(f'Папка {path} существует')
        else:
            print(f'Папка {path} отсутствует')

    def create_file(self, json_data):
        with open("new.json", 'w') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=2)

    def upload(self, file_path: str, url_dict):
        self.create_folder(file_path)
        list_ = []
        json_data = []
        url_number = 0
        for file_item in url_dict:
            file = str(file_item.get('file_name'))
            file_url = file_item.get('file_url')
            file_date = file_item.get('date')
            file_type = file_item.get('type')
            if file in list_:
                file = str(file) + str(time.strftime('_%d_%m_%y', time.gmtime(file_date)))
            else:
                list_.append(file)
            headers = {'Accept': 'application/json',
                       'Authorization': 'OAuth {}'.format(self.token)}
            params = {'path': '/' + file_path + '/' + file,
                      'url': file_url}
            url = 'https://cloud-api.yandex.net/post/v1/disk/resources/upload'
            response = requests.post(url, headers=headers, params=params)
            quantity_url = len(url_dict)
            url_number += 1
            if response.status_code == 202:
                json_data.append({'file_name': file, 'size': file_type})
                print(f'Записано {url_number}/{quantity_url}')
            else:
                print(f'Ошибка {url_number}/{quantity_url}')
        self.create_file(json_data)


response = VKfoto('958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008')
url_dict = response.search_photo(number_photo=5)

if __name__ == '__main__':
    token = ''
    uploader = Yadiskloader(token)
    result = uploader.upload('VK', url_dict)