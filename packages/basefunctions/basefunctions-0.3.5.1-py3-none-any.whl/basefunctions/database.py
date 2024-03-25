"""
# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : stocksdatabase
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  a simple module to connect to a postgres database environment
#
# =============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import decouple
import sqlalchemy

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
#  FUNCTION DEFINITIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
#  create an engine object for connecting to the database
# -------------------------------------------------------------
def connect_to_database(prefix: str) -> sqlalchemy.engine.base.Engine:
    """
    connect to the database and return the connection object

    Returns
    -------
    sqlalchemy.engine.Engine
        connection object
    """

    sqlalchemy_protocol = decouple.config(
        f"{prefix}_PROTOCOL",
        default="postgresql+psycopg2",
        cast=str,
    )
    host_name = decouple.config(f"{prefix}_HOSTNAME", default="localhost", cast=str)
    database_name = decouple.config(f"{prefix}_DATABASE", default=None, cast=str)
    user_name = decouple.config(f"{prefix}_USERNAME", default="postgres", cast=str)
    password = decouple.config(f"{prefix}_PASSWORD", default=None, cast=str)
    port = decouple.config(f"{prefix}_PORT", default=5432, cast=int)

    engine = sqlalchemy.create_engine(
        f"{sqlalchemy_protocol}://{user_name}:{password}" f"@{host_name}:{port}/{database_name}"
    )
    return engine


# -------------------------------------------------------------
#  execute a sql command
# -------------------------------------------------------------
def execute_sql_command(engine: sqlalchemy.engine.base.Engine, sql_command: str) -> None:
    """
    execute a sql command

    Parameters
    ----------
    sql_command : str
        sql command to execute

    Returns
    -------
    None
    """
    with engine.connect() as connection:
        connection.execute(sqlalchemy.text(sql_command))


def execute_sql_drop_table(engine: sqlalchemy.engine.base.Engine, table_name: str) -> None:
    """
    drop a table from the database

    Parameters
    ----------
    table_name : str
        name of the table to drop

    Returns
    -------
    None
    """
    with engine.connect() as connection:
        connection.execute(sqlalchemy.text(f'DROP TABLE IF EXISTS "{table_name}"; COMMIT;'))


def check_if_table_exists(engine: sqlalchemy.engine.base.Engine, table_name: str) -> bool:
    """
    check if a table exists in the database

    Parameters
    ----------
    table_name : str
        name of the table to check

    Returns
    -------
    bool
        True if the table exists, False otherwise
    """
    with engine.connect() as _:
        return sqlalchemy.inspect(engine).has_table(table_name=table_name)


def get_number_of_elements_in_table(engine: sqlalchemy.engine.base.Engine, table_name: str) -> int:
    """
    get number of elements in a table

    Parameters
    ----------
    table_name : str
        the table_name to get the number of elements from

    Returns
    -------
    int
        number of elements in the table
    """

    with engine.connect() as connection:
        if not sqlalchemy.inspect(engine).has_table(table_name=table_name):
            return 0
        return connection.execute(sqlalchemy.text(f"SELECT COUNT(*) FROM {table_name};")).first()[
            0
        ]
