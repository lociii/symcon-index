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
    last_update = models.DateTimeField(null=True, blank=True, verbose_name=_('Last update'))

    def get_url(self):
        return '{owner_url}/{name}'.format(owner_url=self.get_owner_url(), name=self.name)

    def get_issue_url(self):
        return '{repo}/issues'.format(repo=self.get_url())

    def get_owner_url(self):
        return 'https://github.com/{user}'.format(user=self.user)

    class Meta:
        verbose_name = _('Repository')
        verbose_name_plural = _('Repositories')
        unique_together = ('user', 'name')


class Branch(models.Model):
    repository = models.ForeignKey(to='Repository', verbose_name=_('Repository'))
    name = models.CharField(max_length=200, verbose_name=_('Branch'))
    last_update = models.DateTimeField(null=True, blank=True, verbose_name=_('Last update'))
    default = models.BooleanField(default=False, verbose_name=_('Default'))

    def get_raw_url(self):
        return self.repository.get_url() + '/raw/' + self.name

    class Meta:
        verbose_name = _('Branch')
        verbose_name_plural = _('Branches')
        unique_together = ('repository', 'name')


class Library(models.Model):
    objects = querysets.LibraryQuerySet.as_manager()

    repository = models.ForeignKey(to='Repository', verbose_name=_('Repository'))
    uuid = models.UUIDField(verbose_name=_('Identifier'))

    def get_default_librarybranch(self):
        for librarybranch in self.librarybranch_set.all():
            if librarybranch.branch.default:
                return librarybranch
        return None

    class Meta:
        verbose_name = _('Library')
        verbose_name_plural = _('Libraries')
        unique_together = ('repository', 'uuid')


class LibraryBranch(models.Model):
    library = models.ForeignKey(to='Library', verbose_name=_('Library'))
    branch = models.ForeignKey(to='Branch', verbose_name=_('Branch'))
    name = models.CharField(max_length=200, blank=True, verbose_name=_('Name'))
    title = models.TextField(blank=True, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    req_ips_version = models.CharField(max_length=200, blank=True,
                                       verbose_name=_('Minimum Symcon version'))
    author = models.CharField(max_length=200, blank=True, verbose_name=_('Author'))
    url = models.URLField(blank=True, verbose_name=_('URL'))
    version = models.CharField(max_length=50, blank=True, verbose_name=_('Version'))
    build = models.IntegerField(null=True, blank=True, verbose_name=_('Build'))
    date = models.IntegerField(null=True, blank=True, verbose_name=_('Date'))
    readme_markdown = models.TextField(blank=True, verbose_name=_('Readme MarkDown'))
    readme_html = models.TextField(blank=True, verbose_name=_('Readme HTML'))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.convert_readme()
        super().save(force_insert, force_update, using, update_fields)

    def convert_readme(self):
        self.readme_html = MarkDownToHtml(
            text=self.readme_markdown, branch=self.branch).transform()

    def get_min_version(self):
        if self.min_version:
            return self.min_version
        return self.branch.name

    class Meta:
        verbose_name = _('Library branch')
        verbose_name_plural = _('Library branches')
        unique_together = ('library', 'branch')
        ordering = ('-branch__default', 'name')


class LibraryBranchTag(models.Model):
    librarybranch = models.ForeignKey(to='LibraryBranch', verbose_name=_('Library branch'))
    name = models.CharField(max_length=200, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Library branch tag')
        verbose_name_plural = _('Library branche tags')
        unique_together = ('librarybranch', 'name')
        ordering = ('librarybranch', 'name')


class Module(models.Model):
    TYPE_CHOICES = Choices(
        (0, 'core', _('Core')),
        (1, 'io', _('I/O')),
        (2, 'splitter', _('Splitter')),
        (3, 'device', _('Device')),
        (4, 'configurator', _('Configurator')),
    )

    librarybranch = models.ForeignKey(to='LibraryBranch', verbose_name=_('Library branch'))
    uuid = models.UUIDField(verbose_name=_('Identifier'))
    name = models.CharField(max_length=200, blank=True, verbose_name=_('Name'))
    title = models.TextField(blank=True, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    type = models.IntegerField(choices=TYPE_CHOICES, null=True, blank=True, verbose_name=_('Type'))
    vendor = models.CharField(max_length=200, blank=True, verbose_name=_('Vendor'))
    prefix = models.CharField(max_length=200, blank=True, verbose_name=_('Prefix'))
    readme_markdown = models.TextField(blank=True, verbose_name=_('Readme MarkDown'))
    readme_html = models.TextField(blank=True, verbose_name=_('Readme HTML'))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.convert_readme()
        super().save(force_insert, force_update, using, update_fields)

    def convert_readme(self):
        self.readme_html = MarkDownToHtml(
            text=self.readme_markdown, branch=self.librarybranch.branch).transform()

    class Meta:
        verbose_name = _('Module')
        verbose_name_plural = _('Modules')
        unique_together = ('librarybranch', 'uuid')


class ModuleAlias(models.Model):
    module = models.ForeignKey(to='Module', verbose_name=_('Module'))
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    deleted = models.BooleanField(default=False, verbose_name=_('Marked for deletion'))

    class Meta:
        verbose_name = _('Module alias')
        verbose_name_plural = _('Module aliases')
        unique_together = ('module', 'name')


class ModuleParentRequirement(models.Model):
    module = models.ForeignKey(to='Module', verbose_name=_('Module'))
    uuid = models.UUIDField(verbose_name=_('Identifier'))
    deleted = models.BooleanField(default=False, verbose_name=_('Marked for deletion'))

    class Meta:
        verbose_name = _('Module parent requirement')
        verbose_name_plural = _('Module parent requirements')
        unique_together = ('module', 'uuid')


class ModuleChildRequirement(models.Model):
    module = models.ForeignKey(to='Module', verbose_name=_('Module'))
    uuid = models.UUIDField(verbose_name=_('Identifier'))
    deleted = models.BooleanField(default=False, verbose_name=_('Marked for deletion'))

    class Meta:
        verbose_name = _('Module child requirement')
        verbose_name_plural = _('Module child requirements')
        unique_together = ('module', 'uuid')


class ModuleImplementedRequirement(models.Model):
    module = models.ForeignKey(to='Module', verbose_name=_('Module'))
    uuid = models.UUIDField(verbose_name=_('Identifier'))
    deleted = models.BooleanField(default=False, verbose_name=_('Marked for deletion'))

    class Meta:
        verbose_name = _('Module implemented requirement')
        verbose_name_plural = _('Module implemented requirements')
        unique_together = ('module', 'uuid')
