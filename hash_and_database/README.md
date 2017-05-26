# Hasher and Database
## Hasher
### Description
An implementation of Pearson hashing a the hash function to compress the vac_no and vin for the system.

### Usage
To initialize, just use the initializer of the *Hasher* class and use the *hash_function* to hash a message.

Take note that the *end_session* function is important for every usage of the *Hasher* class to end its connection to the database for further usage.

## Database
### Description
A python class used to connect to a PostgreSQL database for ease of usage.

### Usage
#### Initialization
To initialize the *Database* class, the database name (*dbname*), username (*user*), host name (*host*), and password (*password*) are needed to connect the program to the database.

#### INSERT query
To do an INSERT query, the *insert_query* function can be used with the parameters *attributes*, *values*, and *table*. The program would then do the following query: `INSERT INTO <table> (<attributes>) VALUES <values>`.

#### UPDATE query
The UPDATE query can be done by using the *update_query* function with parameters *values_and_atrributes_set*, *table*, and *condition* to do the following query: `UPDATE <table> SET <values_and_atrributes_set> WHERE <condition>`.

#### SELECT query
To SELECT an *attributes* from a *table* with a *condition*, the *select_query* function can be used to do: `SELECT <attribute> FROM <table> WHERE <condition>`

#### DELETE query
To delete a row from a table, the *delete_query* function with the parameters *table*, and *condition* can be used. It does: `DELETE FROM <table> WHERE <condition>`.

Furthermore, it restarts the sequence of ids to the one after the maximum id. This ensures that the ids can be as small as possible.

#### Disconnect
Disconnecting through the *disconnect* function is important to make sure that there would be no running processes between the database and the application.

### Notes
#### The following parameters can be of the following format:
1. *dbname*, *user*, *host*, *password*, *table* - `'parameter'`
2. *attributes*, *values* - `'parameter, parameter, parameter, ...'`
3. *values_and_atrributes_set* - `'parameter = value, parameter = value, ...'`
4. *condition* - `'parameter = value'` or `'parameter LIKE %value%'`
