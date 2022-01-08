from rest_framework.pagination import PageNumberPagination


class WatchlistPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param  = 'size'
    max_page_size = 10
    last_page_strings  = 'end'