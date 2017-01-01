# -*- coding: UTF-8 -*-
import markdown
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.choices import Choices

from symcon import querysets
from symcon.common.util.markdown import MarkDownToHtml


class Repository(models.Model):
    user = models.CharField(max_length=100, verbose_name=_('User'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    last_update = models.DateTimeField(verbose_name=_('Last update'))

    def get_url(self):
        return '{owner_url}/{name}'.format(owner_url=self.get_owner_url(), name=self.name)

    def get_issue_url(self):
        return '{repo}/issues'.format(repo=self.get_url())

    def get_owner_url(self):
        return 'https://github.com/{user}'.format(user=self.user)

    def get_raw_url(self, branch='master'):
        return self.get_url() + '/raw/' + branch

    class Meta:
        verbose_name = _('Repository')
        verbose_name_plural = _('Repositories')
        unique_together = ('user', 'name')


class Library(models.Model):
    repository = models.ForeignKey(to=Repository, verbose_name=_('Repository'))
    uuid = models.UUIDField(verbose_name=_('Identifier'), unique=True)
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    title = models.TextField(verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    author = models.CharField(max_length=200, verbose_name=_('Author'))
    url = models.URLField(verbose_name=_('URL'))
    version = models.CharField(max_length=50, verbose_name=_('Version'))
    build = models.IntegerField(verbose_name=_('Build'))
    date = models.IntegerField(verbose_name=_('Date'))
    readme_markdown = models.TextField(verbose_name=_('Readme MarkDown'))
    readme_html = models.TextField(verbose_name=_('Readme HTML'))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.convert_readme()
        super().save(force_insert, force_update, using, update_fields)

    def convert_readme(self):
        self.readme_html = MarkDownToHtml(
            text=self.readme_markdown, repository=self.repository).transform()

    class Meta:
        verbose_name = _('Library')
        verbose_name_plural = _('Libraries')
        unique_together = ('repository', 'uuid')


class Module(models.Model):
    objects = querysets.ModuleQuerySet.as_manager()

    TYPE_CHOICES = Choices(
        (0, 'core', _('Core')),
        (1, 'io', _('I/O')),
        (2, 'splitter', _('Splitter')),
        (3, 'device', _('Device')),
        (4, 'configurator', _('Configurator')),
    )

    library = models.ForeignKey(to=Library, verbose_name=_('Library'))
    uuid = models.UUIDField(verbose_name=_('Identifier'), unique=True)
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    title = models.TextField(verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name=_('Type'))
    vendor = models.CharField(max_length=200, verbose_name=_('Vendor'))
    prefix = models.CharField(max_length=200, verbose_name=_('Prefix'))
    readme_markdown = models.TextField(verbose_name=_('Readme MarkDown'))
    readme_html = models.TextField(verbose_name=_('Readme HTML'))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.convert_readme()
        super().save(force_insert, force_update, using, update_fields)

    def convert_readme(self):
        self.readme_html = MarkDownToHtml(
            text=self.readme_markdown, repository=self.library.repository).transform()

    class Meta:
        verbose_name = _('Module')
        verbose_name_plural = _('Modules')
        unique_together = ('library', 'uuid')


class ModuleAlias(models.Model):
    module = models.ForeignKey(to=Module, verbose_name=_('Module'))
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    deleted = models.BooleanField(default=False, verbose_name=_('Marked for deletion'))

    class Meta:
        verbose_name = _('Module alias')
        verbose_name_plural = _('Module aliases')
        unique_together = ('module', 'name')


class ModuleParentRequirement(models.Model):
    module = models.ForeignKey(to=Module, verbose_name=_('Module'))
    uuid = models.UUIDField(verbose_name=_('Identifier'))
    deleted = models.BooleanField(default=False, verbose_name=_('Marked for deletion'))

    class Meta:
        verbose_name = _('Module parent requirement')
        verbose_name_plural = _('Module parent requirements')
        unique_together = ('module', 'uuid')


class ModuleChildRequirement(models.Model):
    module = models.ForeignKey(to=Module, verbose_name=_('Module'))
    uuid = models.UUIDField(verbose_name=_('Identifier'))
    deleted = models.BooleanField(default=False, verbose_name=_('Marked for deletion'))

    class Meta:
        verbose_name = _('Module child requirement')
        verbose_name_plural = _('Module child requirements')
        unique_together = ('module', 'uuid')


class ModuleImplementedRequirement(models.Model):
    module = models.ForeignKey(to=Module, verbose_name=_('Module'))
    uuid = models.UUIDField(verbose_name=_('Identifier'))
    deleted = models.BooleanField(default=False, verbose_name=_('Marked for deletion'))

    class Meta:
        verbose_name = _('Module implemented requirement')
        verbose_name_plural = _('Module implemented requirements')
        unique_together = ('module', 'uuid')
