from datetime import datetime

from app.config.database import get_db
from app.models.tarefa_model import Tarefa


def main():
    title = 'Atividade Proposta'
    description = 'Gerenciamento de tarefas'
    status = 'Em Progresso'
    created_at = datetime.now()
    with get_db() as session:
        tarefa = Tarefa(title=title, description=description, status=status, created_at=created_at)

        tarefa.create(session=session)
        tarefa_id = tarefa.id
        print(f'Tarefa criada com id {tarefa_id}')

        tarefa_read = tarefa.read(session=session, tarefa_id=tarefa_id)
        print(f'Tarefa lida: {tarefa_read}')

        tarefa_data = {'title': 'Nova Atividade'}
        tarefa_update = tarefa.update(session=session, _id=tarefa_id, data=tarefa_data) # FIXME: Está passando 3 parametros, mas sua função update recebe apenas 2
        print(f'Tarefa atualizada: {tarefa_update}')

        tarefa_delete = tarefa.delete(session=session, _id=tarefa_id)# FIXME: Está passando 2 parametros, mas sua função update recebe apenas 1
        print(f'Tarefa deletada com id {tarefa_delete}')


if __name__ == '__main__':
    main()
