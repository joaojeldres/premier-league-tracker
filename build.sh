#!/bin/bash

set -e

TEMPORADA=${1:-2023-2024}

echo "========================================"
echo " PREMIER LEAGUE & TOP LEAGUES TRACKER"
echo " Temporada consultada: $TEMPORADA"
echo "========================================"

if [ -z "$SPORTSDB_API_KEY" ]; then
    echo "ERROR: falta la variable de entorno SPORTSDB_API_KEY"
    echo "Ejecuta primero:"
    echo "export SPORTSDB_API_KEY=\"3\""
    exit 1
fi

echo "=== Generando Dockerfile ==="

cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt

ENV PIP_PROGRESS_BAR=off

RUN python -m pip install --upgrade pip --no-cache-dir --progress-bar off
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

CMD ["python", "app.py"]
EOF

echo "=== Construyendo imagen Docker ==="
docker build -t football-app .

echo "=== Eliminando contenedores anteriores si existen ==="
docker rm -f football1 football2 football3 football4 2>/dev/null || true

echo "=== Ejecutando 4 contenedores ==="

docker run --name football1 \
  -e SPORTSDB_API_KEY="$SPORTSDB_API_KEY" \
  -e LEAGUE_ID="4328" \
  -e LEAGUE_NAME="Premier League" \
  -e SEASON="$TEMPORADA" \
  -e TOP_LIMIT="5" \
  football-app

docker run --name football2 \
  -e SPORTSDB_API_KEY="$SPORTSDB_API_KEY" \
  -e LEAGUE_ID="4335" \
  -e LEAGUE_NAME="La Liga" \
  -e SEASON="$TEMPORADA" \
  -e TOP_LIMIT="5" \
  football-app

docker run --name football3 \
  -e SPORTSDB_API_KEY="$SPORTSDB_API_KEY" \
  -e LEAGUE_ID="4332" \
  -e LEAGUE_NAME="Serie A" \
  -e SEASON="$TEMPORADA" \
  -e TOP_LIMIT="5" \
  football-app

docker run --name football4 \
  -e SPORTSDB_API_KEY="$SPORTSDB_API_KEY" \
  -e LEAGUE_ID="4331" \
  -e LEAGUE_NAME="Bundesliga" \
  -e SEASON="$TEMPORADA" \
  -e TOP_LIMIT="5" \
  football-app

echo "=== Generando output.txt ==="

{
  echo "=============================="
  echo " TEMPORADA CONSULTADA"
  echo "=============================="
  echo "$TEMPORADA"

  echo ""
  echo "=============================="
  echo " SALIDA docker ps -a"
  echo "=============================="
  docker ps -a

  echo ""
  echo "=============================="
  echo " LOGS football1 - Premier League"
  echo "=============================="
  docker logs football1

  echo ""
  echo "=============================="
  echo " LOGS football2 - La Liga"
  echo "=============================="
  docker logs football2

  echo ""
  echo "=============================="
  echo " LOGS football3 - Serie A"
  echo "=============================="
  docker logs football3

  echo ""
  echo "=============================="
  echo " LOGS football4 - Bundesliga"
  echo "=============================="
  docker logs football4
} > output.txt

echo "=== Proceso finalizado correctamente ==="
echo "Puedes revisar los resultados con:"
echo "cat output.txt"
