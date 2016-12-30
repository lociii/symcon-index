# -*- coding: UTF-8 -*-
import json
import pytz

from github import Github, GithubException
from django.conf import settings

from symcon import models


class SymconException(Exception):
    pass


class SymconLibrary(object):
    def __init__(self, uuid):
        self.uuid = uuid
        self.author = ''
        self.name = ''
        self.title = ''
        self.description = ''
        self.url = ''
        self.version = ''
        self.build = None
        self.date = None

    def validate(self):
        if not self.author:
            raise SymconException('library has no author')
        if not self.name:
            raise SymconException('library has no name')


class SymconModule(object):
    def __init__(self, uuid):
        self.uuid = uuid
        self.name = ''
        self.title = ''
        self.description = ''
        self.type = None
        self.vendor = ''
        self.aliases = list()
        self.parent_requirements = list()
        self.child_requirements = list()
        self.implemented_requiremens = list()
        self.prefix = ''
        self.readme = ''

    def add_alias(self, name):
        self.aliases.append(name)

    def add_parent_requirement(self, name):
        self.parent_requirements.append(name)

    def add_child_requirement(self, name):
        self.child_requirements.append(name)

    def add_implemented_requiremen(self, name):
        self.implemented_requiremens.append(name)

    def validate(self):
        if not self.name:
            raise SymconException('module has no name')
        if not self.type:
            raise SymconException('module has no type')


class SymconRepository(object):
    def __init__(self, user, name):
        self.user = user
        self.name = name
        self.last_update = None
        self.library = None
        self.modules = list()
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = Github(login_or_token=settings.GITHUB_API_USER,
                                  password=settings.GITHUB_API_TOKEN)
        return self._client

    def parse(self):
        # get repo
        url = '{user}/{repo}'.format(user=self.user, repo=self.name)
        try:
            repo = self.client.get_repo(url)
        except GithubException:
            raise SymconException('failed to open repository')

        # set last update
        self.last_update = pytz.utc.localize(repo.pushed_at)

        # get repo contents
        try:
            contents = repo.get_contents('/')
        except GithubException:
            raise SymconException('failed to get repository root contents')

        # handle repo contents
        for item in contents:
            if item.type == 'dir':
                self._check_subdirectory(repo, item.path)
            elif item.type == 'file' and item.path == 'library.json':
                self._handle_library_json(item.decoded_content)

    def _handle_library_json(self, json_string):
        try:
            definition = json.loads(json_string.decode('UTF-8'))
        except:
            raise SymconException('failed to parse library definition')

        if 'id' not in definition:
            raise SymconException('library definition has no id')

        library = SymconLibrary(uuid=definition['id'])
        if 'author' in definition:
            library.author = definition['author']
        if 'name' in definition:
            library.name = definition['name']
        if 'title' in definition:
            library.title = definition['title']
        if 'description' in definition:
            library.description = definition['description']
        if 'url' in definition:
            library.url = definition['url']
        if 'version' in definition:
            library.version = definition['version']
        if 'build' in definition:
            library.build = definition['build']
        if 'date' in definition:
            library.date = definition['date']

        self._set_library(library=library)

    def _check_subdirectory(self, repo, directory):
        try:
            contents = repo.get_contents('/{dir}'.format(dir=directory))
        except GithubException:
            raise SymconException('failed to get repository root contents')

        definition = None
        readme = None

        for item in contents:
            if item.type == 'file' and item.path == '{dir}/module.json'.format(dir=directory):
                definition = item.decoded_content.decode('UTF-8')
            elif item.type == 'file' and item.path.lower() == '{dir}/readme.md'.format(
                    dir=directory.lower()):
                readme = item.decoded_content.decode('UTF-8')

        if definition and readme:
            try:
                definition = json.loads(definition)
            except:
                raise SymconException('failed to parse module definition')

            if 'id' not in definition:
                raise SymconException('module definition has no id')

            module = SymconModule(uuid=definition['id'])
            if 'name' in definition:
                module.name = definition['name']
            if 'title' in definition:
                module.title = definition['title']
            if 'description' in definition:
                module.description = definition['description']
            if 'type' in definition:
                module.type = definition['type']
            if 'vendor' in definition:
                module.vendor = definition['vendor']
            if 'aliases' in definition:
                for name in definition['aliases']:
                    module.add_alias(name)
            if 'parentRequirements' in definition:
                for name in definition['parentRequirements']:
                    module.add_parent_requirement(name)
            if 'childRequirements' in definition:
                for name in definition['childRequirements']:
                    module.add_child_requirement(name)
            if 'implemented' in definition:
                for name in definition['implemented']:
                    module.add_implemented_requiremen(name)
            if 'prefix' in definition:
                module.prefix = definition['prefix']
            if readme:
                module.readme = readme

            self._add_module(module=module)

    def _set_library(self, library):
        assert isinstance(library, SymconLibrary)
        self.library = library

    def _add_module(self, module):
        assert isinstance(module, SymconModule)
        self.modules.append(module)

    def validate(self):
        self.library.validate()
        for module in self.modules:
            module.validate()

    def save(self):
        self.validate()
        repository, created = models.Repository.objects.update_or_create(
            user=self.user, name=self.name, defaults=dict(last_update=self.last_update))

        library, created = models.Library.objects.update_or_create(
            repository=repository, uuid=self.library.uuid, defaults=dict(
                name=self.library.name, title=self.library.title,
                description=self.library.description, author=self.library.author,
                url=self.library.url, version=self.library.version, build=self.library.build,
                date=self.library.build))

        for symcon_module in self.modules:
            module, created = models.Module.objects.update_or_create(
                library=library, uuid=symcon_module.uuid, defaults=dict(
                    name=symcon_module.name, title=symcon_module.title,
                    description=symcon_module.description, type=symcon_module.type,
                    vendor=symcon_module.vendor, prefix=symcon_module.prefix,
                    readme_markdown=symcon_module.readme))

            module.modulealias_set.all().update(deleted=True)
            for name in symcon_module.aliases:
                models.ModuleAlias.objects.update_or_create(
                    module=module, name=name, defaults=dict(deleted=False))

            module.moduleparentrequirement_set.all().update(deleted=True)
            for name in symcon_module.parent_requirements:
                models.ModuleParentRequirement.objects.update_or_create(
                    module=module, name=name, defaults=dict(deleted=False))

            module.modulechildrequirement_set.all().update(deleted=True)
            for name in symcon_module.child_requirements:
                models.ModuleChildRequirement.objects.update_or_create(
                    module=module, name=name, defaults=dict(deleted=False))

            module.moduleimplementedrequirement_set.all().update(deleted=True)
            for name in symcon_module.implemented_requiremens:
                models.ModuleImplementedRequirement.objects.update_or_create(
                    module=module, name=name, defaults=dict(deleted=False))
