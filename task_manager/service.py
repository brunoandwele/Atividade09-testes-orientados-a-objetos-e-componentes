from task_manager.repository import Task_Repository
from task_manager.Task import Task,Priority,Status
import datetime

class TaskService:
    def __init__(self, repositorio=Task_Repository()):
        self.repositorio = repositorio
        self.__validou_nova_tarefa = False

    def criar_tarefa(self, task = Task()):

        if not task.titulo and task.descricao:
            raise ValueError("Título e Descrição não podem ser vazio")
        if not isinstance(task.status, Status):
            raise ValueError("Status está inválido")
        if not isinstance(task.prioridade, Priority):
            raise ValueError("Prioridade está inválida")
        else:
            self.__validou_nova_tarefa = True

        if self.__validou_nova_tarefa:
            tarefa = Task(None, "Aqui está um título","Uma descrição legal",Priority.Baixa,datetime.now,Status.PENDENTE)
            tarefa.validar()
            self.__validou_nova_tarefa = False
            return self.repositorio.save(tarefa)

    def listar_todas(self) -> list[Task]:
        return self.repositorio.find_all()
    

        
        