# Utility functions
import datetime
from typing import Any

from configs import COUNTRY_COLUMN
from queries import INSERT_ENTRY, CREATE_TABLE


def get_named_tuple_header(header_row: str, separator: str = "|") -> dict:
    """
    Creates a dictionary which holds indices of different field types in the header
    Args:
        header_row: Header row separated by separator
        separator: String by which different data fields are separated in header row

    Returns:
        Dictionary containing DataRow with field indices
    """
    field_indices = dict()

    # Split and create a list from header row
    header_fields = header_row.split(separator)

    # Iterate over all fields and store the their indices
    # [Skip first 2 elements as they will be '' and 'H']
    for i, item in enumerate(header_fields[2:]):
        field_indices[item] = i

    return field_indices


def convert_date(raw_data: str, date_format: str) -> str:
    """
    Converts date string to 'YYYY-MM-DD' format
    Args:
        raw_data: Data present in the file
        date_format: Date format

    Returns:
        String in 'YYYY-MM-DD' format
    """
    d = datetime.datetime.strptime(raw_data, date_format).date()
    return str(d)


def get_database_config(filename: str = "db.ini", section: str = "postgresql") -> dict:
    """
    Get database config dictionary from config file
    Args:
        filename: Absolute configuration file path
        section: Section to refer in the file

    Returns:
        Dictionary containing database config
    """
    from configparser import ConfigParser

    # Parse the config from file
    parser = ConfigParser()
    parser.read(filename)

    try:
        # Create key value pairs from the parsed data
        db_config = dict()
        parameters = parser.items(section)

        for p in parameters:
            db_config[p[0]] = p[1]

        return db_config
    except Exception as e:
        print(f"Failed to parse the db parameters: {e}")
        raise


def insert_row(data: dict, session: Any) -> None:
    """
    Inserts the given data row into corresponding country table, creates the table if it is not existing
    Args:
        data: Data row dictionary
        session: DB session

    Returns:
        None
    """
    # Parse country from data row
    country = data[COUNTRY_COLUMN]

    # Parse column names from data row
    columns = ",".join(data.keys())

    # Get the values to be inserted as string
    values = ",".join([f"'{str(x)}'" for x in data.values()])

    try:
        # Try inserting the value
        cursor = session.cursor()
        cursor.execute(
            INSERT_ENTRY.format(country_code=country, columns=columns, data_values=values)
        )
        session.commit()
    except Exception:
        # Exception occurred while inserting the values, try creating the table and try to add entry
        try:
            # Psycopg2 doesnt allow new query unless error session is rolled back
            session.rollback()

            cursor = session.cursor()
            cursor.execute(CREATE_TABLE.format(country_code=country))
            cursor.execute(
                INSERT_ENTRY.format(country_code=country, columns=columns, data_values=values)
            )

            session.commit()
        except Exception as e:
            print(e)
            # Operation failed, raise the error
            raise Exception
