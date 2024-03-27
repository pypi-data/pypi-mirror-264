"""
Test the variables in eastats.py
"""

import pandas as pd
import numpy as np
import unittest
import warnings
from pyeach import eastats
from tests.config import RANDOM_SEED


class TestEAStats(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", category=RuntimeWarning)

    def test_ci_int(self):
        self.assertEqual(eastats.ci_int(pd.Series([0,1])), (-3.9923217661378816, 4.992321766137882))
        self.assertEqual(eastats.ci_int(pd.Series([0,1]), distr="bin"), (0.0, 1.0))

    def test_mean_t_test(self):
        self.assertEqual(eastats.mean_t_test(pd.Series([0,1]), 1), 0.42264973081037427)

    def test_geo_mean(self):
        self.assertEqual(eastats.geo_mean(pd.Series([0,2])), 0.0)
        self.assertEqual(eastats.geo_mean(pd.Series([0,2]), include_zeros=False), 2.0)
        self.assertEqual(eastats.geo_mean(pd.Series([1,2])), 1.414213562373095)

    def test_smape(self):
        self.assertEqual(eastats.smape(pd.Series([1,2]), pd.Series([2,4])), 0.3333333333333333)

    def test_population_adj_weights(self):
        np.random.seed(RANDOM_SEED)
        N = 10

        patients = [f"PT{x}" for x in np.arange(0, N, 1)]
        counties = np.random.choice(["Guilford", "Alamance"], size=N, replace=True, p=[0.7, 0.3])
        sexes = np.random.choice(["Male", "Female"], size=N, replace=True, p=[0.5, 0.5])
        race_eth = np.random.choice(["Black", "White", "Hispanic", "Asian", "Other"], size=N, replace=True, 
                                    p=[0.30, 0.50, 0.10, 0.05, 0.05])
        age_buckets = np.random.choice(["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-64", "65+"], size=N, replace=True,
                                    p=[0.05, 0.05, 0.10, 0.2, 0.2, 0.15, 0.15, 0.10])
        
        df_example = pd.DataFrame({
            "PatientID": patients,
            "CountyDSC": counties,
            "SexDSC": sexes, 
            "RaceEthnicity": race_eth, 
            "AgeBucket": age_buckets
        })

        df_weights = eastats.population_adj_weights(df_example)
        test_weights = list(np.round(df_weights["weight"], 2))
        weights = [0.33, 0.33, 0.33, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14]
        
        self.assertEqual(test_weights, weights)

    def test_population_adjusted_weights(self):
        np.random.seed(RANDOM_SEED)
        N = 100

        county_to_tract = {"Guilford": ["01", "02"], "Alamance": ["03", "04"]}

        patients = [f"PT{x}" for x in np.arange(0, N, 1)]
        counties = np.random.choice(["Guilford", "Alamance"], size=N, replace=True, p=[0.7, 0.3])
        tracts = [np.random.choice(county_to_tract[c], size=1)[0] for c in counties]
        sexes = np.random.choice(["Male", "Female"], size=N, replace=True, p=[0.5, 0.5])
        race_eth = np.random.choice(["Black", "White", "Hispanic", "Asian", "Other"], size=N, replace=True, 
                                    p=[0.30, 0.50, 0.10, 0.05, 0.05])
        age_buckets = np.random.choice(["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-64", "65+"], size=N, replace=True,
                                    p=[0.05, 0.05, 0.10, 0.20, 0.20, 0.15, 0.15, 0.10])
        targets = np.random.choice([0, 1], size=N, replace=True, p=[0.25, 0.75])

        df_example = pd.DataFrame({
            "PatientID": patients,
            "CountyDSC": counties,
            "CensusTractGEOID": tracts,
            "SexDSC": sexes, 
            "RaceEthnicity": race_eth, 
            "AgeBucket": age_buckets,
            "target": targets
        })

        df_weights = eastats.population_adjusted_rates(df_example, target="target")
        test_weights = list(np.round(df_weights["target_adj_p"], 2))

        weights = [49.64, 56.90, 70.0, 36.67]

        self.assertEqual(test_weights, weights)


if __name__ == '__main__':
    unittest.main()
