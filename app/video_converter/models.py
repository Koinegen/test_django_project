from django.db import models
import os
import hashlib
import time


def rename_file(instance, filename):
    ext = filename.split('.')[-1]
    _h = hashlib.md5(f'{filename}_{time.time()}'.encode('utf-8')).hexdigest()
    filename = f"{_h}.{ext}"
    instance.output_name = os.path.join('output', f'{_h}.{instance.output_format}')
    return os.path.join('video', filename)

def get_name(filename):
    return filename.split('/')[-1].split('.')[0]


class Video(models.Model):
    name = models.CharField(max_length=255, blank=True)
    job_id = models.CharField(max_length=255, blank=True)
    output_format = models.CharField(max_length=10, blank=True)
    video = models.FileField(upload_to=rename_file)
    output_name = models.CharField(max_length=255, blank=True)
    complete = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

# complete field
# 0 - in_progress
# 1 - success
# 2 - error
# 3 - wait another tasks

