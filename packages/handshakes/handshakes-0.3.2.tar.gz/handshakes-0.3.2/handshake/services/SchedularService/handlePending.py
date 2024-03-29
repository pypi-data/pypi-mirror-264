from handshake.services.DBService.models.dynamic_base import TaskBase
from handshake.services.SchedularService.modifySuites import patchTestSuite
from handshake.services.SchedularService.constants import JobType
from handshake.services.SchedularService.completeTestRun import patchTestRun
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handshake.services.SchedularService.pruneTasks import pruneTasks

from loguru import logger
from tortoise.expressions import Q
from datetime import datetime


def add_lookup_task(_scheduler: AsyncIOScheduler):
    _scheduler.add_job(
        lookup_for_tasks,
        id=JobType.LOOKUP_JOB,
        name="clearing up the pending tasks if present",
        args=(_scheduler,),
        next_run_time=datetime.now(),
        max_instances=2,
    )


# NOTE: make sure to pick the task before adding a new task
async def lookup_for_tasks(_scheduler: AsyncIOScheduler):
    logger.info("Looking up for the tasks")

    task = (
        await TaskBase.filter(
            Q(picked=False)
            & Q(processed=False)
            & (
                Q(type=JobType.MODIFY_SUITE)
                | Q(type=JobType.MODIFY_TEST_RUN)
                | Q(type=JobType.PRUNE_TASKS)
            )
        )
        .order_by("dropped")
        .first()
    )  # ascending

    if not task:
        return logger.warning("No Task found in this iteration")

    await task.update_from_dict(dict(picked=True))
    await task.save()

    is_task_processed = False

    match task.type:
        case JobType.MODIFY_SUITE:
            is_task_processed = await patchTestSuite(task.ticketID, task.test_id)

        case JobType.MODIFY_TEST_RUN:
            is_task_processed = await patchTestRun(task.ticketID, task.test_id)

        case JobType.PRUNE_TASKS:
            await pruneTasks(task.ticketID)
            is_task_processed = True

        case _:
            logger.warning("Not Implemented yet..")

    if is_task_processed:
        await task.update_from_dict(dict(processed=True))
        await task.save()
    else:
        logger.info(
            "This Task: {} - {} will continue in the next iteration",
            task.ticketID,
            task.type,
        )

    logger.info("Rescheduling for lookup task")
    add_lookup_task(_scheduler)
