# -*- coding: UTF-8 -*-
import re
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from symcon import forms, models


class IndexView(ListView):
    template_name = 'symcon/index.html'
    context_object_name = 'data'
    paginate_by = 20

    def get_queryset(self):
        queryset = models.Library.objects.last_updated()
        if 'search' in self.request.GET:
            queryset = queryset.search(self.request.GET.get('search'))

        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(dict(library_count=models.Library.objects.all().count()))
        return ctx


class LibraryView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        library = get_object_or_404(models.Library.objects.all().prefetch_related(
            'librarybranch_set__branch'), uuid=self.kwargs.get('library_id'))
        return reverse_lazy('symcon_library_branch', kwargs=dict(
            library_id=library.uuid, branch=library.get_default_librarybranch().branch.name))


class LibraryBranchView(DetailView):
    model = models.LibraryBranch
    context_object_name = 'item'
    template_name = 'symcon/library/index.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'branch__repository', 'library__repository', 'module_set__modulealias_set',
            'module_set__moduleparentrequirement_set', 'module_set__modulechildrequirement_set',
            'module_set__moduleimplementedrequirement_set', 'librarybranchtag_set')

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        obj = queryset.filter(library__uuid=self.kwargs.get('library_id'),
                              branch__name=self.kwargs.get('branch')).first()
        if not obj:
            raise Http404('object not found')
        return obj


class LibrarySubmitView(FormView):
    template_name = 'symcon/library/submit.html'
    form_class = forms.SubmitForm
    success_url = reverse_lazy('symcon_index')

    def form_valid(self, form):
        response = super().form_valid(form)

        url = form.cleaned_data.get('repository_url')
        matches = re.match(r'https://github.com/([^/]+)/([^/]+)/?', url)
        if not matches:
            messages.error(self.request, _('Could not parse GitHub URL'))
            return response
        user, name = matches.groups()

        # remove .git from name
        if name.endswith('.git'):
            name = name.replace('.git', '')

        # issue update task
        from symcon.tasks import symcon_update_repository
        symcon_update_repository.apply_async([user, name])
        messages.success(self.request, _('Thanks! Your submission will be processed soon'))

        return response
