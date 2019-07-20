from __future__ import absolute_import

from kubernetes import client as kube_client
from kubernetes import config as kube_config
import yaml
from urllib.request import urlopen


class K8SClient:
    def __init__(self):
        try:
            kube_config.load_incluster_config()
        except:
            kube_config.load_kube_config()
        self.k_client_v1 = kube_client.CoreV1Api()
        self._SPARKAPP_GROUP = "sparkoperator.k8s.io"
        self._SPARKAPP_VERSION = "v1beta1"
        self._SPARKAPP_PLURAL = "sparkapplications"

    def get_resources_namespaced(self, resource: str, namespace: str = "default"):
        if resource in ["pods", "pod", "po"]:
            ret = self.k_client_v1.list_namespaced_pod(namespace=namespace, watch=False)
            for i in ret.items:
                print(
                    "%s\t%s\t%s"
                    % (i.status.pod_ip, i.metadata.namespace, i.metadata.name)
                )
            return ret
        else:
            return "Why don't you try Pods!"

    def get_logs(self, resource_name: str, namespace: str = "default"):
        print("get log ", resource_name)
        ret = self.k_client_v1.read_namespaced_pod_log(
            resource_name, namespace, follow=True, _preload_content=False,
        )
        return ret

    def init_k8s_instance_for_spark_app(self, yaml_url: str):
        response = urlopen(yaml_url)
        try:
            yaml_obj = yaml.safe_load(response)
            api_instance = kube_client.CustomObjectsApi(kube_client.ApiClient())
            return api_instance, yaml_obj
        except yaml.YAMLError as e:
            print(str(e))

    def apply_sparkapp_yaml_file(self, yaml_url: str):
        api_instance, yaml_obj = self.init_k8s_instance_for_spark_app(yaml_url)
        # Create CRD sparkapp
        api_instance.create_namespaced_custom_object(
            group=self._SPARKAPP_GROUP,
            version=self._SPARKAPP_VERSION,
            namespace=yaml_obj['metadata']['namespace'],
            plural=self._SPARKAPP_PLURAL,
            body=yaml_obj,
        )

        res = api_instance.get_namespaced_custom_object(
            group=self._SPARKAPP_GROUP,
            version=self._SPARKAPP_VERSION,
            namespace=yaml_obj['metadata']['namespace'],
            plural=self._SPARKAPP_PLURAL,
            name=yaml_obj["metadata"]["name"],
        )
        return f"SparkApp {res['metadata']['name']} created"

    def delete_sparkapp_yaml_file(self, yaml_url: str,):
        api_instance,yaml_obj = self.init_k8s_instance_for_spark_app(yaml_url)
        res = api_instance.delete_namespaced_custom_object(
            group=self._SPARKAPP_GROUP,
            version=self._SPARKAPP_VERSION,
            plural=self._SPARKAPP_PLURAL,
            namespace=yaml_obj['metadata']['namespace'],
            name=yaml_obj["metadata"]["name"],
            body=kube_client.V1DeleteOptions(),
        )
        return f"SparkApp {res['details']['name']} deleted"
