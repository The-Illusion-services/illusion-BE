from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  # Default page size
    page_size_query_param = 'page_size'  # Allow custom page size
    max_page_size = 100  # Prevent too large page sizes

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Total items
            'total_pages': self.page.paginator.num_pages,  # Total pages
            'current_page': self.page.number,  # Current page
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,  # Paginated data
        })
