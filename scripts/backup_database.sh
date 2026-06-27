#!/bin/bash

docker exec recommendation_postgres \
pg_dump -U postgres recommendation_db \
> recommendation_backup.sql

echo "Database backup created."