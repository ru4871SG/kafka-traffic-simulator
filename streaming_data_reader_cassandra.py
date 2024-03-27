"""
Streaming data consumer for Cassandra
"""
from cassandra.cluster import Cluster
from datetime import datetime
from dotenv import load_dotenv
from kafka import KafkaConsumer
import os

load_dotenv()

# Cassandra connection parameters
cassandra_host = '172.18.0.2'  # Adjust if your Cassandra datacenter IP is different
keyspace_name = os.environ.get("CASSANDRA_KEYSPACE")

# Initialize Kafka Consumer
db_topic = os.environ.get("DB_TOPIC")

print("Connecting to Cassandra")
try:
    cluster = Cluster([cassandra_host])
    session = cluster.connect(keyspace_name)
except Exception as e:
    print(f"Could not connect to Cassandra: {e}")
else:
    print("Connected to Cassandra")

print("Connecting to Kafka")
consumer = KafkaConsumer(db_topic)
print("Connected to Kafka")
print(f"Reading messages from the topic {db_topic}")

for msg in consumer:
    # Extract information from Kafka
    message = msg.value.decode("utf-8")

    # Transform the date format to suit Cassandra's expected format
    (timestamp, vehicle_id, vehicle_type, plaza_id) = message.split(",")

    dateobj = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
    # Convert datetime object to UNIX timestamp in milliseconds
    unix_timestamp_ms = int(dateobj.timestamp() * 1000)

    # Loading data into the the table called 'toll_events'
    cql = """
    INSERT INTO toll_events (event_time, vehicle_id, vehicle_type, plaza_id)
    VALUES (%s, %s, %s, %s)
    """
    try:
        session.execute(cql, (unix_timestamp_ms, int(vehicle_id), vehicle_type, int(plaza_id)))
        print(f"A {vehicle_type} was inserted into table toll_events")
    except Exception as e:
        print(f"Failed to insert data into Cassandra: {e}")
