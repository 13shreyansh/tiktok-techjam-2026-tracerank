import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_pure_campaign_experiment.py"
SPEC = importlib.util.spec_from_file_location("run_pure_campaign_experiment", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class PureCampaignRecordTests(unittest.TestCase):
    def test_all_evaluation_surfaces_are_copied_to_attempt_record(self):
        result = {
            "valid": {"primary": 0.61},
            "forward_valid": {"primary": 0.60},
            "random_validation": {"primary": 0.59},
            "robustness": {"minimum_primary": 0.58},
        }

        self.assertEqual(
            MODULE.result_metric_fields(result),
            {
                "valid": {"primary": 0.61},
                "valid_primary": 0.61,
                "forward_valid": {"primary": 0.60},
                "random_validation": {"primary": 0.59},
                "robustness": {"minimum_primary": 0.58},
            },
        )

    def test_failed_attempt_projects_null_metrics(self):
        self.assertEqual(
            MODULE.result_metric_fields(None),
            {
                "valid": None,
                "valid_primary": None,
                "forward_valid": None,
                "random_validation": None,
                "robustness": None,
            },
        )


if __name__ == "__main__":
    unittest.main()
