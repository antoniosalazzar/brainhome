from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )

    # Relationship back to User
    owner = relationship("User", back_populates="items")

    def __repr__(self):
        return f"<Item id={self.id} title={self.title} owner_id={self.owner_id}>"