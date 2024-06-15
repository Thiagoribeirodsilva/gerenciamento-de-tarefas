import logging

from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError

from app.domain.dto.dtos import TarefaCreateDTO, TarefaDTO, TarefaUpdateDTO
from app.domain.models import Tarefa
from app.repositories.tarefa_repository import ITarefaRepository

logger = logging.getLogger("fastapi")


class ITarefaService:

    def create_tarefa(self, tarefa_data: object):
        raise NotImplementedError

    def read_tarefa(self, tarefa_id: int):
        raise NotImplementedError

    def update_tarefa(self, tarefa_id: int, tarefa_update: object):
        raise NotImplementedError

    def delete_tarefa(self, tarefa_id: int):
        raise NotImplementedError


class TarefaService(ITarefaService):

    def __init__(self, tarefa_repository: ITarefaRepository):
        self.tarefa_repository = tarefa_repository

    def create_tarefa(self, tarefa_data: TarefaCreateDTO) -> TarefaDTO:
        tarefa = Tarefa(**tarefa_data.model_dump())
        try:
            logger.info("Creating task: %s", tarefa)
            created_tarefa = self.tarefa_repository.create(tarefa)
        except IntegrityError as e:
            logger.error("Error creating task: %s. Detail: %s", tarefa, e)
            raise HTTPException(status_code=409, detail=f"Tarefa already exists. Error: {e.args[0]}")
        return TypeAdapter(TarefaDTO).validate_python(created_tarefa)

    def read_tarefa(self, tarefa_id: int) -> TarefaDTO:
        logger.info("Reading task with id %s", tarefa_id)
        tarefa = self.tarefa_repository.read(tarefa_id)
        if tarefa is None:
            logger.error("Task with id %s not found", tarefa_id)
            raise HTTPException(status_code=404, detail="Task not found")
        return TypeAdapter(TarefaDTO).validate_python(tarefa)

    def find_all(self) -> list[TarefaDTO]:
        logger.info("Finding all tasks")
        tasks = self.tarefa_repository.find_all()
        return [TypeAdapter(TarefaDTO).validate_python(tarefa) for tarefa in tasks]

    def update_tarefa(self, tarefa_id: int, tarefa_data: TarefaUpdateDTO) -> TarefaDTO:
        logger.info("Updating task with id %s", tarefa_id)
        tarefa = self.tarefa_repository.read(tarefa_id)
        if tarefa is None:
            logger.error("Task with id %s not found", tarefa_id)
            raise HTTPException(status_code=404, detail="Task not found")

        tarefa_data = tarefa_data.model_dump(exclude_unset=True)
        for key, value in tarefa_data.items():
            setattr(tarefa, key, value)
        updated_tarefa = self.tarefa_repository.update(tarefa, tarefa_data)
        return TypeAdapter(TarefaDTO).validate_python(updated_tarefa)

    def delete_tarefa(self, tarefa_id: int) -> int:
        logger.info("Deleting task with id %s", tarefa_id)
        tarefa = self.tarefa_repository.read(tarefa_id)
        if tarefa is None:
            logger.error("Task with id %s not found", tarefa_id)
            raise HTTPException(status_code=404, detail="Task not found")
        return self.tarefa_repository.delete(tarefa)