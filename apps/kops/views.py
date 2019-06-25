from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from libs.kubernetes.client import K8SClient


class PodLogView(APIView):
    permission_classes = (
        permissions.AllowAny,
    )
    parser_classes = (JSONParser,)

    def get(self, request):
        pod_name = request.query_params.get("pod_name")
        k = K8SClient()
        lines = k.get_logs(pod_name)
        return Response({"lines": lines}, status=status.HTTP_200_OK)


class ApplyYamlView(APIView):
    permission_classes = (
        permissions.AllowAny,
    )
    parser_classes = (JSONParser,)

    def post(self, request):
        yaml_url = request.data.get("yaml_url")
        k = K8SClient()
        lines = k.apply_sparkapp_yaml_file(yaml_url)
        return Response({"lines": lines}, status=status.HTTP_200_OK)

class DeleteByYamlView(APIView):
    permission_classes = (
        permissions.AllowAny,
    )
    parser_classes = (JSONParser,)

    def post(self, request):
        yaml_url = request.data.get("yaml_url")
        k = K8SClient()
        lines = k.delete_sparkapp_yaml_file(yaml_url)
        return Response({"lines": lines}, status=status.HTTP_200_OK)