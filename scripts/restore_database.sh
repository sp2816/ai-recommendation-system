#!/bin/bash

docker exec -i recommendation_postgres \
psql -U postgres recommendation_db \
< recommendation_backup.sql

echo "Database restored."