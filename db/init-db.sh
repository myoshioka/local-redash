#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER $TEST_DB;
	CREATE DATABASE $TEST_USER;
	GRANT ALL PRIVILEGES ON DATABASE $TEST_DB TO $TEST_USER;
EOSQL

echo 'Importing data'

psql --username $TEST_USER -d $TEST_DB < /docker-entrypoint-initdb.d/dump/pagila-schema.sql
echo 'Importing schema finished successfully'

# psql --username $TEST_USER -d $TEST_DB < /docker-entrypoint-initdb.d/dump/pagila-insert-data.sql
# echo 'Importing insert-data finished successfully'

psql --username $TEST_USER -d $TEST_DB < /docker-entrypoint-initdb.d/dump/pagila-data.sql
echo 'Importing data finished successfully'

echo 'Data import finished successfully'%
