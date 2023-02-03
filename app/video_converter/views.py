from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .forms import VideoForm, Video
from .lib.util import create_video_task_id
from .lib.converter import convert
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

