from django.utils.deprecation import MiddlewareMixin
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException

from core.exceptions import ClientException


class BusinessExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        if isinstance(exception, ClientException):
            return JsonResponse(data={'message': exception.message, 'code': 400}, status=status.HTTP_400_BAD_REQUEST)

