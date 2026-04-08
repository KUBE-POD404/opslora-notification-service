from celery.signals import task_failure
import logging

logger = logging.getLogger(__name__)


@task_failure.connect
def handle_task_failure(sender=None, task_id=None, exception=None, args=None, kwargs=None, traceback=None, **kw):

    logger.error(
        f"[GLOBAL TASK FAILURE] task={sender.name} "
        f"task_id={task_id} "
        f"exception={exception} "
        f"args={args} kwargs={kwargs}"
    )