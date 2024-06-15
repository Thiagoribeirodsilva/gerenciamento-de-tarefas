from sqlalchemy.orm import Session

from app.domain.models import Tarefa


class ITarefaRepository:
    def create(self, tarefa: object):
        raise NotImplementedError

    def read(self, tarefa_id: int):
        raise NotImplementedError

    def update(self, tarefa: object, tarefa_data: dict):
        raise NotImplementedError

    def delete(self, tarefa: object):
        raise NotImplementedError

    def find_all(self):
        raise NotImplementedError


class TarefaRepository(ITarefaRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, tarefa: Tarefa) -> Tarefa:
        self.session.add(tarefa)
        self.session.commit()
        self.session.refresh(tarefa)
        return tarefa

    def update(self, tarefa: Tarefa, tarefa_data) -> Tarefa:
        for key, value in tarefa_data.items():
            setattr(tarefa, key, value)
        self.session.commit()
        self.session.refresh(tarefa)
        return tarefa

    def delete(self, tarefa: Tarefa) -> int:
        tarefa_id = tarefa.id
        self.session.delete(tarefa)
        self.session.commit()
        return tarefa_id

    def read(self, tarefa_id):
        return self.session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

    def find_all(self):
        return self.session.query(Tarefa).all()