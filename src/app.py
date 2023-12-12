from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# <imports>
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

# </imports>

import os
import json

app = Flask(__name__)

socket = SocketIO(app)


# <environment_variables>
endpoint = os.getenv("COSMOS_DB_ENDPOINT")
# </environment_variables>

print(f"ENDPOINT: {endpoint}")


def getLastRequestCharge(c):
    return c.client_connection.last_response_headers["x-ms-request-charge"]


@app.route("/")
def index():
    return render_template("index.html", endpoint=endpoint)


@socket.on("start", namespace="/cosmos-db-nosql")
def start(data):
    emit("new_message", {"message": "Current Status:\tStarting..."})

    # <create_client>
    credential = DefaultAzureCredential()
    client = CosmosClient(url=endpoint, credential=credential)
    # </create_client>

    # <get_database>
    database = client.get_database_client("cosmicworks")
    # </get_database>

    emit("new_message", {"message": f"Get database:\t{database.id}"})

    # <get_container>
    container = database.get_container_client("products")
    # </get_container>
    emit("new_message", {"message": f"Get container:\t{container.id}"})

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
    emit(
        "new_message",
        {"message": f"Upserted item:\t{created_item}"},
    )
    emit(
        "new_message",
        {
            "message": (
                "Request charge:\t" f"{getLastRequestCharge(container)}"
            )
        },
    )

    new_item = {
        "id": "25a68543-b90c-439d-8332-7ef41e06a0e0",
        "category": "gear-surf-surfboards",
        "name": "Kiama Classic Surfboard",
        "quantity": 4,
        "sale": True,
    }
    created_item = container.upsert_item(new_item)
    emit(
        "new_message",
        {"message": f"Upserted item:\t{created_item}"},
    )
    emit(
        "new_message",
        {"message": f"Request charge:\t{getLastRequestCharge(container)}"},
    )

    # <read_item>
    existing_item = container.read_item(
        item="70b63682-b93a-4c77-aad2-65501347265f",
        partition_key="gear-surf-surfboards",
    )
    # </read_item>
    emit(
        "new_message",
        {"message": f"Read item id:\t{existing_item['id']}"},
    )
    emit(
        "new_message",
        {"message": f"Read item:\t{existing_item}"},
    )
    emit(
        "new_message",
        {"message": f"Request charge:\t{getLastRequestCharge(container)}"},
    )

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
    emit("new_message", {"message": "Found items:"})
    emit("new_message", {"code": True, "message": output})


if __name__ == "__main__":
    socket.run(
        app,
        port=os.getenv("PORT", default=5000),
        debug=os.getenv("DEBUG", default=True),
    )
