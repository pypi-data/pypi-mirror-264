"""
Test the functions in eadb.py
"""

import unittest
import warnings
from tests.config import server
from pyeach.eadb import query_edw
from pyeach.eadb import query_socrata


class TestEADB(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", category=ResourceWarning)

    def test_query_edw_string(self):
        query = """
        SET NOCOUNT ON;

        SELECT TOP 100 *
        FROM Epic.Encounter.PatientEncounter;
        """

        string_test = query_edw(server=server, query=query, verbose=False)
        self.assertEqual(string_test.shape, (100, 174))
    
    def test_query_edw_file(self):
        file = "tests/sql/test_query.sql"
        file_test = query_edw(server=server, file=file, verbose=False)
        self.assertEqual(file_test.shape, (100, 174))

    def test_query_socrata(self):
        from tests.config import cdc_token as token, cdc_username as usrnm, cdc_password as psswd

        query = """
        select
            countyname,
            locationid,
            measure,
            short_question_text,
            data_value,
            low_confidence_limit,
            high_confidence_limit,
            data_value_unit
        where
            statedesc = 'North Carolina'
            and countyname in ('Guilford', 'Alamance', 'Rockingham', 'Randolph', 'Forsyth', 'Caswell')
        limit 100
        """

        test_socrata = query_socrata("data.cdc.gov", "cwsq-ngmh", query=query,
                                     token=token, usrnm=usrnm, psswd=psswd)
        self.assertEqual(test_socrata.shape[0], 100)

if __name__ == '__main__':
    unittest.main()
