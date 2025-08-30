from rest_framework.pagination import PageNumberPagination, CursorPagination


class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'


class DefaultCursorPagination(CursorPagination):
    page_size = 5      # как в settings
    ordering = '-id'