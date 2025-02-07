#!/bin/sh

wait_for_service() {
  local host=$1
  local port=$2
  local name=$3
  local retries=30  # Maximum retries (adjust as needed)

  echo "Waiting for $name at $host:$port..."

  while ! nc -z "$host" "$port"; do
    retries=$((retries - 1))
    if [ "$retries" -le 0 ]; then
      echo "$name is not available after multiple attempts. Exiting..."
      exit 1
    fi
    sleep 5
  done

  echo "$name is up!"
}

echo "Django DB Host: ${DJANGO_POSTGRESQL_HOSTNAME}"
echo "Django Db Port: ${DJANGO_POSTGRESQL_PORT_NUMBER}"
wait_for_service "${DJANGO_POSTGRESQL_HOSTNAME}" "${DJANGO_POSTGRESQL_PORT_NUMBER}" "PostgreSQL"

echo "Running migrations..."
uv run python manage.py migrate

echo "Keycloak DB Host: ${KEYCLOAK_POSTGRESQL_HOSTNAME}"
echo "Keycloak DB Port: ${KEYCLOAK_POSTGRESQL_PORT}"
wait_for_service "${KEYCLOAK_POSTGRESQL_HOSTNAME}" "${KEYCLOAK_POSTGRESQL_PORT}" "Keycloak Database"

echo "Waiting for Keycloak service..."
wait_for_service "${KEYCLOAK_CONTAINER_HOSTNAME}" "${KEYCLOAK_INTERNAL_HTTP_PORT}" "Keycloak"

echo "Running Tests"
uv run pytest


echo "Starting the application..."
echo "Django Port: ${DJANGO_PORT}"
exec uv run gunicorn core.wsgi:application --bind 0.0.0.0:${DJANGO_PORT}
