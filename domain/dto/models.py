from sqlalchemy import Column, Integer, String, DateTime

from app.config.database import Base, engine

from datetime import datetime


class Tarefa(Base):
    __tablename__ = 'tarefa'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(50))
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'<tarefa(id={self.id}, title={self.title}, description={self.description},status={self.status}, created_at={self.created_at})>' # TODO: formatação estava errada


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)