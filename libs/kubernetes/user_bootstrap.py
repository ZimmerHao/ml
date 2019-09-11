from libs.kubernetes.client import K8SClient
from kubernetes import client as kube_client
from libs.utils import generate_hash_by_username_creation_epoch


class K8SClientUserInit(K8SClient):
    def bootstrap_new_user(self, hashed_username: str) -> None:
        self.create_namespace(hashed_username)
        self.create_service_account_namespaced(hashed_username)
        self.update_rolebinding_serviceaccount_namespaced(hashed_username)
        self.create_ingress_namespaced_from_template(hashed_username)
        # self.create_tls_secret_namespaced(hashed_username, "ui")
        # self.create_tls_secret_namespaced(hashed_username, "drone")
        # self.create_configmap_namespaced(hashed_username)
        # self.create_deployment_namespaced(hashed_username)
        # self.create_service_namespaced(hashed_username)

    def create_service_account_namespaced(self, hashed_username):
        ret = self.k_client_v1.create_namespaced_service_account(
            namespace=f"ns-{hashed_username}",
            body=kube_client.V1ServiceAccount(
                api_version="v1",
                kind="ServiceAccount",
                metadata=kube_client.V1ObjectMeta(
                    name=f"traefik-ingress-serviceaccount",
                    namespace=f"ns-{hashed_username}",
                ),
            ),
        )
        return ret

    def update_rolebinding_serviceaccount_namespaced(
        self,
        hashed_username: str,
        cluster_role_binding_name: str = "traefik-ingress-clusterrolebinding",
    ):
        current_cluster_role_binding_obj = self.k_client_rbac_auth_v1_beta1.read_cluster_role_binding(
            name=cluster_role_binding_name
        )

        ret = self.k_client_rbac_auth_v1_beta1.patch_cluster_role_binding(
            name=cluster_role_binding_name,
            body=kube_client.V1beta1ClusterRoleBinding(
                api_version=current_cluster_role_binding_obj.api_version,
                kind=current_cluster_role_binding_obj.kind,
                metadata=current_cluster_role_binding_obj.metadata,
                role_ref=current_cluster_role_binding_obj.role_ref,
                subjects=current_cluster_role_binding_obj.subjects.append(
                    kube_client.V1beta1Subject(
                        kind="ServiceAccount",
                        name="traefik-ingress-serviceaccount",
                        namespace=f"ns-{hashed_username}",
                    )
                ),
            ),
        )
        return ret

    def create_tls_secret_namespaced(
        self, hashed_username: str, secret_name: str
    ) -> dict:
        ret = self.k_client_v1.create_namespaced_secret(
            namespace=f"ns-{hashed_username}",
            body=kube_client.V1Secret(
                api_version="v1",
                kind="Secret",
                metadata=kube_client.V1ObjectMeta(
                    name=f"traefik-{secret_name}-tls-cert",
                    namespace=f"ns-{hashed_username}",
                    labels={"k8s-app": "traefik-ingress-controller"},
                ),
                type="kubernetes.io/tls",
                data={"tls.crt": "", "tls.key": ""},
            ),
        )
        return ret

    def create_configmap_namespaced(self, hashed_username: str) -> dict:
        ret = self.k_client_v1.create_namespaced_config_map(
            namespace=f"ns-{hashed_username}",
            body=kube_client.V1ConfigMap(
                api_version="v1",
                kind="ConfigMap",
                metadata=kube_client.V1ObjectMeta(
                    name=f"traefik-ingress-configmap", namespace=f"ns-{hashed_username}"
                ),
                data={
                    "traefik.toml": f"""
                        defaultEntryPoints = ["https","http"]
                        [entryPoints]
                        [entryPoints.http]
                        address = ":80"
                        [entryPoints.http.auth.forward]
                        address = "http://console.deepvega.com/hi/auth"
                        [entryPoints.https]
                        address = ":443"
                        [entryPoints.https.tls]
                        [[entryPoints.https.tls.certificates]]
                        CertFile = "/ssl/ui/tls.crt"
                        KeyFile = "/ssl/ui/tls.key"
                        [[entryPoints.https.tls.certificates]]
                        CertFile = "/ssl/drone/tls.crt"
                        KeyFile = "/ssl/drone/tls.key"
                        [kubernetes]
                        [kubernetes.ingressEndpoint]
                        publishedService = "default/traefik-ingress-controller-http-service"
                        [ping]
                        entryPoint = "http"
                        [api]
                        entryPoint = "webapp"
                    """
                },
            ),
        )
        return ret

    def create_service_namespaced(self, hashed_username: str) -> dict:
        ret = self.k_client_v1.create_namespaced_service(
            namespace=f"ns-{hashed_username}",
            body=kube_client.V1Service(
                api_version="v1",
                kind="Service",
                metadata=kube_client.V1ObjectMeta(
                    name=f"traefik-ingress-controller-http-service",
                    namespace=f"ns-{hashed_username}",
                ),
                spec=kube_client.V1ServiceSpec(
                    selector={"k8s-app": "traefik-ingress-controller"},
                    ports=[
                        kube_client.V1ServicePort(name="http", protocol="TCP", port=80),
                        kube_client.V1ServicePort(
                            name="https", protocol="TCP", port=443
                        ),
                    ],
                    type="NodePort",
                ),
            ),
        )
        return ret

    def create_namespace(self, hashed_username: str) -> dict:
        ret = self.k_client_v1.create_namespace(
            kube_client.V1Namespace(
                api_version="v1",
                kind="Namespace",
                metadata=kube_client.V1ObjectMeta(name=f"ns-{hashed_username}"),
            )
        )
        return ret

    def delete_namespace(self, ns_name: str) -> dict:
        ret = self.k_client_v1.delete_namespace(ns_name)
        return ret

    def create_ingress_namespaced_from_template(self, hashed_username) -> None:
        ret = self.k_client_ext_v1_beta1.create_namespaced_ingress(
            namespace=f"ns-{hashed_username}",
            body=kube_client.V1beta1Ingress(
                api_version="extensions/v1beta1",
                kind="Ingress",
                metadata=kube_client.V1ObjectMeta(
                    name=f"traefik-ingress-controller-{hashed_username}-ingress-auth",
                    namespace=f"ns-{hashed_username}",
                    annotations={
                        "kubernetes.io/ingress.class": "traefik",
                        "traefik.ingress.kubernetes.io/frontend-entry-points": "http,https",
                        "traefik.ingress.kubernetes.io/redirect-entry-point": "https",
                        "traefik.ingress.kubernetes.io/redirect-permanent": '"true"',
                        "ingress.kubernetes.io/auth-type": "forward",
                        "ingress.kubernetes.io/auth-url": "http://webapp.default.svc.cluster.local:5000/hi/auth",
                        "ingress.kubernetes.io/auth-singin": "https://console.deepvega.com/hi/login",
                        "ingress.kubernetes.io/auth-response-headers": "X-Auth-User, X-Secret",
                    },
                ),
                spec=kube_client.V1beta1IngressSpec(
                    rules=[
                        # kube_client.V1beta1IngressRule(
                        #     host=f"{hashed_username}.drone.deepvega.com",
                        #     http=kube_client.V1beta1HTTPIngressRuleValue(
                        #         paths=[
                        #             kube_client.V1beta1HTTPIngressPath(
                        #                 path="/",
                        #                 backend=kube_client.V1beta1IngressBackend(
                        #                     service_name=f"drone", service_port=80
                        #                 ),
                        #             )
                        #         ]
                        #     ),
                        # ),
                        # kube_client.V1beta1IngressRule(
                        #     host=f"{hashed_username}.mlflow.deepvega.com",
                        #     http=kube_client.V1beta1HTTPIngressRuleValue(
                        #         paths=[
                        #             kube_client.V1beta1HTTPIngressPath(
                        #                 path="/",
                        #                 backend=kube_client.V1beta1IngressBackend(
                        #                     service_name=f"mlflow", service_port=5000
                        #                 ),
                        #             )
                        #         ]
                        #     ),
                        # ),
                        kube_client.V1beta1IngressRule(
                            host=f"{hashed_username}.zeppelin.deepvega.com",
                            http=kube_client.V1beta1HTTPIngressRuleValue(
                                paths=[
                                    kube_client.V1beta1HTTPIngressPath(
                                        path="/",
                                        backend=kube_client.V1beta1IngressBackend(
                                            service_name=f"spark-{hashed_username}-zeppelin",
                                            service_port=8080,
                                        ),
                                    )
                                ]
                            ),
                        ),
                        kube_client.V1beta1IngressRule(
                            host=f"{hashed_username}.spark-ui.deepvega.com",
                            http=kube_client.V1beta1HTTPIngressRuleValue(
                                paths=[
                                    kube_client.V1beta1HTTPIngressPath(
                                        path="/",
                                        backend=kube_client.V1beta1IngressBackend(
                                            service_name=f"spark-{hashed_username}-webui",
                                            service_port=8080,
                                        ),
                                    )
                                ]
                            ),
                        ),
                    ]
                ),
            ),
        )
        return ret

    def create_deployment_namespaced(self, hashed_username):
        ret = self.k_client_ext_v1_beta1.create_namespaced_deployment(
            namespace=f"ns-{hashed_username}",
            body=kube_client.ExtensionsV1beta1Deployment(
                api_version="extensions/v1beta1",
                kind="Deployment",
                metadata=kube_client.V1ObjectMeta(
                    name=f"traefik-ingress-controller",
                    namespace=f"ns-{hashed_username}",
                    labels={"k8s-app": "traefik-ingress-controller"},
                ),
                spec=kube_client.ExtensionsV1beta1DeploymentSpec(
                    replicas=1,
                    selector=kube_client.V1LabelSelector(
                        match_labels={"k8s-app": "traefik-ingress-controller"}
                    ),
                    template=kube_client.V1PodTemplateSpec(
                        metadata=kube_client.V1ObjectMeta(
                            name=f"traefik-ingress-controller",
                            labels={"k8s-app": "traefik-ingress-controller"},
                        ),
                        spec=kube_client.V1PodSpec(
                            service_account_name="traefik-ingress-serviceaccount",
                            containers=[
                                kube_client.V1Container(
                                    image="traefik",
                                    name="traefik-ingress-controller",
                                    image_pull_policy="Always",
                                    resources=kube_client.V1ResourceRequirements(
                                        limits={"cpu": "200m", "memory": "384Mi"},
                                        requests={"cpu": "25m", "memory": "128Mi"},
                                    ),
                                    liveness_probe=kube_client.V1Probe(
                                        failure_threshold=2,
                                        http_get=kube_client.V1HTTPGetAction(
                                            path="/ping", port=80, scheme="HTTP"
                                        ),
                                        initial_delay_seconds=5,
                                        period_seconds=4,
                                    ),
                                    readiness_probe=kube_client.V1Probe(
                                        failure_threshold=2,
                                        http_get=kube_client.V1HTTPGetAction(
                                            path="/ping", port=80, scheme="HTTP"
                                        ),
                                        period_seconds=4,
                                    ),
                                    ports=[
                                        kube_client.V1ContainerPort(
                                            name="http", container_port=80
                                        ),
                                        kube_client.V1ContainerPort(
                                            name="https", container_port=443
                                        ),
                                    ],
                                    args=[
                                        "--logLevel=INFO",
                                        "--configfile=/config/traefik.toml",
                                    ],
                                    volume_mounts=[
                                        kube_client.V1VolumeMount(
                                            mount_path="/ssl/ui",
                                            name="traefik-ui-tls-cert",
                                        ),
                                        kube_client.V1VolumeMount(
                                            mount_path="/ssl/drone",
                                            name="traefik-drone-tls-cert",
                                        ),
                                        kube_client.V1VolumeMount(
                                            mount_path="/config",
                                            name="traefik-ingress-configmap",
                                        ),
                                    ],
                                )
                            ],
                            volumes=[
                                kube_client.V1Volume(
                                    name="traefik-ui-tls-cert",
                                    secret=kube_client.V1SecretVolumeSource(
                                        secret_name="traefik-ui-tls-cert"
                                    ),
                                ),
                                kube_client.V1Volume(
                                    name="traefik-drone-tls-cert",
                                    secret=kube_client.V1SecretVolumeSource(
                                        secret_name="traefik-drone-tls-cert"
                                    ),
                                ),
                                kube_client.V1Volume(
                                    name="traefik-ingress-configmap",
                                    config_map=kube_client.V1ConfigMapVolumeSource(
                                        name="traefik-ingress-configmap"
                                    ),
                                ),
                            ],
                        ),
                    ),
                ),
            ),
        )
        return ret


""" The right order to execute and func to bootstrap a newly registered user is as following
"""
# a = K8SClientUserInit()
# a.bootstrap_new_user("tony")
