# Apache Kafka - Traffic Simulator

This repository contains two Python scripts for simulating a traffic toll collection system using Apache Kafka. The `toll_traffic_generator.py` producer script simulates traffic at a toll booth by generating and sending messages to a Kafka topic called `toll`. Meanwhile, the `streaming_data_reader.py` consumer script listens to the Kafka topic, processes the incoming messages, and stores the data in a PostgreSQL database.

This repository also contains a SQL script `create_table_livetolldata.sql` that you can use to create the table in your PostgreSQL database. Lastly, you can also use the provided Bash script if you want to automate all the script executions from this repository.

Update (March 26, 2024): I added two new files in case you want to store the simulated traffic data into a local Apache Cassandra datacenter. The new files include 1 Python script `streaming_data_reader_cassandra.py` and 1 CQL script`create_table_toll_events_cassandra.cql`.


## Overview

- `toll_traffic_generator.py`: Kafka producer script that simulates toll booth traffic by sending vehicle passage events to a Kafka topic. Each event includes a timestamp, vehicle ID, vehicle type, and toll plaza ID.
- `streaming_data_reader.py`: Kafka consumer script that consumes messages from the Kafka topic, processes them to match the database schema, and inserts the data into a PostgreSQL database.
- `create_table_livetolldata.sql`: SQL script that creates an example table called "livetolldata" inside the "public" schema. The same table name is referred in `streaming_data_reader.py`.
- `execute_all.sh`: Bash script to automate all the above script executions (doesn't include Cassandra-related scripts).
- `streaming_data_reader_cassandra.py`: The equivalent of `streaming_data_reader.py` but it stores the data into a local Cassandra datacenter instead.
- `create_table_toll_events_cassandra.cql`: CQL (Cassandra Query Language) to create an example table called "toll_events" inside the "traffic" keyspace. The same table name is referred in `streaming_data_reader_cassandra.py`.

## Prerequisites

- Python 3.x
- Apache Kafka
- PostgreSQL
- Apache Cassandra
- Python packages: `kafka-python`, `psycopg2`, `python-dotenv`, and `cassandra-driver`

## How to Use

Start the zookeeper server as well as the Kafka server. After that, you should create a Kafka topic named `toll`. 

You can then create `.env` file with your database configuration (check `.env.example` for the structure).

After you are done with the configuration, you can just run the provided bash script `execute_all.sh` which will automatically execute `create_table_livetolldata.sql`, `toll_traffic_generator.py`, and `streaming_data_reader.py`.

Update (March 26, 2024): If you want to store the data into Cassandra (and not PostgreSQL), you can just execute `streaming_data_reader_cassandra.py` in exchange of `streaming_data_reader.py`. Make sure you have created the "toll_events" table as instructed in `create_table_toll_events_cassandra.cql`. You can use a standard keyspace named "traffic" with SimpleStrategy and replication factor of 1 since this is just used for simple simulation.