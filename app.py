from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from azure.cosmos import CosmosClient, PartitionKey

import json

app = Flask(__name__)

socket = SocketIO(app, async_handlers=True)


@app.route("/")
def index():
    return render_template("index.html", sync_mode=socket.async_mode)


endpoint = "https://localhost:8081"
key = (
    "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE"
    "2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
)


@socket.on("start", namespace="/cosmos-db-nosql")
def start(data):
    client = CosmosClient(url=endpoint, credential=key)
    emit("new_message", {"message": "Client connected."})

    database = client.create_database_if_not_exists(id="cosmicworks")
    emit("new_message", {"message": f"Database [{database.id}] exists."})

    container = database.create_container_if_not_exists(
        id="products",
        partition_key=PartitionKey(path="/categoryId"),
        offer_throughput=400,
    )
    emit("new_message", {"message": f"Container [{container.id}] exists."})

    new_item = {
        "id": "70b63682-b93a-4c77-aad2-65501347265f",
        "categoryId": "61dba35b-4f02-45c5-b648-c6badc0cbd79",
        "categoryName": "gear-surf-surfboards",
        "name": "Yamba Surfboard",
        "quantity": 12,
        "sale": False,
    }
    created_item = container.upsert_item(new_item)
    emit(
        "new_message",
        {"message": f"New item [{created_item['name']}] upserted."},
    )

    existing_item = container.read_item(
        item="70b63682-b93a-4c77-aad2-65501347265f",
        partition_key="61dba35b-4f02-45c5-b648-c6badc0cbd79",
    )
    emit(
        "new_message",
        {
            "message": (
                f"Performed a point read of item [{existing_item['name']}]."
            )
        },
    )

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
    items = [item for item in results]
    output = json.dumps(items, indent=True)
    emit("new_message", {"message": "NoSQL query performed."})
    emit("new_message", {"code": True, "message": queryText})
    emit("new_message", {"code": True, "message": output})
