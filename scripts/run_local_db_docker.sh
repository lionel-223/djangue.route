#!/bin/bash

docker run --replace -d --name postgres_1l1s -p 5435:5432 -e POSTGRES_HOST_AUTH_METHOD=trust -v /var/lib/postgresql/data postgres
