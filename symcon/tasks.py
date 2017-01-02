# -*- coding: UTF-8 -*-
from celery.utils.log import get_task_logger

from heroku import celery_app

logger = get_task_logger(__name__)


@celery_app.task()
def debug_task():
    print('Congratulation, Celery is running :)')


@celery_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5})
def symcon_repository_update_nightly():
    from symcon.models import Repository
    for repository in Repository.objects.all():
        symcon_update_repository.apply_async([repository.user, repository.name])


@celery_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5})
def symcon_update_repository(user, name):
    from symcon.common.util.symcon import SymconRepositoryHandler
    symcon = SymconRepositoryHandler()
    symcon.update_repository(user=user, name=name)


@celery_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5})
def symcon_update_branch(branch_id):
    from symcon.common.util.symcon import SymconRepositoryHandler
    symcon = SymconRepositoryHandler()
    symcon.update_branch(branch_id=branch_id)


@celery_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5})
def symcon_update_librarybranch_module(librarybranch_id, modulepath):
    from symcon.common.util.symcon import SymconRepositoryHandler
    symcon = SymconRepositoryHandler()
    symcon.update_librarybranch_module(librarybranch_id, modulepath)
