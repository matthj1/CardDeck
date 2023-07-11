from time import timezone
from flask import Flask, Response
import random
import datetime
import math
from flask_cors import CORS
from time import sleep

app = Flask(__name__)
CORS(app)

MAX_QUERIES = 15
LOW_QUERIES = 4
increase_queries = True

query_id = 0

hospitals_and_gateways = [
    {"hospital": "Barbados General Hospital", "gateway":"Barbados Hospital Gateway"},
    {"hospital": "UMCSN, Nevada", "gateway": "2PACS Shakur"},
    {"hospital": "Winnipeg General Hospital", "gateway": "PACSman Turner Overdrive"},
    {"hospital": "Guys and St Thomas' Hospital, United Kingdom", "gateway": "Really long PACS name is really long"}
]

transfer_types = [
    "RETRIEVE_STUDY",
    "RETRIEVE_SCAN"
]

response_stages = [
    {
        "query_status" : "NEW"
    },
    {
        "query_status" : "QUE"
    },
    {
        "query_status" : "RUN",
        "response": {"status": "started"}
    },
    {
        "query_status" : "RUN",
        "response": {"status": "retrieving"}
    },
    {
        "query_status" : "RUN",
        "response": {"status": "waiting_silo"}
    },
    {
        "query_status" : "RUN",
        "response": {"status": "collecting"}
    },
    {
        "query_status" : "RUN",
        "response": {"status": "zipping"}
    },
    {
        "query_status" : "RUN",
        "response": {"status": "uploading"}
    },
    {
        "query_status" : "RUN",
        "response": {"status": "upload_transfer_complete"}
    },
    {
        "query_status" : "RUN",
        "response": {"status": "finished"}
    },
    {
        "query_status" : "FIN"
    }
]

query_list = []

@app.route("/")
def get_queries():
    global increase_queries

    for query in query_list:
        progress_query(query)
    
    if len(query_list) >= MAX_QUERIES:
        increase_queries = False

    if len(query_list) <= LOW_QUERIES:
        increase_queries = True
    
    if increase_queries:
        for _ in range(random.randint(1, 4)):
            query_list.append(create_query())

    return query_list

# create queries with a random time till completion. Progress the queries on every request.

@app.route("/breaks_sometimes")
def breaks_sometimes():
    fails = random.choice([True, False, False]) # twice as likely to succeed
    if(fails):
        return Response("I'm broken", status=500)
    else:
        return [{
            "type": "PACS_TRANSFER",
            "id" : "query-anfnjnjndjfnjdgjnjgg",
            "status" : "RUN",
            "query_id": "anfnjnjndjfnjdgjnjgg",
            "hospital": "Unreliable General Hospital",
            "gateway": "Unreliable Gateway",
            "gateway_id": 1234,
            "elapsed": 0,
            "transfer_type": transfer_types[0],
            "query_status": "NEW",
            "response": response_stages[0],
            "timing": 15,
            "created": datetime.datetime.now()
        }]

@app.route("/error")
def error():
    return [{
        "type": "PACS_TRANSFER",
        "id" : "query-anfnjnjndjfnjdg",
        "status" : "ERROR",
        "query_id": "anfnjnjndjfnjdgjnjgg",
        "hospital": "Broken General Hospital, Brokenville",
        "gateway": "Broken Gateway",
        "gateway_id": 1235,
        "elapsed": 0,
        "transfer_type": transfer_types[0],
        "query_status": "ERR",
        "response": {"name" : "GENERIC ERROR", "message": "OH NO!"},
        "timing": 15,
        "created": datetime.datetime.now()
    },
    {
        "type": "PACS_TRANSFER",
        "id" : "query-anfnjnjndjfnjdgijfiji",
        "status" : "WARN",
        "query_id": "anfnjnjndjfnjdgjnjggkfkdokfokf",
        "hospital": "Really Long Hospital Name, United Kingdom",
        "gateway": "Slow Gateway",
        "gateway_id": 1236,
        "elapsed": 0,
        "transfer_type": transfer_types[0],
        "query_status": "RUN",
        "response": {
                "status": "retrieving",
                "total": 5,
                "completed": 3
            },
        "timing": 15,
        "created": datetime.datetime.now()
    }]

@app.route("/agents")
def agents():
    return [
        {
            "type": "AGENT",
            "id": "agent-gifjgijsdfijgif",
            "status": "RUN",
            "hospital": "James Bond Hospital",
            "online": True,
            "full_status": "ONLINE",
            "agent_id": 1234,
            "assigned_instances": ["ITG Endpoint: The Chris Froome Room"],
            "is_endpoint": True,
            "battery_level": 2,
        },
        {
            "type": "AGENT",
            "id": "agent-gifjgfdfmappppdpdpf",
            "status": "ERROR",
            "hospital": "James Bond Hospital",
            "online": True,
            "full_status": "ONLINE",
            "agent_id": 1235,
            "assigned_instances": ["ITG Endpoint: The Chris Froome Room"],
            "is_endpoint": True,
            "battery_level": 0,
        },
        {
            "type": "AGENT",
            "id": "agent-gifjgijsdfijfhfh",
            "status": "WARN",
            "hospital": "Bames Jond Hospital",
            "online": True,
            "full_status": "ONLINE",
            "agent_id": 1236,
            "assigned_instances": ["ITG Endpoint: The Chris Froome Room", "Video Recorder: Screen 1", "Display Steam: Screen 1", "Something else: to make the list long"],
            "is_endpoint": True,
            "battery_level": 1,
        },
    ]
        
@app.route("/takes_forever")
def takes_forever():
    sleep(4)
    return Response("Timed out")


def create_query():
    now = datetime.datetime.now()
    time_to_completion = random.randint(15, 60)
    transfer = random.randint(0, 1)
    gateway_id = random.randint(0, 3)
    global query_id
    query = {
        "type": "PACS_TRANSFER",
        "id" : f"query-{query_id}",
        "status" : "RUN",
        "query_id": query_id,
        "hospital": hospitals_and_gateways[gateway_id]["hospital"],
        "gateway": hospitals_and_gateways[gateway_id]["gateway"],
        "gateway_id": gateway_id,
        "elapsed": 0,
        "transfer_type": transfer_types[transfer],
        "query_status": "NEW",
        "response": response_stages[0],
        "timing": time_to_completion,
        "created": now
    }
    query_id += 1
    return query

def progress_query(query):
    now = datetime.datetime.now()
    elapsed = (now - query["created"]).total_seconds()
    if elapsed > query["timing"]:
        global query_list
        query_list = [q for q in query_list if q["query_id"] != query["query_id"] ]
    else:
        query["elapsed"] = elapsed
        update = calculate_response(query["elapsed"], query["timing"])
        query["query_status"] = update["query_status"]
        if update["query_status"] == "RUN":
            query["response"] = update["response"]

def calculate_response(elapsed, timing):
    stage_index = math.floor((elapsed/timing) * 10 )
    primary_stage = response_stages[stage_index]
    
    if primary_stage["query_status"] == "RUN":
        if primary_stage["response"]["status"] in ["retrieving", "zipping", "uploading"]:
            completed = math.floor((elapsed/timing) * 100 )
            primary_stage["response"]["completed"] = completed
            primary_stage["response"]["total"] = 100
    
    return primary_stage