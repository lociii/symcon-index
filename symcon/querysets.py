from django.db import models
from django.db.models.query_utils import Q


class ModuleQuerySet(models.QuerySet):
    def last_updated(self):
        return self.prefetch_related('library__repository').order_by(
            '-library__repository__last_update', 'library__name', 'name')

    def search(self, search_term):
        return self.filter(Q(name__icontains=search_term) | Q(library__name__icontains=search_term))
