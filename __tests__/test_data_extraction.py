from unittest import TestCase

from extractor.extractor import DataExtractor
from utilities import get_named_tuple_header, convert_date


class TestDataExtraction(TestCase):
    def setUp(self) -> None:
        self.dummy_header_data = "|H|Customer_Name|Customer_Id|Open_Date|Last_Consulted_Date|" \
                                 "Vaccination_Id|Dr_Name|State|Country|DOB|Is_Active"
        self.dummy_data_row1 = "|D|Alex|123457|20101012|20121013|MVD|Paul|SA|USA|19870603|A"

    def test_result(self):
        data_extractor = DataExtractor(self.dummy_header_data, 'YYYYMMDD')
        result = data_extractor.get_row_data(self.dummy_data_row1)
        self.assertEqual(result['Customer_Name'], 'Alex')
        self.assertEqual(result['Customer_Id'], '123457')
        self.assertEqual(result['Open_Date'], '2010-10-12')
        self.assertEqual(result['Last_Consulted_Date'], '2012-10-13')
        self.assertEqual(result['Vaccination_Id'], 'MVD')
        self.assertEqual(result['Dr_Name'], 'Paul')
        self.assertEqual(result['State'], 'SA')
        self.assertEqual(result['Country'], 'USA')
        self.assertEqual(result['DOB'], '1987-06-03')
        self.assertEqual(result['Is_Active'], 'A')

    def test_exception(self):
        with self.assertRaises(Exception):
            DataExtractor(self.dummy_header_data, 'DUMMY')


class TestUtilityMethods(TestCase):
    def test_meth_get_named_tuple_header(self):
        dummy_header_data = "|H|Customer_Name|Customer_Id|Open_Date|Last_Consulted_Date" \
                            "|Vaccination_Id|Dr_Name|State|Country|DOB|Is_Active"
        data_fields = get_named_tuple_header(dummy_header_data)
        self.assertEqual(data_fields['Customer_Name'], 0)
        self.assertEqual(data_fields['Customer_Id'], 1)
        self.assertEqual(data_fields['Open_Date'], 2)
        self.assertEqual(data_fields['Last_Consulted_Date'], 3)
        self.assertEqual(data_fields['Vaccination_Id'], 4)
        self.assertEqual(data_fields['Dr_Name'], 5)
        self.assertEqual(data_fields['State'], 6)
        self.assertEqual(data_fields['Country'], 7)
        self.assertEqual(data_fields['DOB'], 8)
        self.assertEqual(data_fields['Is_Active'], 9)

    def test_convert_date(self):
        raw_data1 = '2020025'
        raw_data2 = '19851008'
        raw_data3 = '812021'
        self.assertEqual(
            convert_date(raw_data1, '%Y%m%d'),
            '2020-02-05'
        )
        self.assertEqual(
            convert_date(raw_data2, '%Y%m%d'),
            '1985-10-08'
        )

        self.assertEqual(
            convert_date(raw_data3, '%d%m%Y'),
            '2021-01-08'
        )
