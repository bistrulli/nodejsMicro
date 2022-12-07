#!/bin/bash 

set -x

export COHERENCE_SERVICE_NAME=Catalogue
java -jar ~/git/coherence-spring-sockshop-sample/catalog/target/catalog-1.2.4-SNAPSHOT.jar \
--spring.zipkin.enabled=false --coherence.server.startup-timeout=5m
