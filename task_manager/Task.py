from enum import Enum
from enum import IntEnum
from datetime import datetime, timezone

class Priority(IntEnum):
    BAIXA = 1
    MEDIA = 2
    ALTA = 3

class Status(Enum):
    PENDENTE = "pendente"
    EM_PROGRESSO = "em_progresso"
    CONCLUIDA = "concluida"


# Classe Task Atributos:
# • id: int ou None
# • titulo: str
# • descricao: str
# • prioridade: Priority
# • prazo: datetime
# • status: Status (padrão: PENDENTE)

class Task():
    def __init__(self, id, titulo, descricao, prioridade, prazo, status = Status.PENDENTE):
        print(f"[DEBUG] Inicializando Task | id={id}, titulo={titulo!r}, prioridade={prioridade}, prazo={prazo}, status={status}")
        
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.prazo = prazo
        self.status = status
        
        print(f"[DEBUG] Task criada com sucesso | id={self.id}")

    def validar(self):
        print(f"[DEBUG] Iniciando validação | id={self.id}")

        # --- Título ---
        if self.titulo is None:
            print(f"[ERRO] Título é None")
            raise ValueError("Título é nulo")

        if not isinstance(self.titulo, str):
            print(f"[ERRO] Tipo inválido para título: {type(self.titulo)}")
            raise ValueError("Título deve ser string")

        titulo_strip = self.titulo.strip()
        if len(titulo_strip) < 3:
            print(f"[ERRO] Título com menos de 3 caracteres | titulo={self.titulo!r}")
            raise ValueError("Título menor de 3 caracteres")
        elif len(titulo_strip) == 4:
            print(f"[ERRO] Título com exatamente 4 caracteres | titulo={self.titulo!r}")
            raise ValueError("Título com 4 caracteres")

        # --- Prioridade ---
        if not isinstance(self.prioridade, Priority):
            print(f"[ERRO] Prioridade inválida | valor={self.prioridade!r}")
            raise ValueError("Prioridade inválida")

        # --- Status ---
        if not isinstance(self.status, Status):
            print(f"[ERRO] Status inválido | valor={self.status!r}")
            raise ValueError("Status inválido")

        # --- Prazo ---
        if self.prazo is None:
            print(f"[ERRO] Prazo é None")
            raise ValueError("Prazo é nulo")

        if not isinstance(self.prazo, datetime):
            print(f"[ERRO] Tipo inválido para prazo: {type(self.prazo)}")
            raise ValueError("Prazo deve ser datetime")

        prazo = self.prazo

        now = datetime.now()
        if prazo < now:
            print(f"[ERRO] Prazo no passado | prazo={prazo.isoformat()} | agora={now.isoformat()}")
            raise ValueError("Prazo incorreto")

        print(f"[DEBUG] Validação concluída com sucesso | id={self.id}")
        return 0