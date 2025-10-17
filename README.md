# Task Manager - Sistema de Gerenciamento de Tarefas (com Testes Unitários)

Este projeto é um **gerenciador de tarefas simples**, desenvolvido em **Python** com foco em **boas práticas de orientação a objetos e testes automatizados**.  
O objetivo é demonstrar a implementação de uma estrutura modular composta por **entidades, repositórios e armazenamento**, com cobertura completa de testes via **pytest**.

---

## Funcionalidades Principais

- Criação de tarefas com prioridade, descrição, prazo e status.  
- Validação de dados (título mínimo, prazo futuro etc.).  
- Repositório que gerencia IDs e operações CRUD simuladas.  
- Armazenamento em memória simulando persistência de dados.  
- Testes abrangendo desde a criação até o ciclo de vida completo das tarefas.

---

## Instalação

Clone o repositório e instale as dependências:

```bash
pip install -r requirements.txt
```

Esse comando irá instalar as depdendencias do projeto:

```bash
pytest==7.4.0
pytest-cov==4.0.0
pytest-mock==3.11.1
```

---
## Execução dos teses
```bash
pytest -v #Executar sem logs
```

```bash
pytest -v -s #Executar com logs
```

---
## Estreutura do projeto
```
Atividade_9_Testes_att/
│
├── task_manager/
│   ├── __init__.py
│   ├── Task.py                # Classe Task com validações e enums Priority/Status
│   ├── repository.py          # Classe Task_Repository (CRUD e controle de IDs)
│   └── storage.py             # Armazenamento em memória (InMemoryStage)
│
├── tests/
│   ├── __init__.py
│   ├── test_task.py           # Testes da classe Task (validação, estados, herança, etc.)
│   └── test_repository.py     # Testes do repositório (CRUD, ciclo de vida, mocks, etc.)
│
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação do projeto
```

---
## Resultados:

<img width="2902" height="1426" alt="image" src="https://github.com/user-attachments/assets/67ce0067-a380-4c63-840e-ebf444fd96c4" />

