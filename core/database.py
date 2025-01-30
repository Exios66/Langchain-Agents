# core/database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from contextlib import contextmanager

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize SQLite Database
DATABASE_URL = "sqlite:///./multi_agent.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class WorkflowState(Base):
    """Database model for storing agent interactions and workflow states."""
    __tablename__ = "workflow_states"

    id = Column(Integer, primary_key=True, index=True)
    input_data = Column(Text, nullable=False)
    state_data = Column(JSON, nullable=False)
    messages = Column(JSON, nullable=False)
    workflow_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")

    def to_dict(self) -> Dict[str, Any]:
        """Convert DB record to dictionary."""
        try:
            return {
                "id": self.id,
                "input_data": json.loads(self.input_data) if isinstance(self.input_data, str) else self.input_data,
                "state_data": json.loads(self.state_data) if isinstance(self.state_data, str) else self.state_data,
                "messages": json.loads(self.messages) if isinstance(self.messages, str) else self.messages,
                "workflow_type": self.workflow_type,
                "status": self.status
            }
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in to_dict: {e}")
            raise ValueError(f"Invalid JSON data in workflow state: {e}")
        except Exception as e:
            logger.error(f"Error in to_dict: {e}")
            raise

@contextmanager
def get_db():
    """Database session context manager with error handling."""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def save_workflow_state(
    input_data: Dict[str, Any],
    state_data: Dict[str, Any],
    messages: List[str],
    workflow_type: str,
    status: str = "pending"
) -> int:
    """Save workflow state to database with error handling."""
    try:
        with get_db() as db:
            workflow_state = WorkflowState(
                input_data=json.dumps(input_data),
                state_data=json.dumps(state_data),
                messages=json.dumps(messages),
                workflow_type=workflow_type,
                status=status
            )
            db.add(workflow_state)
            db.commit()
            db.refresh(workflow_state)
            return workflow_state.id
    except json.JSONDecodeError as e:
        logger.error(f"JSON encode error in save_workflow_state: {e}")
        raise ValueError(f"Invalid data for workflow state: {e}")
    except SQLAlchemyError as e:
        logger.error(f"Database error in save_workflow_state: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in save_workflow_state: {e}")
        raise

def get_workflow_state(state_id: int) -> Optional[Dict[str, Any]]:
    """Get workflow state from database with error handling."""
    try:
        with get_db() as db:
            workflow_state = db.query(WorkflowState).filter(WorkflowState.id == state_id).first()
            if workflow_state:
                return workflow_state.to_dict()
            return None
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_workflow_state: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_workflow_state: {e}")
        raise

def update_workflow_status(state_id: int, status: str) -> bool:
    """Update workflow status with error handling."""
    try:
        with get_db() as db:
            workflow_state = db.query(WorkflowState).filter(WorkflowState.id == state_id).first()
            if workflow_state:
                workflow_state.status = status
                db.commit()
                return True
            return False
    except SQLAlchemyError as e:
        logger.error(f"Database error in update_workflow_status: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in update_workflow_status: {e}")
        raise

# SQLAlchemy event listeners for debugging
@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    logger.info("Database connection established")

@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    logger.debug("Database connection checked out")

@event.listens_for(engine, "checkin")
def checkin(dbapi_connection, connection_record):
    logger.debug("Database connection checked in")

# Create tables
Base.metadata.create_all(bind=engine)