#!/bin/bash

name=postgres_1l1s

if docker container exists $name; then
	docker start $name
else
	docker run --replace -d --name $name -p 5435:5432 -e POSTGRES_HOST_AUTH_METHOD=trust -v /var/lib/postgresql/data postgres
fi
