from django.core.cache import cache


class MyNotesCache:
    cache_timeout = 120
    cache_key_prefix = 'reservation-notes-cache'
    max_page = 10

    def __init__(self, request):
        self.request = request
        self.__page = self._get_page()
        self.is_cached = self.__page is not None and (0 < self.__page <= self.max_page) and not self._has_other_params()

    @classmethod
    def clear_cache(cls):
        for i in range(1, cls.max_page + 1):
            cache.delete(f'{cls.cache_key_prefix}-{i}')

    def get_page(self):
        return cache.get(self._get_current_prefix())

    def set_page(self, data):
        return cache.set(self._get_current_prefix(), value=data, timeout=self.cache_timeout)

    def _get_current_prefix(self):
        return f'{self.cache_key_prefix}-{self.__page}'

    def _has_other_params(self):
        return bool([param for param in self.request.query_params if param != "page"])

    def _get_page(self):
        try:
            page = int(self.request.GET.get('page', 1))
            return page
        except ValueError:
            return None
