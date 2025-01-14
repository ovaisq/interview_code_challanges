#!/bin/bash
# ©2025, Ovais Quraishi
# NOTE: assumes that setup.config.orig, with all settings assigned
#		except "version" is set to "version=SEMVER" exists

# Define a function for each operation
build_docker() {
  my_ver=$1
  cp setup.config.orig setup.config
  sed -i "s|SEMVER|$my_ver|" setup.config
  ./build_docker.py
}

push_image() {
  my_ver=$1
  service_name=$2
  docker_host_uri=$3

  echo "docker tag ${service_name}:${my_ver} ${docker_host_uri}/${service_name}:${my_ver}"
  docker tag "${service_name}:${my_ver}" "${docker_host_uri}/${service_name}:${my_ver}"
  echo "docker push ${docker_host_uri}/${service_name}:${my_ver}"
  docker push "${docker_host_uri}/${service_name}:${my_ver}"
}

apply_kubernetes() {
  my_ver=$1
  cp deployment.yaml.orig deployment.yaml
  sed -i "s|SEMVER|$my_ver|" deployment.yaml
  kubectl -n ollamagpt apply -f deployment.yaml
  kubectl -n ollamagpt apply -f service.yaml
}

# Read version from ver.txt
my_ver=$(<ver.txt)

docker_host_uri="jenkins-node-1:5000"
service_name="summarize-web-pages"

# Call the functions with the version as an argument
build_docker $my_ver
push_image $my_ver $service_name $docker_host_uri
apply_kubernetes $my_ver
