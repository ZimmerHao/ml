from libs.kubernetes.client import K8SClient

K = K8SClient()

# def test_get_pods_namespaced():
#     exp = ""
#     act = K.get_resources_namespaced("po")
#     print([i.metadata.name for i in act.items])
#     assert exp == act
#
# def test_get_logs():
#     exp=""
#     act = K.get_logs("trx-customer-transactions-listeners-input-77d8b9496f-fvqmg")
#     print(act)
#     assert exp == act

def test_apply_sparkapp_yaml_file():
    act = K.apply_sparkapp_yaml_file("https://raw.githubusercontent.com/GoogleCloudPlatform/spark-on-k8s-operator/master/examples/spark-pi.yaml")
    exp = "SparkApp spark-pi created"
    assert exp == act

def test_delete_sparkapp_yaml_file():
    act = K.delete_sparkapp_yaml_file("https://raw.githubusercontent.com/GoogleCloudPlatform/spark-on-k8s-operator/master/examples/spark-pi.yaml")
    exp = "SparkApp spark-pi deleted"
    assert exp == act