# ##################################################################
#
# Copyright 2024 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Shravan Jat(shravan.jat@teradata.com)
# Secondary Owner: Pradeep Garre(pradeep.garre@teradata.com)
#
#
# Version: 1.0
#
# ##################################################################
from collections import OrderedDict
import os
from teradataml import ReadNOS, WriteNOS, read_csv, DataFrame as tdml_DataFrame
from teradataml.common.utils import UtilFuncs

class DataFrameReader:
    def __init__(self, **kwargs):

        # Always
        #   'format' holds the format for file. - parquet, csv, orc etc.
        #   'mode' holds the format for file. - parquet, csv, orc etc.
        self.__params = {**kwargs}

    def format(self, source):
        self.__params.update({"stored_as": "PARQUET" if source == 'parquet' else 'TEXTFILE'})
        return DataFrameReader(**self.__params)

    def json(self, path, **kwargs):
        self.__params.update({"location": path, "stored_as": "TEXTFILE"})
        from teradatamlspk.sql.dataframe import DataFrame as tdmlspk_DataFrame
        return tdmlspk_DataFrame(ReadNOS(**self.__params).result)


    def option(self, key, value):
        self.__params[key] = value
        return DataFrameReader(**self.__params)

    def parquet(self, path, **kwargs):
        self.__params.update({"location": path, "stored_as": "PARQUET"})
        from teradatamlspk.sql.dataframe import DataFrame as tdmlspk_DataFrame
        return tdmlspk_DataFrame(ReadNOS(**self.__params).result)

    def options(self, **options):
        self.__params.update(**options)
        return DataFrameReader(**self.__params)

    def load(self, path, format = 'parquet', schema = None, **options):
        if not self.__params.get("stored_as"):
            self.__params.update({"stored_as": "PARQUET" if format == 'parquet' else 'TEXTFILE'})
        self.__params.update({"location": path})
        from teradatamlspk.sql.dataframe import DataFrame as tdmlspk_DataFrame
        return tdmlspk_DataFrame(ReadNOS(**self.__params).result)

    def csv(self, path, **kwargs):
        from teradatamlspk.sql.dataframe import DataFrame as tdmlspk_DataFrame

        # Check whether to use tdml read_csv or NoS.
        # Check if the specified path is existed in clients machine or not.
        # If yes, do read_csv. Else, use NoS.
        if os.path.exists(path):

            from teradatamlspk.sql.constants import SPARK_TO_TD_TYPES

            # Define the arguments for read_csv.
            _args = {**self.__params}

            schema = kwargs.get("schema")
            if ("types" not in _args) and schema:
                # Generate types argument.
                types = OrderedDict()
                for column in schema.fieldNames():
                    types[column] = SPARK_TO_TD_TYPES[type(schema[column].dataType)]

                _args["types"] = types
            else:
                # Teradata read_csv can not infer the data.
                raise Exception("Schema is mandatory for Teradata Vantage. ")

            table_name = _args.get("table_name")
            if not table_name:
                # Generate a temp table name.
                _args["table_name"] = UtilFuncs._generate_temp_table_name(
                    prefix="tdmlspk_read_csv", gc_on_quit=True)

            _args["filepath"] = path

            # Call read_csv from teradataml.
            res = read_csv(**_args)

            # Result can be tdml DataFrame or a tuple -
            #       first element is teradataml DataFrame.
            #       second element is a dict.
            # Look read_csv documentation for details.
            if isinstance(res, tdml_DataFrame):
                return tdmlspk_DataFrame(res)

            # Now we are here. So, this returns a tuple.
            # Print the warnings and error DataFrame's dict.
            print(res[1])

            # Then return teradatamlspk DataFrame.
            return tdmlspk_DataFrame(res[0])

        self.__params.update({"location": path, "stored_as": "TEXTFILE"})

        return tdmlspk_DataFrame(ReadNOS(**self.__params).result)

