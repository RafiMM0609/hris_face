import asyncio
from core.myworker import trigger_worker
from repository.clientbilling_refresh import runner_refresh_bo_report, runner_refresh_or_generate_client_bo_report, runner_scheduler_refresh_bo_report
from fastapi.logger import logger

def run_scheduled_task_1(func_name: str):
    try:
        if func_name == "checkout employees":
            checkout_employees()
        elif func_name == "generate_report":
            print("Running generate report task")
            auto_refresh_report()
        elif func_name == "generate_report_runner":
            print("Running generate report runner task")
            auto_refresh_report_runner()
        elif func_name == "generate_client_report_runner":
            print("Running generate client report runner task")
            auto_refresh_client_report_runner()
        else:
            raise ValueError(f"Unknown function name: {func_name}")
    except Exception as e:
        logger.error()(f"Error in scheduled task {func_name}: {e}")
    
def checkout_employees():
    logger.info("Starting checkout employees task...")
    try:
        asyncio.run(trigger_worker("auto_checkout_23_59", {}))
    except Exception as e:
        logger.error(f"Error in checkout employees task: {e}")

def auto_refresh_report():
    logger.info("Starting auto refresh report task...")
    try:
        asyncio.run(runner_scheduler_refresh_bo_report())
    except Exception as e:
        logger.error(f"Error in auto refresh report task: {e}")

def auto_refresh_report_runner():
    logger.info("Starting auto refresh report runner task...")
    try:
        asyncio.run(runner_refresh_bo_report())
    except Exception as e:
        logger.error(f"Error in auto refresh report runner task: {e}")


def auto_refresh_client_report_runner():
    logger.info("Starting auto refresh client report runner task...")
    try:
        asyncio.run(runner_refresh_or_generate_client_bo_report())
    except Exception as e:
        logger.error(f"Error in auto refresh client report runner task: {e}")
