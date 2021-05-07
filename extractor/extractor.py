from configs import DATE_FORMAT_MAPPERS, DATE_COLUMNS
from utilities import get_named_tuple_header, convert_date


class DataExtractor:
    """
    Extract the line present in a file and converts the result into dictionary
    """
    def __init__(self, header_row: str, date_format: str, date_keys: list = DATE_COLUMNS, separator="|"):
        """
        Args:
            header_row: Header row of the file
            date_format: Date format in the file
            date_keys: Fields containing date values
            separator: Separator of fields in the file
        """

        self.header_fields = get_named_tuple_header(header_row, separator)
        self.separator = separator
        self.date_keys = date_keys

        try:
            self.date_matcher = DATE_FORMAT_MAPPERS[date_format]
        except KeyError:
            raise Exception(f"No formula present for handling the format {date_format}")

    def get_row_data(self, raw_data_row: str) -> dict:
        """
        Converts the data row into dictionary
        Args:
            raw_data_row: Data row which needs to be parsed

        Returns:
            The dictionary with data values
        """
        data_row_values = dict()
        data_row_list = raw_data_row.split(self.separator)[2:]

        # For every header field extract the data from data row and create a dictionary
        for k, v in self.header_fields.items():
            if k in self.date_keys:
                # If key is a date field extract the date in correct YYYY-MM-DD format
                # which is expected in postgres query
                data_row_values[k] = convert_date(data_row_list[v], self.date_matcher)
            else:
                data_row_values[k] = data_row_list[v]

        return data_row_values
