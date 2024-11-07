from dotenv import load_dotenv

from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

import json
import os

def getLastRequestCharge(c):
    return c.client_connection.last_response_headers["x-ms-request-charge"]


def runDemo(writeOutput):
    load_dotenv()

    # <create_client>
    endpoint = os.getenv("CONFIGURATION__AZURECOSMOSDB__ENDPOINT")
    if not endpoint:
        raise EnvironmentError("Azure Cosmos DB for NoSQL account endpoint not set.")

    credential = DefaultAzureCredential()
    client = CosmosClient(url=endpoint, credential=credential)
    # </create_client>

    databaseName = os.getenv("CONFIGURATION__AZURECOSMOSDB__DATABASENAME", "cosmicworks")
    database = client.get_database_client(databaseName)

    writeOutput(f"Get database:\t{database.id}")

    containerName = os.getenv("CONFIGURATION__AZURECOSMOSDB__CONTAINERNAME", "products")
    container = database.get_container_client(containerName)

    writeOutput(f"Get container:\t{container.id}")

    new_item = {
        "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        "category": "gear-surf-surfboards",
        "name": "Yamba Surfboard",
        "quantity": 12,
        "sale": False,
    }
    created_item = container.upsert_item(new_item)

    writeOutput(f"Upserted item:\t{created_item}")
    writeOutput("Request charge:\t" f"{getLastRequestCharge(container)}")

    new_item = {
        "id": "bbbbbbbb-1111-2222-3333-cccccccccccc",
        "category": "gear-surf-surfboards",
        "name": "Kiama Classic Surfboard",
        "quantity": 4,
        "sale": True,
    }
    created_item = container.upsert_item(new_item)
    writeOutput(f"Upserted item:\t{created_item}")
    writeOutput(f"Request charge:\t{getLastRequestCharge(container)}")

    existing_item = container.read_item(
        item="aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        partition_key="gear-surf-surfboards",
    )

    writeOutput(f"Read item id:\t{existing_item['id']}")
    writeOutput(f"Read item:\t{existing_item}")
    writeOutput(f"Request charge:\t{getLastRequestCharge(container)}")

    queryText = "SELECT * FROM products p WHERE p.category = @category"
    results = container.query_items(
        query=queryText,
        parameters=[
            dict(
                name="@category",
                value="gear-surf-surfboards",
            )
        ],
        enable_cross_partition_query=False,
    )


    items = [item for item in results]
    output = json.dumps(items, indent=True)

    writeOutput("Found items: ")
    writeOutput(output, isCode=True)
