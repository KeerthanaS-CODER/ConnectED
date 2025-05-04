from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# Attempt connection to a non-existent or unreachable host with a short timeout
try:
    client = MongoClient(host="nonexistent_host", port=27017, serverSelectionTimeoutMS=100)
    client.admin.command('ping')  # Trigger server selection
except ServerSelectionTimeoutError as e:
    print(f"Successfully raised ServerSelectionTimeoutError: {e}")
else:
    print("ServerSelectionTimeoutError was not raised.")
finally:
    # Close the client, even if an exception occurred
    client.close()