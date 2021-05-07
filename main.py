import configparser
import sys

from database_manager import db_connection
from extractor.extractor import DataExtractor
from utilities import get_database_config, insert_row


def execute():
    # Open file
    with open(filename, "r") as f:

        # Read header line and create extractor
        header = f.readline()
        extractor = DataExtractor(header[:-1], date_format=date_format)

        db_config = get_database_config()
        with db_connection(db_config) as session:
            # Read all lines till end and parse the data
            while True:
                d = f.readline()

                # If d is empty then reached end of the file
                if d == '':
                    break

                # Remove new line character and get data dictionary for the row
                row_data = extractor.get_row_data(d[:-1])
                insert_row(row_data, session)

    print("Execution complete")


if __name__ == '__main__':
    filename = sys.argv[1]
    date_format = sys.argv[2]
    execute()
