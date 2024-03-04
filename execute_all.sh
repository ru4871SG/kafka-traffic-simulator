#!/bin/bash

# Exit the script if any command fails
set -e

# Set the paths to the Python and PSQL executables
PYTHON_PATH="/home/username/anaconda3/bin/python"
PSQL_PATH="/usr/bin/psql"

# Load environment variables from .env file
source .env

# Run SQL script
echo "Running SQL script..."
"$PSQL_PATH" -v ON_ERROR_STOP=1 -U "$DB_USER" -d "$DB_NAME" -f create_table_livetolldata.sql

# Run Python scripts
echo "Running Python scripts..."
"$PYTHON_PATH" toll_traffic_generator.py &
"$PYTHON_PATH" streaming_data_reader.py &

echo "Python scripts are running in the background."