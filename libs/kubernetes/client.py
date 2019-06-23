from __future__ import absolute_import

from kubernetes import client as kube_client
from kubernetes import config as kube_config
from kubernetes import utils as kube_utils


class K8SClient:
    def __init__(self):
        try:
            kube_config.load_incluster_config()
        except:
            kube_config.load_kube_config()
        self.k_client_v1 = kube_client.CoreV1Api()

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
        ret = self.k_client_v1.read_namespaced_pod_log(
            resource_name, namespace, follow=False
        )
        return ret

    def apply_sparkapp_yaml_file(
        self,
        yaml_url: str,
        namespace: str = "default",
        fqdn: str = "sparkoperator.k8s.io",
        resource: str = "sparkapp",
        body: dict = {},
    ):
        k8s_api_client = kube_client.ApiClient()
        kube_utils.create_from_yaml(k8s_api_client, yaml_url)
        k8s_api = kube_client.ExtensionsV1beta1Api(k8s_api_client)

        body["apiVersion"] = "sparkoperator.k8s.io/v1beta1"
        body["kind"] = "sparkapp"
        body["metadata"]["name"] = "example-spark-pi"
        res = k8s_api.get_api_resources(
            namespace=namespace, resource=resource, body=body, fqdn=fqdn
        )

        return f"SparkApp {res.metadata.name} created"
