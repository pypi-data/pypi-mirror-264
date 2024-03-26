from django.db.models import QuerySet


def queryset_iterator(queryset: QuerySet, chunk_size: int = 1000):
    total = queryset.count()
    for start in range(0, total, chunk_size):
        end = min(start + chunk_size, total)
        yield queryset[start:end], start, end
