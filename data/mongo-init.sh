#!/bin/bash
echo "Starting data import in mongo-init.sh"
mongoimport --db DesignersDB --collection Designers --file /docker-entrypoint-initdb.d/DesignersDB.Designers.json --jsonArray
echo "Data import finished"
