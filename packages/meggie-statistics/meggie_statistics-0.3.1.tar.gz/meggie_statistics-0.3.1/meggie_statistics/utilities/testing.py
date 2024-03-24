import os
import json
import pkg_resources

from meggie.utilities.testing import BaseTestAction
from meggie.utilities.testing import create_test_experiment


class BaseStatisticsTestAction(BaseTestAction):

    def setup_experiment(self):
        self.experiment = create_test_experiment(
            self.dirpath, "test_experiment", n_subjects=10
        )
        self.experiment.activate_subject("sample_01-raw")

    def load_action_spec(self, action_name):
        action_path = pkg_resources.resource_filename("meggie_statistics", "actions")
        config_path = os.path.join(action_path, action_name, "configuration.json")
        with open(config_path, "r") as f:
            action_spec = json.load(f)
        return action_spec
