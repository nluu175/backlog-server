from rest_framework.pagination import PageNumberPagination


class BacklogPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = "size"
    max_page_size = 100


class GamePagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = "size"
    max_page_size = 100
