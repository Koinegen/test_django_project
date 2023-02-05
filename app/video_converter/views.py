from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseGone
from .forms import VideoForm, Video
from .lib.util import create_video_task_id
from .lib.converter import convert
from django.conf import settings
import os
from django.views.decorators.http import require_http_methods


def status(request, task_id):
    if task_id:
        a = Video.objects.filter(job_id=task_id).first()
        if a:
            return JsonResponse({"status": a.complete, "progress": a.status})
        else:
            return JsonResponse({})
    return JsonResponse({})


def page(request, task_id=None):
    context = {}
    if task_id:
        context = {"task_id": task_id}
    return render(request, 'video_converter/converter.html', context)


@require_http_methods(["GET"])
def download(request, task_id):

    db_obj = Video.objects.filter(job_id=task_id).first()
    if db_obj:
        if db_obj.complete == 1:
            file_location = os.path.join(settings.MEDIA_ROOT, db_obj.output_name)
            try:
                with open(file_location, 'rb') as f:
                    file_data = f.read()

                # sending response
                response = HttpResponse(file_data, content_type='application/video')
                response['Content-Disposition'] = f'attachment; filename="{task_id}.{db_obj.output_format}"'

            except IOError:
                # handle file not exist case here
                response = HttpResponseNotFound('<h1>File not exist</h1>')

            return response
    return HttpResponseNotFound('<h1>Download fail, try again later</h1>')


@require_http_methods(["POST"])
def model_form_upload(request):
    form = VideoForm(request.POST, request.FILES)
    if form.is_valid():
        video_obj: Video = form.save(commit=False)
        job_id = create_video_task_id(video_obj.name)
        video_obj.job_id = job_id
        video_obj.save()
        response = JsonResponse({"task_id": job_id})
        convert.apply_async(args=(job_id,))
        return response
    else:
        return JsonResponse({})

