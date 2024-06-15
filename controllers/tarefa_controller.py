from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.domain.dto.dtos import TarefaDTO, TarefaCreateDTO, TarefaUpdateDTO
from app.repositories.tarefa_repository import TarefaRepository
from app.services.tarefa_service import TarefaService

tarefa_router = APIRouter(prefix="/tarefa", tags=["Tarefas"])


def get_tarefa_repo(db: Session = Depends(get_db)) -> TarefaRepository:
    return TarefaRepository(db)


@tarefa_router.post("/", status_code=201, description="Busca todas as tarefas", response_model=TarefaDTO)
def create(request: TarefaCreateDTO, tarefa_repo: TarefaRepository = Depends(get_tarefa_repo)):
    tarefa_service = TarefaService(tarefa_repo)
    return tarefa_service.create_tarefa(request)


@tarefa_router.get("/{tarefa_id}", status_code=200, description="Busca uma tarefa pelo ID", response_model=TarefaDTO)
def find_by_id(tarefa_id: int, tarefa_repo: TarefaRepository = Depends(get_tarefa_repo)):
    tarefa_service = TarefaService(tarefa_repo)
    return tarefa_service.read_tarefa(tarefa_id)


@tarefa_router.get("/", status_code=200, description="Busca todas as tarefas", response_model=list[TarefaDTO])
def find_all(tarefa_repo: TarefaRepository = Depends(get_tarefa_repo)):
    tarefa_service = TarefaService(tarefa_repo)
    return tarefa_service.find_all()


@tarefa_router.put("/{tarefa_id}", status_code=200, description="Atualiza uma tarefa", response_model=TarefaDTO)
def update(tarefa_id: int, request: TarefaUpdateDTO, tarefa_repo: TarefaRepository = Depends(get_tarefa_repo)):
    tarefa_service = TarefaService(tarefa_repo)
    return tarefa_service.update_tarefa(tarefa_id, request)


@tarefa_router.delete("/{tarefa_id}", status_code=204, description="Deleta uma tarefa")
def delete(tarefa_id: int, tarefa_repo: TarefaRepository = Depends(get_tarefa_repo)):
    tarefa_service = TarefaService(tarefa_repo)
    tarefa_service.delete_tarefa(tarefa_id)