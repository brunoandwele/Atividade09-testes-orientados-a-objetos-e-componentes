from datetime import datetime, timedelta
from unittest.mock import Mock
import pytest
from task_manager.repository import Task_Repository
from task_manager.storage import InMemoryStage
from task_manager.Task import Priority, Status, Task

def test_save_atribui_id(mocker):
    print("[TEST] Iniciando test_save_atribui_id")
    mock_storage = mocker.Mock()
    repo = Task_Repository(mock_storage)
    task = Task(None, "Teste", "Desc", Priority.BAIXA, datetime.now() + timedelta(minutes=5), Status.EM_PROGRESSO)

    print("[TEST] Salvando task...")
    resultado = repo.save(task)
    print(f"[TEST] Task salva | id={resultado.id} titulo={resultado.titulo} prioridade={resultado.prioridade}")

    assert resultado.id == 1
    assert isinstance(resultado.id, int)
    assert resultado is task
    mock_storage.add.assert_called_once()
    called_id, called_task = mock_storage.add.call_args[0]
    assert called_id == resultado.id
    assert called_task is task
    print("[TEST] OK test_save_atribui_id")

def test_save_chama_storage_add(mocker):
    print("[TEST] Iniciando test_save_chama_storage_add")
    mock_storage = mocker.Mock()
    task = Task(None, "Teste2", "Desc", Priority.ALTA, datetime.now() + timedelta(minutes=10), Status.CONCLUIDA)
    repo = Task_Repository(mock_storage)

    print("[TEST] Chamando repo.save(task)...")
    repo.save(task)
    mock_storage.add.assert_called_once_with(task.id, task)
    assert task.id == 1
    assert task.titulo == "Teste2"
    print(f"[TEST] OK test_save_chama_storage_add | task.id={task.id}")

def test_find_by_id(mocker):
    print("[TEST] Iniciando test_find_by_id")
    mock_storage = mocker.Mock()
    repo = Task_Repository(mock_storage)

    print("[TEST] Chamando repo.find_by_id(20)")
    repo.find_by_id(20)
    mock_storage.get.assert_called_once_with(20)
    print("[TEST] OK test_find_by_id")

def test_find_all(mocker):
    print("[TEST] Iniciando test_find_all")
    mock_storage = mocker.Mock()
    repo = Task_Repository(mock_storage)
    task = Task(None, "Teste3", "Desc", Priority.MEDIA, datetime.now() + timedelta(minutes=15), Status.PENDENTE)

    mock_storage.get_all.return_value = [task]
    print("[TEST] Chamando repo.find_all()")
    result = repo.find_all()

    mock_storage.get_all.assert_called_once()
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] is task
    print(f"[TEST] OK test_find_all | total={len(result)}")

def test_repository_setup_teardown():
    print("[TEST] Iniciando test_repository_setup_teardown")
    storage_falso = Mock()
    repo = Task_Repository(storage_falso)
    print("[TEST] Repo criado")
    assert repo is not None
    assert hasattr(repo, "_Task_Repository__next_id")
    assert repo._Task_Repository__next_id == 1
    del repo
    print("[TEST] Repo removido (teardown)")
    print("[TEST] OK test_repository_setup_teardown")

def test_repository_encapsulamento():
    print("[TEST] Iniciando test_repository_encapsulamento")
    storage_falso = Mock()
    storage_falso.get_all.return_value = []
    repo = Task_Repository(storage_falso)
    prazo = datetime.now() + timedelta(hours=1)
    t = Task(None, "Encap", "Teste", Priority.BAIXA, prazo, Status.PENDENTE)

    print("[TEST] Salvando via save()")
    repo.save(t)
    assert t.id == 1

    print("[TEST] Buscando via find_by_id()")
    repo.find_by_id(t.id)

    print("[TEST] Listando via find_all()")
    repo.find_all()

    print("[TEST] Removendo via delete()")
    repo.delete(t.id)

    storage_falso.add.assert_called_once_with(t.id, t)
    storage_falso.get.assert_called_once_with(t.id)
    storage_falso.get_all.assert_called_once()
    storage_falso.delete.assert_called_once_with(t.id)
    print("[TEST] OK test_repository_encapsulamento")

def test_repository_isolamento_dependencias():
    print("[TEST] Iniciando test_repository_isolamento_dependencias")
    storage_falso = Mock()
    repo = Task_Repository(storage_falso)
    prazo = datetime.now() + timedelta(hours=1)
    t = Task(None, "Iso", "Dep", Priority.MEDIA, prazo, Status.PENDENTE)

    print("[TEST] save() com storage mock")
    repo.save(t)
    storage_falso.add.assert_called_once_with(t.id, t)
    assert t.id == 1

    storage_falso.get.return_value = t
    print("[TEST] find_by_id() retorna a mesma instância do mock")
    repo.find_by_id(t.id)
    storage_falso.get.assert_called_once_with(1)
    print("[TEST] OK test_repository_isolamento_dependencias")

def test_repository_interacao_metodos():
    print("[TEST] Iniciando test_repository_interacao_metodos")
    storage_falso = Mock()
    repo = Task_Repository(storage_falso)
    prazo = datetime.now() + timedelta(hours=1)
    t = Task(None, "Fluxo", "Seq", Priority.ALTA, prazo, Status.PENDENTE)

    print("[TEST] Salvando tarefa")
    repo.save(t)
    assert t.id == 1

    print("[TEST] Buscando por id")
    repo.find_by_id(t.id)

    print("[TEST] Listando todas")
    storage_falso.get_all.return_value = [t]
    all_items = repo.find_all()
    assert isinstance(all_items, list)
    assert len(all_items) == 1

    print("[TEST] Deletando por id")
    repo.delete(t.id)

    storage_falso.add.assert_called_once_with(t.id, t)
    storage_falso.get.assert_called_once_with(t.id)
    storage_falso.get_all.assert_called_once()
    storage_falso.delete.assert_called_once_with(t.id)
    print("[TEST] OK test_repository_interacao_metodos")

def test_repository_polimorfismo_storage_simples():
    print("[TEST] Iniciando test_repository_polimorfismo_storage_simples")
    class MeuStorageSimples:
        def __init__(self):
            self.data = {}
        def add(self, k, v): 
            self.data[k] = v
        def get(self, k): 
            return self.data.get(k)
        def get_all(self): 
            return list(self.data.values())
        def delete(self, k): 
            existed = k in self.data
            if existed:
                del self.data[k]
            return existed

    storage = MeuStorageSimples()
    repo = Task_Repository(storage)
    prazo = datetime.now() + timedelta(hours=1)
    t = Task(None, "Poly", "Store", Priority.MEDIA, prazo, Status.PENDENTE)

    print("[TEST] Usando storage alternativo")
    repo.save(t)
    assert t.id == 1
    assert storage.get(1) is t

    ok = repo.delete(t.id)
    assert ok is True
    assert storage.get(1) is None
    print("[TEST] OK test_repository_polimorfismo_storage_simples")

def test_repository_ciclo_de_vida_ids_incremento():
    print("[TEST] Iniciando test_repository_ciclo_de_vida_ids_incremento")
    storage_falso = Mock()
    storage_falso.get_all.return_value = []
    repo = Task_Repository(storage_falso)

    p = datetime.now() + timedelta(hours=1)
    t1 = Task(None, "A", "Desc", Priority.BAIXA, p, Status.PENDENTE)
    t2 = Task(None, "B", "Desc", Priority.MEDIA, p, Status.PENDENTE)

    print("[TEST] Salvando t1")
    repo.save(t1)
    print("[TEST] Salvando t2")
    repo.save(t2)

    print(f"[TEST] IDs gerados | t1.id={t1.id} t2.id={t2.id}")
    assert t1.id == 1
    assert t2.id == 2
    assert t1 is not t2

    print("[TEST] Deletando t1 e listando novamente")
    repo.delete(t1.id)
    repo.find_all()

    storage_falso.add.assert_any_call(1, t1)
    storage_falso.add.assert_any_call(2, t2)
    storage_falso.delete.assert_called_with(1)
    storage_falso.get_all.assert_called()
    print("[TEST] OK test_repository_ciclo_de_vida_ids_incremento")