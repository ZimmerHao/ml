from rest_framework import pagination
from rest_framework.response import Response


class WavePagination(pagination.PageNumberPagination):

    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'count': self.page.paginator.count,
            'has_next': self.page.paginator.num_pages > self.page.number,
            'results': data
        })
