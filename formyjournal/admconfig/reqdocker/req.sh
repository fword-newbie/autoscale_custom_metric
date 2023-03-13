#!/bin/bash

for i in {1..20}; do
  curl -I http://helloworld-service:80
  sleep 20
done

