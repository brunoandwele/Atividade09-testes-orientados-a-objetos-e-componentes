from datetime import datetime
from task_manager.storage import InMemoryStage
from task_manager.Task import Task

class Task_Repository:
    def __init__(self, storage=InMemoryStage()):
        print(f"[DEBUG] Inicializando Task_Repository com storage={type(storage).__name__}")
        self.storage = storage
        self.__next_id = 1
        print(f"[DEBUG] Repositório iniciado | Próximo ID={self.__next_id}")

    def save(self, task: Task):
        print(f"[DEBUG] Salvando tarefa... | task={task}")

        if not isinstance(task, Task):
            print(f"[ERRO] Objeto inválido para salvar | tipo={type(task)}")
            raise ValueError("O objeto salvo deve ser uma instância de Task.")

        if getattr(task, "titulo", None) is None or not isinstance(task.titulo, str):
            print(f"[ERRO] Task sem título válido.")
            raise ValueError("A tarefa deve possuir um título válido.")

        task.id = self.__next_id
        self.__next_id += 1
        self.storage.add(task.id, task)
        print(f"[DEBUG] Tarefa salva com sucesso | id={task.id} | próximo_id={self.__next_id}")
        return task
    
    def find_by_id(self, id):
        print(f"[DEBUG] Buscando tarefa por ID | id={id}")

        if not isinstance(id, int) or id <= 0:
            print(f"[ERRO] ID inválido: {id}")
            raise ValueError("O ID deve ser um número inteiro positivo.")

        task = self.storage.get(id)
        if task:
            print(f"[DEBUG] Tarefa encontrada | id={id}")
            return task
        else:
            print(f"[WARN] Nenhuma tarefa encontrada com o ID {id}")
            return None
    
    def find_all(self) -> list[Task]:
        print(f"[DEBUG] Recuperando todas as tarefas...")
        tasks = list(self.storage.get_all())
        print(f"[DEBUG] Total de tarefas encontradas: {len(tasks)}")
        return tasks

    def delete(self, id):
        print(f"[DEBUG] Tentando excluir tarefa | id={id}")

        if not isinstance(id, int) or id <= 0:
            print(f"[ERRO] ID inválido para exclusão: {id}")
            raise ValueError("O ID deve ser um número inteiro positivo.")

        deleted = self.storage.delete(id)
        if deleted:
            print(f"[DEBUG] Tarefa removida com sucesso | id={id}")
        else:
            print(f"[WARN] Nenhuma tarefa encontrada para remover | id={id}")
        return deleted