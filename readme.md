<!--
---
page_type: sample
name: "Quickstart: Azure Cosmos DB for NoSQL and Azure SDK for Python"
description: This is a simple Flask web application to illustrate common basic usage of Azure Cosmos DB for NoSQL and the Azure SDK for Python.
urlFragment: template
languages:
- python
- azdeveloper
products:
- azure-cosmos-db
---
-->

# Quickstart: Azure Cosmos DB for NoSQL - Azure SDK for Python

This is a simple Flask web application to illustrate common basic usage of Azure Cosmos DB for NoSQL with the Azure SDK for Python.

## Prerequisites

- [Docker](https://www.docker.com/)
- [Azure Developer CLI](https://aka.ms/azd-install)
- [Python 3.12](https://www.python.org/downloads/)

## Quickstart

1. Log in to Azure Developer CLI. *This is only required once per-install.*

    ```bash
    azd auth login
    ```

1. Initialize this template (`cosmos-db-nosql-python-quickstart`) using `azd init`

    ```bash
    azd init --template cosmos-db-nosql-python-quickstart
    ```

1. Ensure that **Docker** is running in your environment.

1. Use `azd up` to provision your Azure infrastructure and deploy the web application to Azure.

    ```bash
    azd up
    ```

1. Observed the deployed web application

    ![Screenshot of the deployed web application.](assets/web.png)
