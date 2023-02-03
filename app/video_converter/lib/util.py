from hashlib import md5
import time


def create_video_task_id(name=''):
    return md5(f'{time.time()}{name}'.encode('utf-8')).hexdigest()
