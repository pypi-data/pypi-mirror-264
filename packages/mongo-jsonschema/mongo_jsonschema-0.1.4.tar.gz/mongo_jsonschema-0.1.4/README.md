# Mongo Schema

Reverse engineer JSONSchemas from a MongoDB database.

## Installation

`pip install mongo-jsonschema`

## Usage

### As CLI Tool

<pre>
usage: python -m mongo_jsonschema [-h] [-c COLLECTIONS] [-p PORT] [-s SAMPLE_SIZE] [-r {PRIMARY,PRIMARY_PREFERRED,SECONDARY,SECONDARY_PREFERRED,NEAREST}] [-d DESTINATION] [-e] host db

Generates JSONSchemas from MongoDB Collections by sampling documents from the collection.

positional arguments:
  host                  A MongoDB hostname or connection string.
  db                    The name of the database in which the collections reside.

optional arguments:
  -h, --help            show this help message and exit
  -c COLLECTIONS, --collections COLLECTIONS
                        A comma separated list of collections to generate schemas from. If blank, schemas will be generated for all collections.
  -p PORT, --port PORT  The port to use when connecting to the MongoDB server. Required if host is not a connectionstring.
  -s SAMPLE_SIZE, --sample_size SAMPLE_SIZE
                        A decimal representation of the percentage of total documents in the collection to sample when deriving the schema. Default is .33.
  -r {PRIMARY,PRIMARY_PREFERRED,SECONDARY,SECONDARY_PREFERRED,NEAREST}, --read_preference {PRIMARY,PRIMARY_PREFERRED,SECONDARY,SECONDARY_PREFERRED,NEAREST}
                        The read preference to use when querying the MongoDB database. Default is 'SECONDARY'.
  -d DESTINATION, --destination DESTINATION
                        The directory to output the generated schemas to. If none is specified, will be output to the current working directory.
  -e, --external_sorting
                        Enables external sorting, using the disk on the mongodb server, for aggregations that exceed the memory limit. If false, the aggregation fails due to an exceeded memory limit, the
                        schema will be skipped.
</pre>

### As A Library

```python
from mongo_jsonschema import SchemaGenerator

# Initialize with your mongodb hostname and port
schema_generator = SchemaGenerator('localhost', 27017)
# Or use a connection string
schema_generator = SchemaGenerator('mongodb+srv://username:password@localhost/mydatabase')

#Generate schema for a multiple collections
schemas = schema_generator.get_schemas(
    db='mydatabase', 
    collections=['foo','bar'],
    sample_percent=.05
)

# Generate schema for a single collection.
schema = schema_generator.get_schemas(
    db='dbname',
    collection='baz',
    sample_percent=.05
)
