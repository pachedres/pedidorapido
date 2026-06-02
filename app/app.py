import os, socket
from flask import Flask, render_template_string
import redis

app = Flask(__name__)

# Conecta ao Redis pelo nome do serviço no Swarm
r = redis.Redis(host="redis", port=6379)

TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="3">
  <title>PedidoRápido</title>
  <style>
    body { font-family: Arial; background: #f0f4f8; display: flex;
           justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .card { background: white; border-radius: 16px; padding: 48px 56px;
            text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,.1); }
    h1   { color: #2563eb; font-size: 2rem; margin: 0 0 8px; }
    .count { font-size: 5rem; font-weight: 800; color: #0ea5e9; line-height: 1; }
    .host  { color: #16a34a; font-size: .9rem; margin-top: 24px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>🐳 PedidoRápido</h1>
    <p>Total de acessos</p>
    <div class="count">{{ count }}</div>
    <p class="host">Respondido por: <strong>{{ host }}</strong></p>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    count = r.incr("visitas")       # incrementa atomicamente no Redis
    host  = socket.gethostname()    # hostname único de cada container
    return render_template_string(TEMPLATE, count=count, host=host)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
