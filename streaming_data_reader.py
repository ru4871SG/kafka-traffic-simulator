"""
Streaming data consumer
"""
from datetime import datetime
from dotenv import load_dotenv
from kafka import KafkaConsumer
import os
import psycopg2

load_dotenv()

db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_topic = os.environ.get("DB_TOPIC")


print("Connecting to the database")
try:
    connection = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
except Exception:
    print("Could not connect to database. Please check credentials")
else:
    print("Connected to database")
cursor = connection.cursor()

print("Connecting to Kafka")
consumer = KafkaConsumer(db_topic)
print("Connected to Kafka")
print(f"Reading messages from the topic {db_topic}")
for msg in consumer:

    # Extract information from kafka
    message = msg.value.decode("utf-8")

    # Transform the date format to suit the database schema
    (timestamp, vehicle_id, vehicle_type, plaza_id) = message.split(",")

    dateobj = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
    timestamp = dateobj.strftime("%Y-%m-%d %H:%M:%S")

    # Loading data into the database table "livetolldata"
    sql = "insert into livetolldata values(%s,%s,%s,%s)"
    result = cursor.execute(sql, (timestamp, vehicle_id, vehicle_type, plaza_id))
    print(f"A {vehicle_type} was inserted into the database")
    connection.commit()
connection.close()