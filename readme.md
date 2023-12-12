# Quickstart: Azure Cosmos DB for NoSQL client library for Python

This is a simple Flask web application to illustrate common basic usage of Azure Cosmos DB for NoSQL's client library for Python. This sample application accesses an existing account, database, and container using the [`azure-cosmos`](https://pypi.org/project/azure-cosmos/) and [`azure-identity`](https://pypi.org/project/azure-identity/) packages from PyPi. Modify the source code and leverage the Infrastructure as Code (IaC) Bicep assets to get up and running quickly.

When you are finished, you will have a fully functional web application deployed to Azure.

![Screenshot of the deployed web application.](assets/web.png)

### Prerequisites

> This template will create infrastructure and deploy code to Azure. If you don't have an Azure Subscription, you can sign up for a [free account here](https://azure.microsoft.com/free/). Make sure you have the contributor role in the Azure subscription.

The following prerequisites are required to use this application. Please ensure that you have them all installed locally.

- [Azure Developer CLI](https://aka.ms/azd-install)
- [Python 3.11 or newer](https://www.python.org/downloads/) 

### Quickstart

To learn how to get started with any template, follow the steps in [this quickstart](https://learn.microsoft.com/azure/cosmos-db/nosql/quickstart-python) with this template (`cosmos-db-nosql-python-quickstart`).

This quickstart will show you how to authenticate on Azure, initialize using a template, provision infrastructure and deploy code on Azure via the following commands:

```bash
# Log in to azd. Only required once per-install.
azd auth login

# First-time project setup. Initialize a project in the current directory, using this template. 
azd init --template cosmos-db-nosql-python-quickstart

# Provision and deploy to Azure
azd up
```

### Application Architecture

This application utilizes the following Azure resources:

- [**Azure Container Registry**](https://learn.microsoft.com/azure/container-registry/)
    - This services hosts the container image.
- [**Azure Container Apps**](https://learn.microsoft.com/azure/container-apps/)
    - This service hosts the ASP.NET Blazor web application.
- [**Azure Cosmos DB for NoSQL**](https://learn.microsoft.com/azure/cosmos-db/) 
    - This service stores the NoSQL data.

Here's a high level architecture diagram that illustrates these components. Notice that these are all contained within a single **resource group**, that will be created for you when you create the resources.

```mermaid
%%{ init: { 'theme': 'base', 'themeVariables': { 'background': '#243A5E', 'primaryColor': '#50E6FF', 'primaryBorderColor': '#243A5E', 'tertiaryBorderColor': '#50E6FF', 'tertiaryColor': '#243A5E', 'fontFamily': 'Segoe UI', 'lineColor': '#FFFFFF', 'primaryTextColor': '#243A5E', 'tertiaryTextColor': '#FFFFFF' } }}%%
flowchart TB
    subgraph web-app[Azure Container Apps]
        app-framework([Python 3.11 - Flask])
    end
    subgraph cosmos-db[Azure Cosmos DB]
        subgraph database-cosmicworks[Database: cosmicworks]
            subgraph container-products[Container: products]
                prd-yamba[Product: Yamba Surfboard]
                prd-kiama-classic[Product: Kiama Classic Surfboard]
            end
        end
    end
    web-app --> cosmos-db
```



