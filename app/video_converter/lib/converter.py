import subprocess
import re
from ..models import Video
from django.conf import settings
import os
from celery import shared_task


def to_ms(**kwargs) -> int:
    hour = int(kwargs.get("hour", 0))
    minute = int(kwargs.get("min", 0))
    sec = int(kwargs.get("sec", 0))
    ms = int(kwargs.get("ms", 0))

    return (hour * 60 * 60 * 1000) + (minute * 60 * 1000) + (sec * 1000) + ms


DUR_REGEX = re.compile(
        r"Duration: (?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})\.(?P<ms>\d{2})"
    )
TIME_REGEX = re.compile(
        r"out_time=(?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})\.(?P<ms>\d{2})"
    )


def _convert(file_in, file_out):
    proc = subprocess.Popen(["ffmpeg", "-progress", "-", "-nostats", "-i", file_in, file_out], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=False,)
    total_dur = None
    while proc:
        if proc.stdout is None:
            continue
        _str = proc.stdout.readline().decode('utf-8')
        if _str == "" and proc.poll() is not None:
            break
        if _str:
            total_dur_match = DUR_REGEX.search(_str)
            if total_dur_match:
                total_dur = to_ms(**total_dur_match.groupdict())
            if total_dur:
                progress_time = TIME_REGEX.search(_str)
                if progress_time:


                    elapsed_time = to_ms(**progress_time.groupdict())
                    yield (int(elapsed_time / total_dur * 100))


@shared_task()
def convert(job_id): #db_object: Video):
    db_object = Video.objects.filter(job_id=job_id).first()
    _in = os.path.join(settings.MEDIA_ROOT, db_object.video.path)
    _out = os.path.join(settings.MEDIA_ROOT, db_object.output_name)
    print(_in)
    print(_out)
    for i in _convert(_in, _out):
        db_object.status = i
        db_object.save(update_fields=['status'])

    db_object.complete = 1
    db_object.status = 100
    db_object.save(update_fields=['status', 'complete'])



