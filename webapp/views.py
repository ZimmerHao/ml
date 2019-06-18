from django.shortcuts import render
from libs.kubernetes.client import K8SClient


def index(request):
    return render(request, 'webapp/index.html', {})


def pog_log(request, pod_name):
    k = K8SClient()
    lines = k.get_logs(pod_name)
    # lines = "..................."
    return render(request, 'webapp/index.html', {"lines": lines})
