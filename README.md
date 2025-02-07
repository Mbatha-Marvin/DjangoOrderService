# Project Setup Guide

## Overview

This project is a Django-based Orders application that integrates with Keycloak for authentication using OpenID Connect via the `client_credentials` grant type. The development environment is managed using Podman and Podman Compose, while Kubernetes is provisioned and managed using Ansible.

## Prerequisites

Ensure that you have the following installed:

- **Podman**: [Installation Guide](https://podman.io/getting-started/installation)
  
- **Podman Compose**: Install via pip
  
  ```sh
  pip install podman-compose
  ```
  
- **Ansible**: [Installation Guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
  
- **Python 3.x** (for Django and Ansible playbooks)
  
- **Keycloak** (configured for OpenID authentication)
  

## Environment Configuration

### 1. Setup `.env` File

Create a `.env` file in the root directory based on `example.env`:

```sh
cp example.env .env
```

Edit the `.env` file to set the appropriate values for your environment.

## Running the Project with Podman Compose

### 1. Start the Containers

Ensure Podman is running and execute the following command:

```sh
podman-compose -f compose.yml up -d
```

This will start the Django Orders App along with PostgreSQL and Keycloak.

### 2. Verify Running Containers

To check if the services are running, execute:

```sh
podman ps
```

### 3. Stop Containers

To stop the running services:

```sh
podman-compose -f compose.yml down
```

## Ansible for Kubernetes Setup

The project includes an Ansible playbook to set up Kubernetes clusters.

### 1. Inventory Configuration

The Ansible inventory is managed through SSH configurations, allowing server references by hostname. The inventory file is `dev.ini`, which contains:

```ini
[ubuntu_servers]
ansible-1
```

Ensure that your SSH configuration allows access to the specified servers.

### 2. Run Kubernetes Setup

To provision Kubernetes, execute the Ansible playbook:

```sh
ansible-playbook -i dev.ini setup-kubernetes.yml
```

### 3. Tear Down Kubernetes

To remove the Kubernetes setup, use:

```sh
ansible-playbook -i dev.ini teardown-kubernetes.yml
```

## Keycloak OpenID Configuration

This project uses Keycloak for authentication. The OpenID endpoints are set in the `.env` file:

```sh
OPENID_TOKEN_ENDPOINT='http://keycloak/realms/SavannahInformatics/protocol/openid-connect/token'
OPENID_INTROSPECT_URL='http://keycloak/realms/SavannahInformatics/protocol/openid-connect/token/introspect'
```

Ensure your Keycloak server is running and properly configured for OpenID Connect.

## CI/CD Configuration

The project includes a CI/CD pipeline defined in `ci.yml`. Ensure your CI/CD environment is properly set up to execute this workflow.

## Troubleshooting

1. **Containers not starting?**
  
  - Check logs using `podman logs <container_id>`
  - Ensure Podman is installed and running
2. **Kubernetes setup issues?**
  
  - Verify SSH connectivity to inventory hosts
  - Check Ansible logs for errors
3. **Authentication issues?**
  
  - Confirm Keycloak configuration matches `.env` settings
  - Ensure the Keycloak server is accessible