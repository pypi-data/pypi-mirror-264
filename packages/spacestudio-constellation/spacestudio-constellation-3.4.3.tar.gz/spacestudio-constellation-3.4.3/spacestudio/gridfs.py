from .api_requests import get_request
from .urls import GRIDFS_URL
import requests


def write_stream_to_disk(path, stream: requests.Response):
    file_size = int(stream.headers.get('content-length', 0))
    chunk_size = 8192
    current_size = 0
    print()
    with open(path, 'wb') as f:
        with stream as s:
            for chunk in s.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                current_size += len(chunk)
                print(f"Downloading data to {path} : {formatted_size(current_size)}", end="")
                if file_size > 0:
                    print(f"/ {formatted_size(file_size)}", end="")
                print('                                \r', end="")

    print()


def formatted_size(size_in_bytes):
    units = ["B", "KB", "MB", "GB"]
    current_unit_index = 0
    converted_size = size_in_bytes
    while current_unit_index < len(units) - 1 and converted_size > 1024:
        current_unit_index += 1
        converted_size /= 1024
    return f"{round(converted_size, 2)} {units[current_unit_index]}"


def save_csv_file_to_disk(filename, path):
    stream = get_request(GRIDFS_URL + '/ascsv/' + filename, stream=True)
    write_stream_to_disk(path, stream)


def save_json_file_to_disk(filename, path):
    stream = get_request(GRIDFS_URL + '/asjson/' + filename, stream=True)
    write_stream_to_disk(path, stream)


def get_csv_as_json_object(filename):
    return get_request(GRIDFS_URL + '/csvasjson/' + filename)
