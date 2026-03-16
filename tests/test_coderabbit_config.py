"""
Tests for .coderabbit.yaml configuration.

This PR removed the following top-level review settings:
  - profile: "assertive"
  - high_level_summary: true
  - review_status: true
  - review_details: true

Tests verify that:
  1. The YAML file is valid and parseable.
  2. The removed keys are no longer present (regression guard).
  3. The retained structure (pre_merge_checks) is correct.
"""

import os
import unittest
import yaml


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", ".coderabbit.yaml")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


class TestCodeRabbitYamlValidity(unittest.TestCase):
    """The YAML file must be parseable and return a mapping."""

    def test_file_is_parseable(self):
        """Loading the YAML file must not raise an exception."""
        config = load_config()
        self.assertIsNotNone(config)

    def test_top_level_is_mapping(self):
        """The top-level document must be a dict, not a list or scalar."""
        config = load_config()
        self.assertIsInstance(config, dict)

    def test_reviews_key_exists(self):
        """The 'reviews' top-level key must be present."""
        config = load_config()
        self.assertIn("reviews", config)

    def test_reviews_value_is_mapping(self):
        """The value of 'reviews' must be a dict."""
        config = load_config()
        self.assertIsInstance(config["reviews"], dict)


class TestRemovedReviewsKeys(unittest.TestCase):
    """
    Regression tests: keys removed in this PR must NOT be present.
    If any of these keys reappear, these tests will catch the regression.
    """

    def setUp(self):
        self.reviews = load_config()["reviews"]

    def test_profile_key_is_removed(self):
        """'profile' was removed and must not exist under 'reviews'."""
        self.assertNotIn("profile", self.reviews)

    def test_high_level_summary_key_is_removed(self):
        """'high_level_summary' was removed and must not exist under 'reviews'."""
        self.assertNotIn("high_level_summary", self.reviews)

    def test_review_status_key_is_removed(self):
        """'review_status' was removed and must not exist under 'reviews'."""
        self.assertNotIn("review_status", self.reviews)

    def test_review_details_key_is_removed(self):
        """'review_details' was removed and must not exist under 'reviews'."""
        self.assertNotIn("review_details", self.reviews)

    def test_no_unexpected_top_level_review_keys(self):
        """
        Boundary test: 'reviews' should contain only 'pre_merge_checks' after
        this PR. If new unknown keys are added later this test will flag them.
        """
        allowed_keys = {"pre_merge_checks"}
        actual_keys = set(self.reviews.keys())
        unexpected = actual_keys - allowed_keys
        self.assertEqual(
            unexpected,
            set(),
            msg=f"Unexpected keys found under 'reviews': {unexpected}",
        )


class TestPreMergeChecksStructure(unittest.TestCase):
    """The pre_merge_checks block retained after this PR must be well-formed."""

    def setUp(self):
        config = load_config()
        self.pre_merge = config["reviews"]["pre_merge_checks"]

    def test_pre_merge_checks_key_exists(self):
        """'pre_merge_checks' must be present under 'reviews'."""
        config = load_config()
        self.assertIn("pre_merge_checks", config["reviews"])

    def test_pre_merge_checks_is_mapping(self):
        """'pre_merge_checks' value must be a dict."""
        self.assertIsInstance(self.pre_merge, dict)

    def test_docstrings_key_exists(self):
        """'docstrings' must be present under 'pre_merge_checks'."""
        self.assertIn("docstrings", self.pre_merge)

    def test_docstrings_mode_is_error(self):
        """'docstrings.mode' must equal 'error' (unchanged by this PR)."""
        self.assertEqual(self.pre_merge["docstrings"]["mode"], "error")

    def test_docstrings_mode_is_string(self):
        """'docstrings.mode' must be a string, not a boolean or number."""
        self.assertIsInstance(self.pre_merge["docstrings"]["mode"], str)


class TestNegativeCases(unittest.TestCase):
    """Negative / boundary cases to strengthen confidence."""

    def test_file_is_not_empty(self):
        """The config file must not be empty (yaml.safe_load returns None for empty files)."""
        config = load_config()
        self.assertIsNotNone(config)
        self.assertNotEqual(config, {})

    def test_reviews_is_not_empty(self):
        """The 'reviews' mapping must not be an empty dict after the removals."""
        reviews = load_config()["reviews"]
        self.assertGreater(len(reviews), 0)

    def test_removed_profile_value_not_assertive(self):
        """
        Even if 'profile' were somehow present with a different value,
        the old value 'assertive' must not appear anywhere under 'reviews'.
        """
        reviews = load_config()["reviews"]
        for value in reviews.values():
            self.assertNotEqual(value, "assertive")

    def test_yaml_has_no_duplicate_keys(self):
        """
        YAML technically allows duplicate keys (last value wins).
        Verify the parsed config has the expected number of top-level keys.
        """
        config = load_config()
        # Top level should have exactly one key: 'reviews'
        self.assertEqual(list(config.keys()), ["reviews"])


if __name__ == "__main__":
    unittest.main()