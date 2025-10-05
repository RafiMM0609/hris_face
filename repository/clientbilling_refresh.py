from typing import List
import calendar
from datetime import datetime, timedelta, date
from typing import Optional
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import Session
from core.myworker import trigger_worker
from models import get_background_db
from models.Client import Client
from models.ClientPayment import ClientPayment
from pytz import timezone
from models.RefreshClientReport import RefreshClientReport
from models.RefreshReport import RefreshReport
from models.UserClient import UserClient
from models.UserRole import UserRole
from settings import TZ
from datetime import datetime, timedelta
import traceback
from fastapi.logger import logger


async def get_list_id_client(
    db: Session,
):
    logger.info("Starting get_list_id_client...")
    try:
        ls_client_id = db.query(Client.id).where(
            Client.isact == True
        ).all()

        ls_client_id = [client[0] for client in ls_client_id]
        logger.info(f"Retrieved {len(ls_client_id)} client IDs")
        return ls_client_id
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error fetching client IDs: {str(e)}")
        return []

async def get_last_payment_id(db:Session, client_id:List[int]):
    logger.info(f"Starting get_last_payment_id for {len(client_id)} clients...")
    try:
        ls_result = []
        for cid in client_id:
            last_payment = db.query(ClientPayment.id).\
                filter(
                    ClientPayment.client_id == cid,
                    ClientPayment.isact == True
                    ).\
                order_by(ClientPayment.date.desc()).\
                first()
            if last_payment:
                # ls_result.append((cid, last_payment.id))
                ls_result.append(last_payment.id)
        logger.info(f"Retrieved {len(ls_result)} last payment IDs")
        return ls_result
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error fetching last payment IDs: {str(e)}")
        return []

async def runner_scheduler_refresh_bo_report():
    logger.info("Starting scheduler refresh BO report...")
    with get_background_db() as db:
        try:
            client_ids = await get_list_id_client(db)
            if not client_ids:
                logger.info("No active clients found")
                return
            
            last_payment_ids = await get_last_payment_id(db, client_ids)
            if not last_payment_ids:
                logger.info("No payment records found for any client")
                return
            
            logger.info(f"Found {len(last_payment_ids)} payment records to process")
            
            ls_new_reports = []
            for payment_id in last_payment_ids:
                logger.info(f"Add payment ID to refresh tasks list: {payment_id}")
                existing = db.query(RefreshReport).filter(RefreshReport.billing_id == payment_id).first()
                if existing:
                    existing.isact = True
                    existing.last_refresh = datetime.now(timezone(TZ)).replace(tzinfo=None) - timedelta(days=1)
                else:
                    new_report = RefreshReport(
                        billing_id=payment_id, 
                        isact=True,
                        last_refresh=datetime.now(timezone(TZ)).replace(tzinfo=None) - timedelta(days=1)
                        )
                    ls_new_reports.append(new_report)
            db.bulk_save_objects(ls_new_reports)

            ls_new_client_reports = []
            for client_id in client_ids:
                existing = db.query(RefreshClientReport).filter(RefreshClientReport.client_id == client_id).first()
                if existing:
                    existing.isact = True
                    existing.last_refresh = datetime.now(timezone(TZ)).replace(tzinfo=None) - timedelta(days=1)
                else:
                    new_entry = RefreshClientReport(
                        client_id=client_id,
                        isact=True,
                        last_refresh=datetime.now(timezone(TZ)).replace(tzinfo=None) - timedelta(days=1)
                    )
                    ls_new_client_reports.append(new_entry)
            if ls_new_client_reports:
                db.bulk_save_objects(ls_new_client_reports)

            db.commit()
            logger.info("Completed refreshing BO reports for all clients")
            
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error in scheduler runner: {str(e)}")
            raise
    
async def runner_refresh_bo_report():
    logger.info("Starting runner_refresh_bo_report...")
    with get_background_db() as db:
        try:
            reports_to_refresh = db.query(RefreshReport).where(
                RefreshReport.isact == True,
                RefreshReport.last_refresh < datetime.now(timezone(TZ)).replace(tzinfo=None).replace(hour=0, minute=0, second=0, microsecond=0)
            ).order_by(RefreshReport.id.desc()).first()
            
            if not reports_to_refresh:
                logger.info("No reports to refresh")
                return
            
            logger.info(f"Found {reports_to_refresh.billing_id} reports to refresh")

            await refresh_bo_report(db, reports_to_refresh.billing_id, reports_to_refresh.id)

            logger.info("Completed call all BO report refresh tasks")
            
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error in runner_refresh_bo_report: {str(e)}")
            raise

async def runner_refresh_or_generate_client_bo_report():
    logger.info("Starting runner_refresh_or_generate_client_bo_report...")
    with get_background_db() as db:
        try:
            client_report_for_refresh = db.query(RefreshClientReport).where(
                RefreshClientReport.isact == True,
                RefreshClientReport.last_refresh < datetime.now(timezone(TZ)).replace(tzinfo=None).replace(hour=0, minute=0, second=0, microsecond=0)
            ).order_by(RefreshClientReport.id.desc()).first()
            
            if not client_report_for_refresh:
                logger.info("No client report to refresh")
                return
            client_report_for_refresh.isact = False
            client_report_for_refresh.last_refresh = datetime.now(timezone(TZ)).replace(tzinfo=None)
            db.commit()

            logger.info(f"Found client {client_report_for_refresh.client_id} report to refresh (Refresh ID: {client_report_for_refresh.id})")
            batch_data = {
                "client_id": client_report_for_refresh.client_id,
            }
            await trigger_worker("bulk_operation_client", batch_data)

            logger.info(f"Completed triggering BO report refresh task for client {client_report_for_refresh.client_id} (Report ID: {client_report_for_refresh.id})")

            
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error in runner_refresh_or_generate_client_bo_report: {str(e)}")
            raise

async def refresh_bo_report(db:Session, id:str, refresh_report_id:int):
    logger.info(f"Starting refresh_bo_report for payment ID: {id}")
    try:
        client_payment_data = db.query(ClientPayment).where(ClientPayment.id==id).first()
        if not client_payment_data:
            raise ValueError("Client payment data not found")
            
 
        
        allowed_roles = [1, 6]
        list_id_user = db.query(UserClient.emp_id.distinct()).\
            join(UserRole, UserClient.emp_id == UserRole.c.emp_id).\
            where(
                UserClient.client_id == client_payment_data.client_id,
                UserClient.isact == True,
                and_(
                    UserRole.c.role_id.in_(allowed_roles)
                )
            ).all()

        ls_userids = [user[0] for user  in list_id_user]
        
        if not ls_userids:
            logger.info("No active users found for client")
            return
        
        logger.info(f"Processing {len(ls_userids)} users for client {client_payment_data.client_id}")

        # get data client
        client_data = db.execute(
            select(Client.cutoff_date).where(Client.id == client_payment_data.client_id)
        ).scalar()
        client_cutoff_date = client_data if client_data else 30  # Default to 30 if not set
        custom_today = client_payment_data.date - timedelta(days=1) if client_payment_data.date else datetime.now(timezone(TZ))
        start_date, end_date = get_periode_by_kontrak_custom(
            tgl_kontrak= client_cutoff_date,
            today= custom_today
        )
        logger.info(f"Start Date: {start_date}, End Date: {end_date}")
        
        BATCH_SIZE = 45  # Process 50 users at a time
        
        for i in range(0, len(ls_userids), BATCH_SIZE):
            batch_userids = ls_userids[i:i + BATCH_SIZE]
            
            # Create batch data for multiple users
            batch_data = {
                "emp_ids": batch_userids,  # Send list of emp_ids instead of single emp_id
                "client_id": client_payment_data.client_id,
                "id_client": client_payment_data.client_id,
                "batch_size": len(batch_userids),
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
            }
            
            logger.info(f"Processing batch {i//BATCH_SIZE + 1}: {len(batch_userids)} users")
            
            await trigger_worker("bulk_batch_checkout_operations_with_date", batch_data)
            
        logger.info(f"Successfully queued all {len(ls_userids)} users for processing")
        logger.info(f"Completed refresh_bo_report for payment ID: {id}")
        update_last_sync_report_if_exist(refresh_id=refresh_report_id)
            
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Error refreshing BO report: {str(e)}")
        raise ValueError("Gagal refresh billing, silahkan hubungi admin")
    
def update_last_sync_report_if_exist(refresh_id:int):
    logger.info(f"Starting update_last_sync_report_if_exist for refresh ID: {refresh_id}")
    with get_background_db() as db:
        try:
            report_record = db.query(RefreshReport).where(RefreshReport.id == refresh_id).first()
            if report_record:
                report_record.last_refresh = datetime.now(timezone(TZ)).replace(tzinfo=None)
                report_record.isact = False
                db.commit()
                logger.info(f"Updated last_refresh for report ID: {refresh_id}")
            else:
                logger.info(f"No RefreshReport found with ID: {refresh_id}")
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error updating last_refresh: {str(e)}")
            raise

def get_periode_by_kontrak_custom(
    tgl_kontrak: int,
    today: Optional[date] = None
):
    if today is None:
        today = date.today()
    # Cari tanggal kontrak bulan ini
    last_day_this_month = calendar.monthrange(today.year, today.month)[1]
    tgl_kontrak_bulan_ini = min(tgl_kontrak, last_day_this_month)
    tanggal_kontrak_bulan_ini = today.replace(day=tgl_kontrak_bulan_ini)

    if today < tanggal_kontrak_bulan_ini:
        # Periode: kontrak bulan lalu - kontrak bulan ini
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month > 1 else today.year - 1
        last_day_prev_month = calendar.monthrange(prev_year, prev_month)[1]
        tgl_kontrak_bulan_lalu = min(tgl_kontrak, last_day_prev_month)
        tanggal_kontrak_bulan_lalu = tanggal_kontrak_bulan_ini.replace(year=prev_year, month=prev_month, day=tgl_kontrak_bulan_lalu)
        start_periode = tanggal_kontrak_bulan_lalu + timedelta(days=1)
        end_periode = tanggal_kontrak_bulan_ini
    else:
        # Periode: kontrak bulan ini - kontrak bulan depan
        next_month = today.month + 1 if today.month < 12 else 1
        next_year = today.year if today.month < 12 else today.year + 1
        last_day_next_month = calendar.monthrange(next_year, next_month)[1]
        tgl_kontrak_bulan_depan = min(tgl_kontrak, last_day_next_month)
        tanggal_kontrak_bulan_depan = tanggal_kontrak_bulan_ini.replace(year=next_year, month=next_month, day=tgl_kontrak_bulan_depan)
        start_periode = tanggal_kontrak_bulan_ini + timedelta(days=1)
        end_periode = tanggal_kontrak_bulan_depan
    return start_periode, end_periode
