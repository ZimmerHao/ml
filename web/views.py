from django.shortcuts import render
from libs.kubernetes.client import K8SClient


def index(request):
    return render(request, 'webapp/index.html', {})


def pod_log(request, pod_name):
    k = K8SClient()
    lines = k.get_logs(pod_name)
    # lines = "..................."
    return render(request, 'webapp/index.html', {"lines": lines})


def submit_yaml_by_url(request, yaml_url="https://raw.githubusercontent.com/GoogleCloudPlatform/spark-on-k8s-operator/master/examples/spark-pi.yaml"):
    k = K8SClient()
    lines = k.apply_sparkapp_yaml_file(yaml_url)
    return render(request, 'webapp/index.html', {"lines": lines})