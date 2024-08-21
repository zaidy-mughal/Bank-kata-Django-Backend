from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNubmerPagination(PageNumberPagination):
    """
    this is used to get Customized Pagination Response According to the requirements
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        """
        Override this method to get Custom Response
        """

        return Response({
            'count':self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'first': self.get_first_link(),
            'last': self.get_last_link(),
            'results': data,
        })
    
    def _get_link(self,page_number):
        request = self.request
        url = self.request.build_absolute_uri()
        query_params = request.query_params.copy()
        query_params['page'] = page_number
        return f"{url}?{query_params.urlencode()}"
    
    def get_first_link(self):
        if self.page.number > 1:
            return self._get_link(1)
        return None

    def get_last_link(self):
        if self.page.number < self.page.paginator.num_pages:
            return self._get_link(self.page.paginator.num_pages)
        return None