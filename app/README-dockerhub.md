# Orders Service

A Django-based RESTful service for managing customers and orders with OpenID (Keycloak) authentication integration.

## Image Information

- Base Image: `python:3.12-alpine`
- Package Manager: `uv` (from astral-sh)
- Exposed Port: 8881

## Environment Variables

### Required Environment Variables

```env
# Django Database Configuration
DJANGO_POSTGRESQL_DATABASE=orders_db
DJANGO_POSTGRESQL_USERNAME=postgres
DJANGO_POSTGRESQL_PASSWORD=your-password
DJANGO_POSTGRESQL_HOSTNAME=db
DJANGO_POSTGRESQL_PORT_NUMBER=5432
DJANGO_PORT=8881

# Keycloak Configuration
KEYCLOAK_POSTGRESQL_HOSTNAME=keycloak-db
KEYCLOAK_POSTGRESQL_PORT=5432
KEYCLOAK_CONTAINER_HOSTNAME=keycloak
KEYCLOAK_INTERNAL_HTTP_PORT=8080

# OpenID Authentication
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
OPENID_TOKEN_ENDPOINT=http://your-auth-server/token
OPENID_INTROSPECT_URL=http://your-auth-server/introspect

# Africa's Talking API
AT_API_KEY=your-at-api-key
AT_USERNAME=your-at-username
AT_TEST_PHONENUMBER=your-test-phone
```

## Quick Start

### Using Docker Run

```bash
docker run -d \
  --name orders-service \
  -p 8881:8881 \
  -e DJANGO_POSTGRESQL_DATABASE=orders_db \
  -e DJANGO_POSTGRESQL_USERNAME=postgres \
  -e DJANGO_POSTGRESQL_PASSWORD=your-password \
  -e DJANGO_POSTGRESQL_HOSTNAME=db \
  -e DJANGO_POSTGRESQL_PORT_NUMBER=5432 \
  -e DJANGO_PORT=8881 \
  -e KEYCLOAK_POSTGRESQL_HOSTNAME=keycloak-db \
  -e KEYCLOAK_POSTGRESQL_PORT=5432 \
  -e KEYCLOAK_CONTAINER_HOSTNAME=keycloak \
  -e KEYCLOAK_INTERNAL_HTTP_PORT=8080 \
  mbathamarvin/orders-service:latest
```

### Using Docker Compose

```yaml
version: '3.8'

services:
  orders-service:
    image: mbathamarvin/orders-service:latest
    ports:
      - "8881:8881"
    environment:
      - DJANGO_POSTGRESQL_DATABASE=orders_db
      - DJANGO_POSTGRESQL_USERNAME=postgres
      - DJANGO_POSTGRESQL_PASSWORD=your-password
      - DJANGO_POSTGRESQL_HOSTNAME=db
      - DJANGO_POSTGRESQL_PORT_NUMBER=5432
      - DJANGO_PORT=8881
      - KEYCLOAK_POSTGRESQL_HOSTNAME=keycloak-db
      - KEYCLOAK_POSTGRESQL_PORT=5432
      - KEYCLOAK_CONTAINER_HOSTNAME=keycloak
      - KEYCLOAK_INTERNAL_HTTP_PORT=8080
    depends_on:
      - db
      - keycloak
    healthcheck:
      test: ["CMD", "nc", "-z", "localhost", "8881"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=${DJANGO_POSTGRESQL_DATABASE}
      - POSTGRES_USER=${DJANGO_POSTGRESQL_USERNAME}
      - POSTGRES_PASSWORD=${DJANGO_POSTGRESQL_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  keycloak-db:
    image: postgres:13
    environment:
      - POSTGRES_DB=keycloak
      - POSTGRES_USER=keycloak
      - POSTGRES_PASSWORD=your-keycloak-db-password

  keycloak:
    image: quay.io/keycloak/keycloak:latest
    environment:
      - KC_DB=postgres
      - KC_DB_URL=jdbc:postgresql://keycloak-db:5432/keycloak
      - KC_DB_USERNAME=keycloak
      - KC_DB_PASSWORD=your-keycloak-db-password
      - KEYCLOAK_ADMIN=admin
      - KEYCLOAK_ADMIN_PASSWORD=admin
    depends_on:
      - keycloak-db
    ports:
      - "8882:8080"
```

## Container Behavior

The container uses an entrypoint script that:

1. Waits for PostgreSQL database to be ready
2. Runs Django migrations
3. Waits for Keycloak database and service
4. Runs pytest tests
5. Starts the Gunicorn server

## API Endpoints

### Customers
- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create a new customer
- `GET /api/customers/{id}/` - Retrieve a customer
- `PUT /api/customers/{id}/` - Update a customer
- `DELETE /api/customers/{id}/` - Delete a customer

### Orders
- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create a new order
- `GET /api/orders/{id}/` - Retrieve an order
- `PUT /api/orders/{id}/` - Update an order
- `DELETE /api/orders/{id}/` - Delete an order

## Health Check

The container includes a health check that verifies the application is running on port 8881. You can monitor the container health using:

```bash
docker inspect --format='{{json .State.Health}}' orders-service
```

## Troubleshooting

1. Container fails to start:
   - Check if PostgreSQL and Keycloak services are accessible
   - Verify environment variables are correctly set
   - Check container logs: `docker logs orders-service`

2. Database connection issues:
   - Ensure PostgreSQL containers are running and healthy
   - Verify database credentials
   - Check network connectivity between containers

3. Keycloak authentication issues:
   - Verify Keycloak is running and accessible
   - Check client credentials
   - Ensure Keycloak realm is properly configured

## Version History

- 0.1.0: Initial release
  - Basic CRUD operations for customers and orders
  - Keycloak integration
  - Africa's Talking API integration

## Security Notes

1. Use secure passwords in production
2. Enable SSL/TLS in production
3. Configure proper firewall rules
4. Regularly update the image to get security patches

