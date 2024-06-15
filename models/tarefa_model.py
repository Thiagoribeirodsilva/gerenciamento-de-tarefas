from datetime import datetime

from app.config.database import Base, engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session


class Tarefa(Base):
    __tablename__ = 'tarefa'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(50))
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

    def create(self, session: Session):
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    def update(self, session: Session, user_data):
        for key, value in user_data.items():
            setattr(self, key, value)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session: Session):
        tarefa_id = self.id
        session.delete(self)
        session.commit()
        return tarefa_id

    def read(self, session: Session, tarefa_id):
        return session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

    def __repr__(self):
        return f'<tarefa(id={self.id}, title={self.title}, description={self.description},status={self.status}, created_at={self.created_at})>'


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
