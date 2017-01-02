# -*- coding: UTF-8 -*-
from django.db import models
from django.db.models.query_utils import Q


class LibraryQuerySet(models.QuerySet):
    def last_updated(self):
        return self.order_by('-repository__last_update')

    def search(self, search_term):
        return self.prefetch_related(
            'repository', 'librarybranch_set__branch',
            'librarybranch_set__module_set__modulealias_set',
            'librarybranch_set__module_set__moduleparentrequirement_set',
            'librarybranch_set__module_set__modulechildrequirement_set',
            'librarybranch_set__module_set__moduleimplementedrequirement_set').filter(
            Q(librarybranch__name__icontains=search_term) |
            Q(librarybranch__module__name__icontains=search_term) |
            Q(librarybranch__title__icontains=search_term) |
            Q(librarybranch__module__title__icontains=search_term) |
            Q(librarybranch__description__icontains=search_term) |
            Q(librarybranch__module__description__icontains=search_term) |
            Q(librarybranch__librarybranchtag__name__icontains=search_term)).distinct()
