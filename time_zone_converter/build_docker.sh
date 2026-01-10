#!/usr/bin/env bash
release_name="timezone-converter"
repository_host="jenkins-node-1:5000"
release_ver="0.3.0"
docker build -t "$release_name:$release_ver" .
docker tag "$release_name:$release_ver" "$repository_host/$release_name:$release_ver"
docker push "$repository_host/$release_name:$release_ver"
