from rest_framework.pagination import PageNumberPagination

class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'