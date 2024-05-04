### Distributed Caching Service

A relatively efficient implementation of distributed caching using Redis with a Flask endpoint.

* Implements consistent hashing: ensures even distribution of keys across nodes.
* Implements a client interface/communication protocol: interact with this service via endpoint,
  defines a READ/WRITE/DELETE communication protocol.
* Replication: relies on Redis Server Replication (there are few other options available as well).
* Assumes: for this exercise, a Redis server with 1 master and 3 replicas.
* **Encrypt value**: see the _encryption.py_ module should you need to store encrypted values. See code example
  ```code
  value = encrypt_text(value).decode('utf-8')
  ```

##### Generate SSL key/cert
* Gen SSL key/cert for secure connection to the service
    > openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 3650

#### Examples

**GET Bearer Token**
requires "jq" Command-line JSON processor 
```shell
> export api_key="your_api_key_here"
> export AT=$(curl -sk -X POST \
  https://localhost:8000/login \
  -H 'Content-Type: application/json' \
  -d '{
    "api_key": "'${api_key}'"
}' | jq -r .access_token)

```

**WRITE**
```shell
> curl -k -X POST \
  https://localhost:8000/cache \
  -H "Authorization: Bearer ${AT}" \
  -H 'Content-Type: application/json' \
  -d '{
    "command": "WRITE",
    "key": "my_key",
    "value": "my_value"
}'

{
  "command": "WRITE",
  "status": "SUCCESS",
  "value": "my_value"
}
* Closing connection
```

**READ**
```shell
curl -k -X POST \
  https://localhost:8000/cache \
  -H "Authorization: Bearer ${AT}" \
  -H 'Content-Type: application/json' \
  -d '{
    "command": "READ",
    "key": "my_key"
}'

{
  "command": "READ",
  "status": "SUCCESS",
  "value": "my_value"
}
```

**DELETE**
```shell
curl -k -X POST \
  https://localhost:8000/cache \
  -H "Authorization: Bearer ${AT}" \
  -H 'Content-Type: application/json' \
  -d '{
    "command": "DELETE",
    "key": "my_key"
}'

{
  "command": "DELETE",
  "message": "my_key Key deleted",
  "status": "SUCCESS"
}
```
