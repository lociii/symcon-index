# -*- coding: UTF-8 -*-
import re
from django.contrib import messages
from django.http.response import Http404
from django.urls.base import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from symcon import forms, models
from symcon.common.util.symcon import SymconRepository


class IndexView(ListView):
    template_name = 'symcon/index.html'
    context_object_name = 'data'
    paginate_by = 20

    def get_queryset(self):
        queryset = models.Module.objects.last_updated()
        if 'search' in self.request.GET:
            queryset = queryset.search(self.request.GET.get('search'))

        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(dict(library_count=models.Library.objects.all().count(),
                        module_count=models.Module.objects.all().count()))
        return ctx


class LibraryModuleView(DetailView):
    model = models.Module
    context_object_name = 'item'
    template_name = 'symcon/library/module/index.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if 'module_id' not in self.kwargs:
            raise Http404('Dataset not found')

        return queryset.get(uuid=self.kwargs.get('module_id'))


class LibraryView(DetailView):
    model = models.Library
    context_object_name = 'item'
    template_name = 'symcon/library/index.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        if 'library_id' not in self.kwargs:
            raise Http404('Dataset not found')

        return queryset.get(uuid=self.kwargs.get('library_id'))


class LibrarySubmitView(FormView):
    template_name = 'symcon/submit.html'
    form_class = forms.SubmitForm
    success_url = reverse_lazy('symcon_index')

    def form_valid(self, form):
        url = form.cleaned_data.get('repository_url')
        matches = re.match(r'https://github.com/([^/]+)/([^/]+)/?', url)
        if not matches:
            messages.error(self.request, _('Could not parse GitHub URL'))
            return super().form_valid(form)

        user, name = matches.groups()
        try:
            symconrepo = SymconRepository(user=user, name=name)
            symconrepo.parse()
            symconrepo.save()
            messages.success(self.request, _('Library added successfully'))
        except Exception as e:
            messages.error(self.request, str(e))

        return super().form_valid(form)

