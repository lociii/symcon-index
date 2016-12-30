# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from symcon import models


@admin.register(models.Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name']
    search_fields = ['user', 'name']


@admin.register(models.Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['id', 'uuid', 'name', 'author', 'url']
    search_fields = ['uuid', 'name', 'author', 'url']


@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'uuid', 'name', 'get_library_name', 'type', 'vendor']
    search_fields = ['uuid', 'name', 'vendor', 'library__name']
    list_filter = ['type']

    def get_library_name(self, obj):
        return obj.library.name
    get_library_name.short_description = _('Library')


@admin.register(models.ModuleAlias)
class ModuleAliasAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    readonly_fields = ['deleted']
    search_fields = ['name']

    def get_module_name(self, obj):
        return obj.module.name
    get_module_name.short_description = _('Module')


@admin.register(models.ModuleParentRequirement)
@admin.register(models.ModuleChildRequirement)
@admin.register(models.ModuleImplementedRequirement)
class ModuleRequirementAdmin(admin.ModelAdmin):
    list_display = ['id', 'uuid']
    readonly_fields = ['deleted']
    search_fields = ['uuid']

    def get_module_name(self, obj):
        return obj.module.name
    get_module_name.short_description = _('Module')
