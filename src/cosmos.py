# <imports>
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

# </imports>

import json


def getLastRequestCharge(c):
    return c.client_connection.last_response_headers["x-ms-request-charge"]


def runDemo(endpoint, writeOutput):
    # <create_client>
    credential = DefaultAzureCredential()
    client = CosmosClient(url=endpoint, credential=credential)
    # </create_client>

    # <get_database>
    database = client.get_database_client("cosmicworks")
    # </get_database>

    writeOutput(f"Get database:\t{database.id}")

    # <get_container>
    container = database.get_container_client("products")
    # </get_container>
    writeOutput(f"Get container:\t{container.id}")

    # <create_item>
    new_item = {
        "id": "70b63682-b93a-4c77-aad2-65501347265f",
        "category": "gear-surf-surfboards",
        "name": "Yamba Surfboard",
        "quantity": 12,
        "sale": False,
    }
    created_item = container.upsert_item(new_item)
    # </create_item>
    writeOutput(f"Upserted item:\t{created_item}")
    writeOutput("Request charge:\t" f"{getLastRequestCharge(container)}")

    new_item = {
        "id": "25a68543-b90c-439d-8332-7ef41e06a0e0",
        "category": "gear-surf-surfboards",
        "name": "Kiama Classic Surfboard",
        "quantity": 4,
        "sale": True,
    }
    created_item = container.upsert_item(new_item)
    writeOutput(f"Upserted item:\t{created_item}")
    writeOutput(f"Request charge:\t{getLastRequestCharge(container)}")

    # <read_item>
    existing_item = container.read_item(
        item="70b63682-b93a-4c77-aad2-65501347265f",
        partition_key="gear-surf-surfboards",
    )
    # </read_item>
    writeOutput(f"Read item id:\t{existing_item['id']}")
    writeOutput(f"Read item:\t{existing_item}")
    writeOutput(f"Request charge:\t{getLastRequestCharge(container)}")

    # <query_items>
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
    # </query_items>
    # <parse_results>
    items = [item for item in results]
    output = json.dumps(items, indent=True)
    # </parse_results>
    writeOutput("Found items:")
    writeOutput(output, isCode=True)
