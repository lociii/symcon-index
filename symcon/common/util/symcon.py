# -*- coding: UTF-8 -*-
import json
import logging
from uuid import UUID
from urllib.parse import quote

import pytz

from github import Github, GithubException
from django.conf import settings
from github.GithubException import UnknownObjectException

from symcon import models, tasks

logger = logging.getLogger(__name__)


class SymconRepositoryHandler(object):
    def __init__(self):
        super().__init__()
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = Github(login_or_token=settings.GITHUB_API_USER,
                                  password=settings.GITHUB_API_TOKEN)
        return self._client

    def update_repository(self, user, name):
        # get repository from github
        try:
            repo = self.client.get_repo('{user}/{name}'.format(user=user, name=name), lazy=False)
        except UnknownObjectException:
            # repository wasn't found on github, let's delete it
            models.Repository.objects.filter(user=user, name=name).delete()
            return
        except GithubException as e:
            logger.exception(e)
            return

        # get the database model
        repository, created = models.Repository.objects.update_or_create(
            user=user, name=name, defaults=dict(last_update=pytz.utc.localize(repo.pushed_at)))

        # get all branches
        try:
            branches = repo.get_branches()
        except GithubException as e:
            logger.exception(e)
            return

        # index every branch
        for branch_data in branches:
            default = branch_data.name == repo.default_branch
            branch, created = models.Branch.objects.update_or_create(
                repository=repository, name=branch_data.name, defaults=dict(default=default))
            tasks.symcon_update_branch.apply_async([branch.pk])

    def update_branch(self, branch_id):
        # load branch
        branch = models.Branch.objects.filter(pk=branch_id).prefetch_related('repository').first()
        if not branch:
            return

        # get repository
        try:
            repo = self.client.get_repo('{user}/{name}'.format(
                user=branch.repository.user, name=branch.repository.name), lazy=False)
        except GithubException as e:
            logger.exception(e)
            return

        # get branch contents
        try:
            contents = repo.get_contents('/', ref=branch.name)
        except GithubException as e:
            logger.exception(e)
            return

        # handle repo contents
        definition = None
        readme = None
        modulepaths = []
        for item in contents:
            if item.type == 'dir':
                modulepaths.append(item.path)
            elif item.type == 'file' and item.path.lower() == 'library.json':
                definition = item.decoded_content.decode('UTF-8')
            elif item.type == 'file' and item.path.lower() == 'readme.md':
                readme = item.decoded_content.decode('UTF-8')

        # no library.json found
        if definition is None:
            logger.exception('no def found')
            return

        # check library.json for validity
        try:
            definition = json.loads(definition)
        except ValueError:
            logger.exception('invalid json')
            return

        # check if the library.json contains a valid library id
        if 'id' not in definition:
            logger.exception('no id in def')
            return
        try:
            library_uuid = UUID(definition['id'], version=4)
        except ValueError:
            logger.exception('invalid uuid')
            return
        if library_uuid.hex == definition['id']:
            logger.exception('uuid does not match')
            return

        # build defaults to update values
        defaults = dict()
        for attribute in ['author', 'name', 'title', 'description', 'url', 'version', 'build',
                          'date', 'req_ips_version']:
            if attribute in definition:
                defaults[attribute] = definition[attribute]
        if readme:
            defaults['readme_markdown'] = readme

        # get library
        library, created = models.Library.objects.get_or_create(
            repository=branch.repository, uuid=definition['id'])

        # create or update library
        librarybranch, created = models.LibraryBranch.objects.update_or_create(
            library=library, branch=branch, defaults=defaults)

        # save tags
        if 'tags' in definition:
            for tag in definition['tags']:
                models.LibraryBranchTag.objects.update_or_create(
                    librarybranch=librarybranch, name=str(tag).strip())

        # issue task for each subdirectory to check for modules
        for modulepath in modulepaths:
            tasks.symcon_update_librarybranch_module.apply_async([librarybranch.pk, modulepath])

    def update_librarybranch_module(self, librarybranch_id, modulepath):
        # load library
        librarybranch = models.LibraryBranch.objects.filter(pk=librarybranch_id).prefetch_related(
            'branch__repository', 'library').first()
        if not librarybranch:
            return

        # get repository
        try:
            repo = self.client.get_repo('{user}/{name}'.format(
                user=librarybranch.branch.repository.user,
                name=librarybranch.branch.repository.name), lazy=False)
        except GithubException as e:
            logger.exception(e)
            return

        # get repository contents in subdirectory
        try:
            contents = repo.get_contents('/{dir}'.format(
                dir=quote(modulepath)), ref=librarybranch.branch.name)
        except GithubException as e:
            logger.exception(e)
            return

        # handle repo contents
        definition = None
        readme = None
        for item in contents:
            if item.type == 'file' and item.path == '{path}/module.json'.format(path=modulepath):
                definition = item.decoded_content.decode('UTF-8')
            elif item.type == 'file' and item.path.lower() == '{path}/readme.md'.format(
                    path=modulepath.lower()):
                readme = item.decoded_content.decode('UTF-8')

        # no module.json found
        if definition is None:
            return

        # check module.json for validity
        try:
            definition = json.loads(definition)
        except ValueError:
            return

        # check if the module.json contains a valid library id
        if 'id' not in definition:
            return
        try:
            module_uuid = UUID(definition['id'], version=4)
        except ValueError:
            return
        if module_uuid.hex == definition['id']:
            return

        # build defaults to update values
        defaults = dict()
        for attribute in ['name', 'title', 'description', 'type', 'vendor']:
            if attribute in definition:
                defaults[attribute] = definition[attribute]
        if readme:
            defaults['readme_markdown'] = readme

        # create or update module
        module, created = models.Module.objects.get_or_create(
            librarybranch=librarybranch, uuid=definition['id'], defaults=defaults)

        # add module aliases
        if 'aliases' in definition:
            module.modulealias_set.all().update(deleted=True)
            for name in definition['aliases']:
                models.ModuleAlias.objects.update_or_create(
                    module=module, name=name, defaults=dict(deleted=False))

        # add module parent requirements
        if 'parentRequirements' in definition:
            module.moduleparentrequirement_set.all().update(deleted=True)
            for uuid in definition['parentRequirements']:
                models.ModuleParentRequirement.objects.update_or_create(
                    module=module, uuid=uuid, defaults=dict(deleted=False))

        # add module child requirements
        if 'childRequirements' in definition:
            module.modulechildrequirement_set.all().update(deleted=True)
            for uuid in definition['childRequirements']:
                models.ModuleChildRequirement.objects.update_or_create(
                    module=module, uuid=uuid, defaults=dict(deleted=False))

            # add module implemented requirements
        if 'implemented' in definition:
            module.moduleimplementedrequirement_set.all().update(deleted=True)
            for uuid in definition['implemented']:
                models.ModuleImplementedRequirement.objects.update_or_create(
                    module=module, uuid=uuid, defaults=dict(deleted=False))
