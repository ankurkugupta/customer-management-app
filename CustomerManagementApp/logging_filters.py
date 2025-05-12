import logging

class RequestIDFilter(logging.Filter):
    def filter(self, record):
        from threading import current_thread
        request = getattr(current_thread(), 'request', None)
        record.request_id = getattr(request, 'request_id', 'N/A')
        return True
