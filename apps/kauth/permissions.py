from rest_framework.permissions import BasePermission


class KPermission(BasePermission):
    pass


class NamespaceAllow(KPermission):

    def has_permission(self, request, view):
        user = request.user
        ns = request.query_params.get("ns")
        role = user.k8s_roles.filter(namespace=ns).first()
        return True if role else False
