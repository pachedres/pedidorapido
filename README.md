# PedidoRápido — Docker Swarm

## Arquitetura

```
Internet
   │
   ▼
[ Nginx :80 ]  ← load balancer
   │
   ├──▶ [ web.1 Flask :5000 ]
   ├──▶ [ web.2 Flask :5000 ]  ← réplicas do serviço web
   ├──▶ [ web.3 Flask :5000 ]
   ├──▶ [ web.4 Flask :5000 ]
   └──▶ [ web.5 Flask :5000 ]
              │
              ▼
         [ Redis :6379 ]  ← estado compartilhado
```

**Serviços:**
- **nginx** — recebe as requisições na porta 80 e distribui entre as réplicas
- **web** — aplicação Flask que conta acessos e exibe o hostname do container
- **redis** — armazena o contador de visitas compartilhado entre todas as réplicas

**Rede:** `pedido-net` (overlay) — permite comunicação interna entre os serviços

---

## Estrutura de arquivos

```
pedidorapido/
├── app/
│   ├── app.py            ← aplicação Flask
│   ├── requirements.txt  ← dependências Python
│   └── Dockerfile        ← imagem do serviço web
├── nginx/
│   └── nginx.conf        ← configuração do load balancer
├── docker-stack.yml      ← deploy
└── README.md
```

## Como executar

### Pré-requisitos

- Docker instalado (`docker --version`)
- Docker Swarm inicializado

### 1. Build da imagem

```bash
docker build -t pedidorapido-web ./app
```

### 2. Inicializar o Swarm

```bash
docker swarm init
# Se houver múltiplos IPs na interface:
docker swarm init --advertise-addr <SEU_IP>
```

### Docker Stack

```bash
docker stack deploy -c docker-stack.yml pedidorapido
```

### 3. Verificar status

```bash
docker service ls
```

Acesse **http://localhost** no navegador.


## Escalando

```bash
# Escalar para 5 réplicas
docker service scale web=5

# Verificar
docker service ps web
```

Recarregue o navegador várias vezes — o campo **"Respondido por"** alterna entre hostnames diferentes (Nginx distribuindo a carga), mas o contador continua em sequência (Redis compartilhado).


## Simulando falha (Self-Healing)

```bash
# Listar containers
docker ps --filter name=web

# Matar um container à força
docker rm -f <CONTAINER_ID>

# Observar o Swarm recriar automaticamente
docker service ps web
```

O Swarm detecta que o número de réplicas caiu abaixo do desejado e recria o container automaticamente.

## Encerrando

```bash
docker stack rm pedidorapido
docker swarm leave --force
```
