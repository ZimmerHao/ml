from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from libs.kubernetes.client import K8SClient
from .serializers import PodSerializer
from rest_framework import generics


# class PodsListView(APIView):
class PodsListView(generics.ListCreateAPIView):
    parser_classes = (JSONParser,)
    #     try:
    #         namespace = request.query_params.get("namespace")
    #         if not namespace:
    #             raise ValueError
    #     except:
    #         namespace = "default"

    lines = []
    namespace = "default"
    k = K8SClient()
    res = k.get_resources_namespaced(resource="po", namespace=namespace)

    for r in res.items:
        lines.append({
            "pod_name": r.metadata.name,
            "pod_status": r.status.phase,
            "pod_namespace": r.metadata.namespace,
            "created_time": r.metadata.creation_timestamp,
        })
    queryset = lines
    serializer_class = PodSerializer
    # return Response(lines, status=status.HTTP_200_OK)


class PodLogView(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)

    def get(self, request):
        pod_name = request.query_params.get("pod_name")
        k = K8SClient()
        lines = k.get_logs(pod_name)
        print(type(lines))
        # d = lines.data
        # print(type(d))
        # print("aaa", d, "ccccc")
        return Response({"lines": lines}, status=status.HTTP_200_OK)


class ApplyYamlView(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)

    def post(self, request):
        yaml_url = request.data.get("yaml_url")
        k = K8SClient()
        lines = k.apply_sparkapp_yaml_file(yaml_url)
        return Response({"lines": lines}, status=status.HTTP_200_OK)


class DeleteByYamlView(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)

    def post(self, request):
        yaml_url = request.data.get("yaml_url")
        k = K8SClient()
        lines = k.delete_sparkapp_yaml_file(yaml_url)
        return Response({"lines": lines}, status=status.HTTP_200_OK)
