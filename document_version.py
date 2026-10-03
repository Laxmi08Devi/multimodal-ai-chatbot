from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from app.database.database import Base


class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )

    version_number = Column(Integer)

    content = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )