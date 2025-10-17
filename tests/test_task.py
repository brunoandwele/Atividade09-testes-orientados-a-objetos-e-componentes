import pytest
from datetime import datetime, timedelta
from task_manager.Task import Task, Priority, Status

def test_task_valida():
    print("[TEST] Iniciando test_task_valida")
    prazo = datetime.now() + timedelta(days=1)
    task = Task(None, "Estudar", "Python", Priority.ALTA, prazo, Status.EM_PROGRESSO)
    print(f"[TEST] Pré-validação | id={task.id} titulo={task.titulo} prioridade={task.prioridade} prazo={task.prazo} status={task.status}")
    task.validar()
    print(f"[TEST] Pós-validação | titulo={task.titulo} status={task.status}")
    assert task.titulo == "Estudar"
    assert isinstance(task.descricao, str)
    assert task.prioridade == Priority.ALTA
    assert task.prazo > datetime.now()
    assert task.status == Status.EM_PROGRESSO
    print("[TEST] OK test_task_valida")

def test_task_valida_2():
    print("[TEST] Iniciando test_task_valida_2")
    prazo = datetime.now() + timedelta(days=3)
    task = Task(2, "Treinar", "C", Priority.ALTA, prazo, Status.CONCLUIDA)
    print(f"[TEST] Pré-validação | id={task.id} titulo={task.titulo} status={task.status}")
    task.validar()
    print(f"[TEST] Pós-validação | id={task.id}")
    assert task.id is not None
    assert isinstance(task.id, int)
    assert task.id == 2
    assert task.status == Status.CONCLUIDA
    assert task.prazo > datetime.now()
    print("[TEST] OK test_task_valida_2")

def test_titulo_curto_invalido():
    print("[TEST] Iniciando test_titulo_curto_invalido")
    prazo = datetime.now() + timedelta(days=1)
    task = Task(None, "AB", "Desc", Priority.BAIXA, prazo, Status.PENDENTE)
    print("[TEST] Chamando task.validar() e esperando erro por título curto (<3)")
    with pytest.raises(ValueError) as exc:
        task.validar()
    msg = str(exc.value)
    print(f"[TEST] Erro esperado capturado | msg={msg}")
    assert "3 caracteres" in msg or "menor de 3" in msg
    assert task.status == Status.PENDENTE
    print("[TEST] OK test_titulo_curto_invalido")

def test_titulo_curto_invalido_2():
    print("[TEST] Iniciando test_titulo_curto_invalido_2")
    prazo = datetime.now() + timedelta(days=1)
    task = Task(None, "ABCD", "Desc", Priority.BAIXA, prazo, Status.PENDENTE)
    print("[TEST] Chamando task.validar() e esperando erro por título com 4 caracteres")
    with pytest.raises(ValueError) as exc:
        task.validar()
    msg = str(exc.value)
    print(f"[TEST] Erro esperado capturado | msg={msg}")
    assert "4 caracteres" in msg
    assert isinstance(task.prioridade, Priority)
    print("[TEST] OK test_titulo_curto_invalido_2")

def test_prazo_passado():
    print("[TEST] Iniciando test_prazo_passado")
    prazo = datetime.now() - timedelta(days=1)
    task = Task(None, "ESTUDAR", "Testes", Priority.MEDIA, prazo, Status.PENDENTE)
    print("[TEST] Chamando task.validar() e esperando erro por prazo no passado")
    with pytest.raises(ValueError) as exc:
        task.validar()
    msg = str(exc.value)
    print(f"[TEST] Erro esperado capturado | msg={msg}")
    assert "Prazo" in msg or "passado" in msg or "incorreto" in msg
    assert task.prioridade == Priority.MEDIA
    print("[TEST] OK test_prazo_passado")

# Criação e limpeza de um objeto (setup/teardown)
def test_setup_teardown():
    print("[TEST] Iniciando test_setup_teardown")
    prazo = datetime.now() + timedelta(hours=2)
    task = Task(None, "Estudar", "Python", Priority.ALTA, prazo, Status.PENDENTE)
    print(f"[TEST] Objeto criado | id={task.id} titulo={task.titulo} status={task.status}")
    task.validar()
    print(f"[TEST] Validação concluída | prazo_futuro={(task.prazo > datetime.now())}")
    assert task.prazo > datetime.now()
    assert isinstance(task.titulo, str)
    del task
    print("[TEST] Objeto removido (teardown)")
    print("[TEST] OK test_setup_teardown")

# Encapsulamento: usar apenas interface pública e checar campos
def test_encapsulamento():
    print("[TEST] Iniciando test_encapsulamento")
    prazo = datetime.now() + timedelta(days=1)
    task = Task(None, "Revisar", "Estudo", Priority.MEDIA, prazo, Status.PENDENTE)
    print(f"[TEST] Pré-validação | titulo={task.titulo}")
    task.validar()
    print(f"[TEST] Pós-validação | titulo={task.titulo}")
    assert task.titulo == "Revisar"
    assert isinstance(task.status, Status)
    assert isinstance(task.prioridade, Priority)
    print("[TEST] OK test_encapsulamento | titulo=", task.titulo)

# Classe isolada, sem dependências externas (sanidade básica extra)
def test_isolamento_dependencias():
    print("[TEST] Iniciando test_isolamento_dependencias")
    prazo = datetime.now() + timedelta(hours=1)
    task = Task(None, "Treinar", "Sem dependências", Priority.BAIXA, prazo, Status.PENDENTE)
    print(f"[TEST] Antes validar | prioridade={task.prioridade} status={task.status}")
    task.validar()
    print(f"[TEST] Depois validar | prioridade={task.prioridade} status={task.status}")
    assert task.prioridade in (Priority.BAIXA, Priority.MEDIA, Priority.ALTA)
    assert task.status == Status.PENDENTE
    print("[TEST] OK test_isolamento_dependencias")

# Sequência de mudanças entre métodos (checar estados em cada passo)
def test_interacao_entre_metodos():
    print("[TEST] Iniciando test_interacao_entre_metodos")
    prazo = datetime.now() + timedelta(hours=2)
    task = Task(None, "Aprender", "Sequência de validações", Priority.ALTA, prazo, Status.PENDENTE)
    print(f"[TEST] Passo 1 | status={task.status}")
    task.validar()
    assert task.status == Status.PENDENTE

    task.status = Status.EM_PROGRESSO
    print(f"[TEST] Passo 2 | status={task.status}")
    task.validar()
    assert task.status == Status.EM_PROGRESSO

    task.status = Status.CONCLUIDA
    print(f"[TEST] Passo 3 | status={task.status}")
    task.validar()
    assert task.status == Status.CONCLUIDA

    assert task.prazo > datetime.now()
    print("[TEST] OK test_interacao_entre_metodos")

# Herança e polimorfismo: subclasse simples e checagens adicionais
def test_heranca_polimorfismo():
    print("[TEST] Iniciando test_heranca_polimorfismo")
    class SubTask(Task):
        def mensagem(self):
            return "Sou uma subtarefa"

    prazo = datetime.now() + timedelta(hours=1)
    sub = SubTask(None, "Subclasse", "Herança simples", Priority.MEDIA, prazo, Status.PENDENTE)
    print(f"[TEST] Subclasse criada | type={type(sub).__name__} titulo={sub.titulo}")
    assert sub.mensagem() == "Sou uma subtarefa"
    sub.validar()
    assert isinstance(sub, Task)
    assert isinstance(sub.status, Status)
    assert sub.prazo > datetime.now()
    print("[TEST] OK test_heranca_polimorfismo")

# Ciclo de vida do objeto: garantir transições e consistência final
def test_ciclo_de_vida():
    print("[TEST] Iniciando test_ciclo_de_vida")
    prazo = datetime.now() + timedelta(hours=3)
    task = Task(None, "Ciclo", "Mudança de estados", Priority.ALTA, prazo, Status.PENDENTE)
    print(f"[TEST] Estado inicial: {task.status}")
    assert task.status == Status.PENDENTE

    task.status = Status.EM_PROGRESSO
    print(f"[TEST] Estado alterado: {task.status}")
    task.validar()
    assert task.status == Status.EM_PROGRESSO

    task.status = Status.CONCLUIDA
    print(f"[TEST] Estado alterado: {task.status}")
    task.validar()
    assert task.status == Status.CONCLUIDA

    assert isinstance(task.titulo, str)
    assert task.prazo > datetime.now()
    assert task.prioridade == Priority.ALTA
    print("[TEST] OK test_ciclo_de_vida")