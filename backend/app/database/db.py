import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Text, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class AnalysisRecord(Base):
    __tablename__ = 'analysis_records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    fake_news_label = Column(Text, nullable=False)
    fake_news_confidence = Column(Float, nullable=False)
    sentiment_label = Column(Text, nullable=False)
    sentiment_confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = None
SessionLocal = None
db_available = False

def init_db(app):
    global engine, SessionLocal, db_available
    db_url = app.config.get('DATABASE_URL')
    
    if not db_url:
        logging.warning("DATABASE_URL not configured. Database persistence disabled.")
        db_available = False
        return

    try:
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 3}  # fail fast if PostgreSQL not available
        )
        Base.metadata.create_all(bind=engine)

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db_available = True
        logging.info("PostgreSQL database initialized successfully.")
    except Exception as e:
        logging.warning(f"Failed to connect to PostgreSQL database: {e}. Graceful degradation active.")
        db_available = False

def save_analysis(text, fake_news_res, sentiment_res):
    global db_available, SessionLocal
    if not db_available or not SessionLocal:
        return None
    
    try:
        session = SessionLocal()
        record = AnalysisRecord(
            text=text[:2000],  # truncate long text for history storage safety
            fake_news_label=fake_news_res.get('label', 'UNKNOWN'),
            fake_news_confidence=float(fake_news_res.get('confidence', 0.0)),
            sentiment_label=sentiment_res.get('label', 'NEUTRAL'),
            sentiment_confidence=float(sentiment_res.get('confidence', 0.0))
        )
        session.add(record)
        session.commit()
        record_id = record.id
        session.close()
        return record_id
    except Exception as e:
        logging.error(f"Failed to save analysis record to PostgreSQL: {e}")
        return None
