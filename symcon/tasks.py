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
        symcon_repository_update.apply_async([repository.user, repository.name])


@celery_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5})
def symcon_repository_update(user, name):
    from symcon.common.util.symcon import SymconRepositoryHandler
    symcon = SymconRepositoryHandler()
    symcon.update_repository(user, name)


@celery_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5})
def symcon_repository_subdirectory(user, name, library_id, path):
    from symcon.common.util.symcon import SymconRepositoryHandler
    symcon = SymconRepositoryHandler()
    symcon.update_repository_module(user, name, library_id, path)
