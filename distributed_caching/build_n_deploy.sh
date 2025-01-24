#!/bin/bash

check_pod_status() {
  namespace_name="$1"
  my_srvc_name="$2"
  iterations=0
  while [ $iterations -lt 10 ]; do
    output=$(kubectl -n ${namespace_name} describe deployment | grep -e "Replicas:")
    if [[ "$output" =~ "0 unavailable" ]]
    then
      echo "Pod is running."
      return
    elif [ $iterations -ge 10 ]; then
      echo "Failed to start pod after 10 attempts"
      exit 1 # hard exit with a non-zero status code
    else
      echo "**** ${output} not yet 'Running', trying again..."
      sleep 2
      ((iterations++))
    fi
  done
}

cd ./distributed_caching
pwd

scp -r ovais@localhost:/home/ovais/caching-service/setup.config .

#docker build -D -t caching-service .

./build_docker.py

srvc_ver=$(<ver.txt)
namespace="caching"
srvc_name="caching"

echo "**** Pushing Docker Image ${srvc_name}:${srvc_ver} to remote registry"
docker tag ${srvc_name}:${srvc_ver} jenkins-node-1:5000/${srvc_name}:${srvc_ver} > /dev/null 2>&1
docker tag ${srvc_name}:latest jenkins-node-1:5000/${srvc_name}:latest > /dev/null 2>&1
docker push jenkins-node-1:5000/"${srvc_name}":${srvc_ver} > /dev/null 2>&1
docker push jenkins-node-1:5000/${srvc_name}:latest > /dev/null 2>&1


sed -i "s|SEMVER|"${srvc_ver}"|" deployment.yaml
sed -i "s|SEMVER|"${srvc_ver}"|" service.yaml
kubectl -n "${namespace}" apply -f deployment.yaml
kubectl -n "${namespace}" apply -f service.yaml
sleep 5

git checkout deployment.yaml
git checkout service.yaml

echo "**** Get Healthcheck of the service"
k8_srvc_name=$(kubectl -n "${namespace}" get svc -o name | sed -e 's/service\///g')
k8_srvc_nodeport=$(kubectl -n "${namespace}" get svc "${k8_srvc_name}" -o jsonpath='{.spec.ports[0].nodePort}')

check_pod_status "${namespace}" "${srvc_name}"

running_srvc_ver=$(curl -X GET -s "http://k8prod-1.ifthenelse.org:${k8_srvc_nodeport}/version")
echo "**** Running service version: ${running_srvc_ver}"
