from pymongo import MongoClient
from pymongo.errors import OperationFailure
from genson import SchemaBuilder, TypedSchemaStrategy
from genson.schema.node import SchemaGenerationError
from bson import ObjectId
import json
from datetime import datetime
from warnings import warn
from typing import List, Optional, Union


class AdditionalTypesStrategy(TypedSchemaStrategy):
    JS_TYPE = "string"
    PYTHON_TYPE = (ObjectId, datetime)


class ObjectIdAwareBuilder(SchemaBuilder):
    EXTRA_STRATEGIES = (AdditionalTypesStrategy,)


class SchemaGenerator:

    def __init__(self, host: str, port: Optional[int]=None, **kwargs) -> None:
        """
        Creates an instance of SchemaGenerator.

        Args:
            host: The MongoDB hostname or connection string, defaults to localhost.
            port: The port that MongoDB is listening for connections, defaults to None.
            kwargs: See the documentation for pymongo.MongoClient for additional kwargs.

        Returns:
            An instance of the SchemaGenerator class.
        """
        self.client = MongoClient(
            host, port, datetime_conversion="DATETIME_AUTO", **kwargs
        )

    def get_schemas(
        self,
        db: str,
        collections: Union[str, List[str]],
        sample_percent: float = 0.33,
        **kwargs,
    ) -> Union[dict, List[dict]]:
        """
        Generates schema from the provided database and collection or list of collections.

        Args:
            db: The name of the database in which the collection(s) reside.
            collection: The name of the collection or a list of collection names to generate schemase for.
            sample_size: A percentage of the documents in the collection to sample for schema generation, defaults to .33.

        Returns:
            A dict or list of dicts containing the schemas generated for the provided collections.
        """
        if isinstance(collections, str):
            return self._get_schema(db, collection, sample_percent, **kwargs)
        elif isinstance(collections, list):
            return [
                self._get_schema(db, collection, sample_percent, **kwargs)
                for collection in collections
            ]
        else:
            raise TypeError("collection must be a string or list of strings")

    def _get_documents(self, db, collection, sample_percent, **kwargs):
        collection = self.client.get_database(db).get_collection(collection)
        sample_size = int(collection.estimated_document_count() * sample_percent)
        external_sorting = kwargs.get("external_sorting", False)
        try:
            for document in collection.aggregate(
                [{"$sample": {"size": sample_size}}], allowDiskUse=external_sorting
            ):
                yield document
        except OperationFailure:
            warn(
                f"An OperationFailure occurred when trying to sample the collection {collection}. Set external_sorting to True to use the mongodb server disk for sorting."
            )
            return False
        except Exception as e:
            print(document)
            raise e

    def _get_schema(self, db, collection, sample_percent, **kwargs):
        documents = self._get_documents(db, collection, sample_percent, **kwargs)
        if documents:
            builder = ObjectIdAwareBuilder()
            for document in documents:
                try:
                    builder.add_object(document)
                except SchemaGenerationError:
                    warn(f"failed to add document to schema: {document}")
            return builder.to_schema()
        else:
            return {
                "error": "external_sorting disabled, memory limit exceeded for query"
            }


if __name__ == "__main__":
    from argparse import ArgumentParser
    from pymongo.read_preferences import ReadPreference
    from pymongo.read_preferences import _MODES as read_preference_modes
    from os import path, mkdir

    parser = ArgumentParser(
        prog="python -m mongo_jsonschema",
        description="Generates JSONSchemas from MongoDB Collections by sampling documents from the collection.",
    )
    parser.add_argument("host", help="A MongoDB hostname or connection string.")
    parser.add_argument(
        "db", help="The name of the database in which the collections reside."
    )
    parser.add_argument(
        "-c",
        "--collections",
        help="A comma separated list of collections to generate schemas from. If blank, schemas will be generated for all collections.",
        dest="collections",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="The port to use when connecting to the MongoDB server. Required if host is not a connectionstring.",
        dest="port",
        type=int,
    )
    parser.add_argument(
        "-s",
        "--sample_size",
        type=float,
        help="A decimal representation of the percentage of total documents in the collection to sample when deriving the schema. Default is .33.",
        default=0.33,
        dest="sample_size",
    )
    parser.add_argument(
        "-r",
        "--read_preference",
        help="The read preference to use when querying the MongoDB database. Default is 'SECONDARY'.",
        default="SECONDARY",
        choices=read_preference_modes,
        dest="read_preference",
    )
    parser.add_argument(
        "-d",
        "--destination",
        help="The directory to output the generated schemas to. If none is specified, will be output to the current working directory.",
        default="schemas",
        dest="destination",
    )
    parser.add_argument(
        "-e",
        "--external_sorting",
        help="Enables external sorting, using the disk on the mongodb server, for aggregations that exceed the memory limit. If false, the aggregation fails due to an exceeded memory limit, the schema will be skipped.",
        action="store_true",
        dest="external_sorting",
    )

    args = parser.parse_args()

    read_preference = ReadPreference().__getattribute__(args.read_preference)

    schema_generator = SchemaGenerator(
        host=args.host, port=args.port, read_preference=read_preference
    )

    if not path.exists(args.destination):
        mkdir(args.destination)

    if args.collections:
        collections = args.collections.split(",")
    else:  # discover the available collections in the database when no collections are specified
        collections = schema_generator.client.get_database(
            args.db
        ).list_collection_names()
        collections = list(
            filter(lambda collection: collection != "system.views", collections)
        )

    for collection in collections:
        print(f"Generating schema for collection {collection}")
        schema = schema_generator.get_schemas(
            args.db,
            collection,
            args.sample_size,
            external_sorting=args.external_sorting,
        )
        with open((d_path := f"{args.destination}/{collection}.json"), "w") as f:
            print(f"Saving schema for {collection} to {d_path}")
            f.write(json.dumps(schema))
