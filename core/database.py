# core/database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from typing import Dict, Any, Optional

# Initialize SQLite Database
DATABASE_URL = "sqlite:///./multi_agent.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
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
        return {
            "id": self.id,
            "input_data": json.loads(self.input_data) if isinstance(self.input_data, str) else self.input_data,
            "state_data": json.loads(self.state_data) if isinstance(self.state_data, str) else self.state_data,
            "messages": json.loads(self.messages) if isinstance(self.messages, str) else self.messages,
            "workflow_type": self.workflow_type,
            "status": self.status
        }

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)