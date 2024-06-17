#!/usr/bin/env python3
"""
Write a Python script that provides some stats about Nginx
logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the number of documents in this collection
second line: Methods:
5 lines with the number of documents with the method =
["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
(see example below - warning: it’s a tabulation before each line)
one line with the number of documents with:
method=GET
path=/status
You can use this dump as data sample: dump.zip
"""

import pymongo
from pymongo import MongoClient

def log_nginx_stats(mongo_collection):
    """Provides some stats about Nginx logs."""
    try:
        log_count = mongo_collection.estimated_document_count()
        print(f"{log_count} logs")

        print("Methods:")
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        for method in methods:
            method_count = mongo_collection.count_documents({"method": method})
            print(f"\tmethod {method}: {method_count}")

        status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
        print(f"{status_check_count} status check")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        with MongoClient('mongodb://127.0.0.1:27017') as client:
            mongo_collection = client.logs.nginx
            log_nginx_stats(mongo_collection)
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print(f"Failed to connect to MongoDB: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

