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


@app.route("/")
def index():
    return render_template("index.html")


# <environment_variables>
endpoint = os.getenv("ENDPOINT")
# </environment_variables>

print(f"ENDPOINT: {endpoint}")


@socket.on("start", namespace="/cosmos-db-nosql")
def start(data):
    # <create_client>
    credential = DefaultAzureCredential()
    client = CosmosClient(url=endpoint, credential=credential)
    # </create_client>
    emit("new_message", {"message": "Client connected."})

    # <get_database>
    database = client.get_database_client(id="cosmicworks")
    # </get_database>

    emit("new_message", {"message": f"Database [{database.id}] exists."})

    # <get_container>
    container = database.get_container_client(id="products")
    # </get_container>
    emit("new_message", {"message": f"Container [{container.id}] exists."})

    # <create_item>
    new_item = {
        "id": "70b63682-b93a-4c77-aad2-65501347265f",
        "categoryId": "61dba35b-4f02-45c5-b648-c6badc0cbd79",
        "categoryName": "gear-surf-surfboards",
        "name": "Yamba Surfboard",
        "quantity": 12,
        "sale": False,
    }
    created_item = container.upsert_item(new_item)
    # </create_item>
    emit(
        "new_message",
        {"message": f"New item [{created_item['name']}] upserted."},
    )

    new_item = {
        "id": "25a68543-b90c-439d-8332-7ef41e06a0e0",
        "categoryId": "61dba35b-4f02-45c5-b648-c6badc0cbd79",
        "categoryName": "gear-surf-surfboards",
        "name": "Kiama Classic Surfboard",
        "quantity": 4,
        "sale": True,
    }
    created_item = container.upsert_item(new_item)
    emit(
        "new_message",
        {"message": f"New item [{created_item['name']}] upserted."},
    )

    # <read_item>
    existing_item = container.read_item(
        item="70b63682-b93a-4c77-aad2-65501347265f",
        partition_key="61dba35b-4f02-45c5-b648-c6badc0cbd79",
    )
    # </read_item>
    emit(
        "new_message",
        {
            "message": (
                f"Performed a point read of item [{existing_item['name']}]."
            )
        },
    )

    # <query_items>
    queryText = "SELECT * FROM products p WHERE p.categoryId = @categoryId"
    results = container.query_items(
        query=queryText,
        parameters=[
            dict(
                name="@categoryId",
                value="61dba35b-4f02-45c5-b648-c6badc0cbd79",
            )
        ],
        enable_cross_partition_query=False,
    )
    # </query_items>
    # <parse_results>
    items = [item for item in results]
    output = json.dumps(items, indent=True)
    # </parse_results>
    emit("new_message", {"message": "NoSQL query performed."})
    emit("new_message", {"code": True, "message": queryText})
    emit("new_message", {"code": True, "message": output})


if __name__ == "__main__":
    socket.run(
        app,
        port=os.getenv("PORT", default=5000),
        debug=os.getenv("DEBUG", default=True),
        host="0.0.0.0",
    )
