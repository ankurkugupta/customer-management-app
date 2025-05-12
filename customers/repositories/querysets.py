from django.db.models import QuerySet


class CustomerQuerySet(QuerySet):
    def available(self):
        return self.filter(deleted_at=None)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)

