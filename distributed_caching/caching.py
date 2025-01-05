#!/usr/bin/env python3
# ©2024, Ovais Quraishi
"""A relatively efficient implementation of distributed caching using Redis with a Flask endpoint
	Implements consistent hashing: ensures even distribution of keys across nodes
	Implements a client Interface/communication protocol: interact with this service via endpoint,
		defines a READ/WRITE/DELETE communication protocol
	Replication: relies on Redis Server Replication (there are few other options available as well)

	Assumes: for this exercise a redis server with 1 master and 3 replicas
"""

import redis
from hashlib import blake2b
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

# import required local modules
from config import get_config
from utils import get_version

# constants
app = Flask("Caching-Service")

CONFIG = get_config()

REDIS_CONFIG = {
    "host": CONFIG.get('redis','host'),
    "port": CONFIG.get('redis','port'),
    "password": CONFIG.get('redis','password'),
    "db": CONFIG.get('redis','db'),
    "decode_responses": CONFIG.get('redis','decode_responses')
}

app.config.update(
                  JWT_SECRET_KEY=CONFIG.get('service', 'JWT_SECRET_KEY'),
                  SECRET_KEY=CONFIG.get('service', 'APP_SECRET_KEY'),
                  PERMANENT_SESSION_LIFETIME=172800 #2 days
                 )
jwt = JWTManager(app)

class DistributedCache:
    def __init__(self, nodes):
        """Establish connection context"""

        self.nodes = nodes
        self.redis_clients = [redis.StrictRedis(**REDIS_CONFIG) for _ in nodes]

    def blake2_hash_function(self, key):
        """Consistent hashing function
            blake2b is preferred over MD5 for security-sensitive applications
            where strong collision resistance and performance are required.
        """

        return int(blake2b(key.encode()).hexdigest(), 16)

    def get_node(self, key):
        """Use consistent hashing to determine target storage node for a given key"""

        hash_value = self.blake2_hash_function(key)
        node_index = hash_value % len(self.nodes)
        return node_index

    def send_request(self, node, request):
        """Send a request to the specified cache node and receive the response"""
        if request["command"] == "WRITE":
            self.redis_clients[node].set(request["key"], request["value"])
            return {"command": request["command"], "status": "SUCCESS", "value": request["value"]}
        elif request["command"] == "READ":
            value = self.redis_clients[node].get(request["key"])
            if value is not None:
                return {"command": request["command"], "status": "SUCCESS", "value": value}
            else:
                return {"command": request["command"], "status": "NOT_FOUND", "message": request["key"] + " Key not found"}
        elif request["command"] == "DELETE":
            deleted_count = self.redis_clients[node].delete(request["key"])
            if deleted_count == 1:
                return {"command": request["command"], "status": "SUCCESS", "message": request["key"] + " Key deleted"}
            else:
                return {"status": "NOT_FOUND", "message": request["key"] + " Key not found"}
        else:
            return {"status": "ERROR", "message": request["command"] + " Invalid command"}

    def read(self, key):
        """Send a READ request to the appropriate cache node"""
        node = self.get_node(key)
        request = {"command": "READ", "key": key}
        return self.send_request(node, request)

    def write(self, key, value):
        """Send a WRITE request to the appropriate cache node"""
        node = self.get_node(key)
        request = {'command': 'WRITE', 'key': key, 'value': value}
        return self.send_request(node, request)

    def delete(self, key):
        """Send a DELETE request to the appropriate cache node"""
        node = self.get_node(key)
        request = {"command": "DELETE", "key": key}
        return self.send_request(node, request)

# Instantiate the cache with nodes
cache = DistributedCache(nodes=['node1', 'node2', 'node3'])  # redis node names here

@app.route('/version', methods=['GET'])
def version():
    """Get service version semver
    """

    response = get_version()

    if isinstance(response, dict) and 'error' in response:
        return jsonify(response), 400
    elif response is False:  # New elif block to handle False responses
        # Return a custom error message or status code
        custom_error = {'message': 'Version information is not available'}
        return jsonify(custom_error), 500
    elif isinstance(response, dict):
        return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    """Generate JWT
    """

    secret = request.json.get('api_key')

    if secret != CONFIG.get('service','SRVC_SHARED_SECRET'):  # if the secret matches
        return jsonify({"message": "Invalid secret"}), 401

    # generate access token
    access_token = create_access_token(identity=CONFIG.get('service','IDENTITY'))
    return jsonify(access_token=access_token), 200

@app.route('/cache', methods=['POST'])
@jwt_required()
def cache_request():
    """Endpoint to handle caching requests"""
    data = request.get_json()
    command = data.get('command')
    key = data.get('key')
    value = data.get('value')

    if command == 'READ':
        return cache.read(key)
    elif command == 'WRITE':
        return cache.write(key, value)
    elif command == 'DELETE':
        return cache.delete(key)
    else:
        return {"status": "ERROR", "message": "Invalid command"}

if __name__ == '__main__':

    # non-production WSGI settings:
    #  port 8000, listen to local ip address, use ssl
    # in production we use gunicorn
    app.run(port=CONFIG.get('service','PORT'),
			host='0.0.0.0',
			#ssl_context=('1cert.pem', '1key.pem'),
			debug=False) # not for production
