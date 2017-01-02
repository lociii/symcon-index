# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from symcon import models


@admin.register(models.Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'last_update']
    search_fields = ['user', 'name']


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_repository', 'name', 'default', 'last_update']
    search_fields = ['name']

    def get_repository(self, obj):
        return '{user}/{name}'.format(user=obj.repository.user, name=obj.repository.name)
    get_repository.short_description = _('Repository')


@admin.register(models.Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_repository', 'uuid']
    search_fields = ['uuid']

    def get_repository(self, obj):
        return '{user}/{name}'.format(user=obj.repository.user, name=obj.repository.name)
    get_repository.short_description = _('Repository')


@admin.register(models.LibraryBranch)
class LibraryBranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_branch', 'get_library', 'name', 'title', 'author']
    search_fields = ['name', 'title', 'author', 'description', 'library__uuid', 'branch__name',
                     'branch__repository__user', 'branch_repository__name']

    def get_branch(self, obj):
        return '{user}/{name}:{branch}'.format(
            user=obj.branch.repository.user, name=obj.branch.repository.name,
            branch=obj.branch.name)
    get_branch.short_description = _('Branch')

    def get_library(self, obj):
        return obj.library.uuid
    get_library.short_description = _('Library')


@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_librarybranch', 'uuid', 'name', 'type', 'vendor']
    search_fields = ['uuid', 'name', 'vendor', 'librarybranch__name']
    list_filter = ['type']

    def get_librarybranch(self, obj):
        return obj.librarybranch.name
    get_librarybranch.short_description = _('Library')


@admin.register(models.ModuleAlias)
class ModuleAliasAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_module', 'name']
    readonly_fields = ['deleted']
    search_fields = ['name']

    def get_module(self, obj):
        return '{lib}/{mod}'.format(lib=obj.module.librarybranch.name, mod=obj.module.name)
    get_module.short_description = _('Module')


@admin.register(models.ModuleParentRequirement)
@admin.register(models.ModuleChildRequirement)
@admin.register(models.ModuleImplementedRequirement)
class ModuleRequirementAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_module', 'uuid']
    readonly_fields = ['deleted']
    search_fields = ['uuid']

    def get_module(self, obj):
        return '{lib}/{mod}'.format(lib=obj.module.librarybranch.name, mod=obj.module.name)
    get_module.short_description = _('Module')
