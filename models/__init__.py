from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import logging
import time
from settings import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER
)
from contextlib import contextmanager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

# Konfigurasi optimal connection pool untuk high-concurrency
engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_size=30,        # Increased untuk concurrent requests
    max_overflow=20,      # Increased overflow capacity
    pool_recycle=3600,    # Increased ke 1 jam untuk stability
    pool_timeout=60,      # Increased timeout untuk busy periods
    pool_pre_ping=True,   # Validates connections before use
    pool_reset_on_return='commit',  # Ensures clean connection state
    echo=False            # Set to True for SQL debugging
)

def log_pool_status(message: str = "Pool Status"):
    pool = engine.pool
    worker_pool = worker_engine.pool
    
    # Log pool status with available attributes
    logger.info(f"{message} - Main Pool - Checked out: {pool.checkedout()}, Size: {pool.size()}, Overflow: {pool.overflow()}")
    logger.info(f"{message} - Worker Pool - Checked out: {worker_pool.checkedout()}, Size: {worker_pool.size()}, Overflow: {worker_pool.overflow()}")
    
    # Alert if pool usage is high
    main_usage = (pool.checkedout() / (pool.size() + pool.overflow())) * 100 if (pool.size() + pool.overflow()) > 0 else 0
    worker_usage = (worker_pool.checkedout() / (worker_pool.size() + worker_pool.overflow())) * 100 if (worker_pool.size() + worker_pool.overflow()) > 0 else 0
    
    if main_usage > 80:
        logger.warning(f"Main pool usage high: {main_usage:.1f}%")
    if worker_usage > 80:
        logger.warning(f"Worker pool usage high: {worker_usage:.1f}%")

# @event.listens_for(engine, "connect")
# def connect(dbapi_connection, connection_record):
#     logger.info("Database connection established")
#     log_pool_status()

# @event.listens_for(engine, "checkout")
# def checkout(dbapi_connection, connection_record, connection_proxy):
#     logger.info("Database connection retrieved from pool")
#     log_pool_status()

# Add connection pool monitoring
@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    logger.info("Database connection established")

@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    logger.info("Database connection retrieved from pool")

# Create database session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Separate engine for worker service to avoid pool conflicts
worker_engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_size=30,         # Dedicated pool for background tasks
    max_overflow=10,      # Additional capacity for worker tasks
    pool_recycle=2400,    # 40 minutes for background tasks
    pool_timeout=45,      # Longer timeout for heavy operations
    pool_pre_ping=True,
    pool_reset_on_return='commit',
    echo=False
)

# Worker session factory
WorkerSessionLocal = sessionmaker(bind=worker_engine, autoflush=False, autocommit=False)

@contextmanager
def get_background_db():
    """Context manager for background task database operations"""
    db = WorkerSessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        logger.error(f"Background task database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Validate database connection on startup
try:
    with engine.connect() as connection:
        logger.info("Successfully connected to MySQL database")
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")

# Import all model modules to ensure they are registered
import models.Allowances
import models.Attendance
import models.AttendanceSummary
import models.Bpjs
import models.BpjsEmployee
import models.Client
import models.ClientOutlet
import models.ClientPayment
import models.ClientWilayah
import models.Compensation
import models.Contract
import models.ContractClient
import models.CustomAllowances
import models.DbBackup
import models.DefaultPassword
import models.EmployeeAllowances
import models.EmployeeTax
import models.ExcelDownload
import models.ForgotPassword
import models.HistoryActivityEmp
import models.Izin
import models.LeaveTable
import models.LogActivity
import models.MasterCompensation
import models.MasterPtkp
import models.MasterShift
import models.Menu
import models.MobileVersion
import models.Module
import models.NationalHoliday
import models.Notification
import models.OutletWilayah
import models.PajakTer
import models.ParentCompensation
import models.Payroll
import models.Performance
import models.Permission
import models.RefreshClientReport
import models.RefreshReport
import models.Role
import models.RolePermission
import models.ShiftSchedule
import models.StatusIzin
import models.StatusPayment
import models.TadAllowance
import models.Tax
import models.TempDataKaryawan
import models.TimeSheet
import models.TypeTad
import models.User
import models.UserClient
import models.UserOutlet
import models.UserRole
import models.UserToken
import models.UserWilayah
import models.Wilayah