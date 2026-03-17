"""
Tests for .coderabbit.yaml configuration.

Verifies that the config file is structurally valid and that all
required settings are present with correct types and values.
"""

import os
import unittest

import yaml


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", ".coderabbit.yaml")

VALID_MODES = {"error", "warning", "disabled"}


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


class TestCodeRabbitYamlValidity(unittest.TestCase):
    """The YAML file must be parseable and return a non-empty mapping."""

    def test_file_exists(self):
        """The .coderabbit.yaml file must exist at the repo root."""
        self.assertTrue(os.path.isfile(CONFIG_PATH), msg=f"File not found: {CONFIG_PATH}")

    def test_file_is_parseable(self):
        """Loading the YAML must not raise an exception."""
        config = load_config()
        self.assertIsNotNone(config)

    def test_top_level_is_mapping(self):
        """Top-level document must be a dict, not a list or scalar."""
        config = load_config()
        self.assertIsInstance(config, dict)

    def test_file_is_not_empty(self):
        """Config file must not be empty (yaml.safe_load returns None for empty files)."""
        config = load_config()
        self.assertIsNotNone(config)
        self.assertNotEqual(config, {})

    def test_top_level_contains_only_reviews(self):
        """Top-level document must contain exactly one key: 'reviews'."""
        config = load_config()
        self.assertEqual(list(config.keys()), ["reviews"])

    def test_reviews_key_exists(self):
        """The 'reviews' top-level key must be present."""
        config = load_config()
        self.assertIn("reviews", config)

    def test_reviews_value_is_mapping(self):
        """The value of 'reviews' must be a dict."""
        config = load_config()
        self.assertIsInstance(config["reviews"], dict)

    def test_reviews_is_not_empty(self):
        """The 'reviews' mapping must not be an empty dict."""
        reviews = load_config()["reviews"]
        self.assertGreater(len(reviews), 0)


class TestReviewsTopLevelKeys(unittest.TestCase):
    """Required keys under 'reviews' must exist with correct types and values."""

    def setUp(self):
        self.reviews = load_config()["reviews"]

    def test_profile_key_exists(self):
        """'profile' must be present under 'reviews'."""
        self.assertIn("profile", self.reviews)

    def test_profile_is_string(self):
        """'profile' value must be a string."""
        self.assertIsInstance(self.reviews["profile"], str)

    def test_profile_value_is_assertive(self):
        """'profile' must equal 'assertive'."""
        self.assertEqual(self.reviews["profile"], "assertive")

    def test_review_status_key_exists(self):
        """'review_status' must be present under 'reviews'."""
        self.assertIn("review_status", self.reviews)

    def test_review_status_is_bool(self):
        """'review_status' must be a boolean."""
        self.assertIsInstance(self.reviews["review_status"], bool)

    def test_review_status_is_true(self):
        """'review_status' must be True."""
        self.assertTrue(self.reviews["review_status"])

    def test_review_details_key_exists(self):
        """'review_details' must be present under 'reviews'."""
        self.assertIn("review_details", self.reviews)

    def test_review_details_is_bool(self):
        """'review_details' must be a boolean."""
        self.assertIsInstance(self.reviews["review_details"], bool)

    def test_review_details_is_true(self):
        """'review_details' must be True."""
        self.assertTrue(self.reviews["review_details"])

    def test_high_level_summary_is_absent(self):
        """'high_level_summary' is not configured and must not appear under 'reviews'."""
        self.assertNotIn("high_level_summary", self.reviews)

    def test_reviews_known_keys(self):
        """'reviews' must only contain the known expected keys."""
        expected_keys = {
            "profile",
            "path_filters",
            "path_instructions",
            "review_status",
            "review_details",
            "pre_merge_checks",
        }
        actual_keys = set(self.reviews.keys())
        unexpected = actual_keys - expected_keys
        self.assertEqual(
            unexpected,
            set(),
            msg=f"Unexpected keys found under 'reviews': {unexpected}",
        )


class TestPathFilters(unittest.TestCase):
    """'path_filters' must be a non-empty list of glob pattern strings."""

    def setUp(self):
        self.path_filters = load_config()["reviews"]["path_filters"]

    def test_path_filters_key_exists(self):
        """'path_filters' must be present under 'reviews'."""
        reviews = load_config()["reviews"]
        self.assertIn("path_filters", reviews)

    def test_path_filters_is_list(self):
        """'path_filters' must be a list."""
        self.assertIsInstance(self.path_filters, list)

    def test_path_filters_has_two_entries(self):
        """'path_filters' must contain exactly two patterns."""
        self.assertEqual(len(self.path_filters), 2)

    def test_path_filters_all_strings(self):
        """Every entry in 'path_filters' must be a string."""
        for pattern in self.path_filters:
            with self.subTest(pattern=pattern):
                self.assertIsInstance(pattern, str)

    def test_path_filters_contains_main_java(self):
        """'path_filters' must include the main Java source glob."""
        self.assertIn("src/main/java/**/*.java", self.path_filters)

    def test_path_filters_contains_test_java(self):
        """'path_filters' must include the test Java source glob."""
        self.assertIn("src/test/java/**/*.java", self.path_filters)

    def test_path_filters_no_empty_strings(self):
        """No entry in 'path_filters' should be an empty string."""
        for pattern in self.path_filters:
            with self.subTest(pattern=pattern):
                self.assertNotEqual(pattern.strip(), "")


class TestPathInstructions(unittest.TestCase):
    """'path_instructions' must be a list of well-formed instruction objects."""

    def setUp(self):
        self.path_instructions = load_config()["reviews"]["path_instructions"]

    def test_path_instructions_key_exists(self):
        """'path_instructions' must be present under 'reviews'."""
        reviews = load_config()["reviews"]
        self.assertIn("path_instructions", reviews)

    def test_path_instructions_is_list(self):
        """'path_instructions' must be a list."""
        self.assertIsInstance(self.path_instructions, list)

    def test_path_instructions_is_not_empty(self):
        """'path_instructions' must have at least one entry."""
        self.assertGreater(len(self.path_instructions), 0)

    def test_path_instructions_entries_are_mappings(self):
        """Each entry in 'path_instructions' must be a dict."""
        for entry in self.path_instructions:
            with self.subTest(entry=entry):
                self.assertIsInstance(entry, dict)

    def test_path_instructions_entries_have_path_key(self):
        """Each instruction entry must have a 'path' key."""
        for entry in self.path_instructions:
            with self.subTest(entry=entry):
                self.assertIn("path", entry)

    def test_path_instructions_entries_have_instructions_key(self):
        """Each instruction entry must have an 'instructions' key."""
        for entry in self.path_instructions:
            with self.subTest(entry=entry):
                self.assertIn("instructions", entry)

    def test_path_instructions_entry_path_is_string(self):
        """The 'path' field in each instruction entry must be a string."""
        for entry in self.path_instructions:
            with self.subTest(entry=entry):
                self.assertIsInstance(entry["path"], str)

    def test_path_instructions_entry_instructions_is_string(self):
        """The 'instructions' field in each instruction entry must be a string."""
        for entry in self.path_instructions:
            with self.subTest(entry=entry):
                self.assertIsInstance(entry["instructions"], str)

    def test_path_instructions_first_path_matches_test_java(self):
        """The first instruction entry must target the test Java glob."""
        self.assertEqual(self.path_instructions[0]["path"], "src/test/java/**/*.java")

    def test_path_instructions_first_entry_instructions_not_empty(self):
        """The first instruction entry must have non-empty instructions."""
        instructions = self.path_instructions[0]["instructions"]
        self.assertTrue(instructions.strip())

    def test_path_instructions_first_entry_mentions_junit(self):
        """The first instruction entry must reference JUnit (framework context check)."""
        instructions = self.path_instructions[0]["instructions"]
        self.assertIn("Junit 5", instructions)


class TestPreMergeChecksStructure(unittest.TestCase):
    """'pre_merge_checks' must be well-formed with the expected sub-sections."""

    def setUp(self):
        config = load_config()
        self.pre_merge = config["reviews"]["pre_merge_checks"]

    def test_pre_merge_checks_key_exists(self):
        """'pre_merge_checks' must be present under 'reviews'."""
        reviews = load_config()["reviews"]
        self.assertIn("pre_merge_checks", reviews)

    def test_pre_merge_checks_is_mapping(self):
        """'pre_merge_checks' must be a dict."""
        self.assertIsInstance(self.pre_merge, dict)

    def test_pre_merge_checks_has_expected_keys(self):
        """'pre_merge_checks' must contain all expected sub-check keys."""
        expected_keys = {"docstrings", "title", "description", "issue_assessment", "custom_checks"}
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, self.pre_merge)

    # --- docstrings ---

    def test_docstrings_key_exists(self):
        """'docstrings' must be present under 'pre_merge_checks'."""
        self.assertIn("docstrings", self.pre_merge)

    def test_docstrings_is_mapping(self):
        """'docstrings' value must be a dict."""
        self.assertIsInstance(self.pre_merge["docstrings"], dict)

    def test_docstrings_mode_exists(self):
        """'docstrings.mode' must be present."""
        self.assertIn("mode", self.pre_merge["docstrings"])

    def test_docstrings_mode_is_string(self):
        """'docstrings.mode' must be a string."""
        self.assertIsInstance(self.pre_merge["docstrings"]["mode"], str)

    def test_docstrings_mode_is_error(self):
        """'docstrings.mode' must equal 'error'."""
        self.assertEqual(self.pre_merge["docstrings"]["mode"], "error")

    def test_docstrings_mode_is_valid(self):
        """'docstrings.mode' must be one of the valid mode values."""
        self.assertIn(self.pre_merge["docstrings"]["mode"], VALID_MODES)

    def test_docstrings_threshold_exists(self):
        """'docstrings.threshold' must be present."""
        self.assertIn("threshold", self.pre_merge["docstrings"])

    def test_docstrings_threshold_is_numeric(self):
        """'docstrings.threshold' must be an integer."""
        self.assertIsInstance(self.pre_merge["docstrings"]["threshold"], int)

    def test_docstrings_threshold_value(self):
        """'docstrings.threshold' must equal 50."""
        self.assertEqual(self.pre_merge["docstrings"]["threshold"], 50)

    def test_docstrings_threshold_in_valid_range(self):
        """'docstrings.threshold' must be between 0 and 100 inclusive."""
        threshold = self.pre_merge["docstrings"]["threshold"]
        self.assertGreaterEqual(threshold, 0)
        self.assertLessEqual(threshold, 100)

    # --- title ---

    def test_title_key_exists(self):
        """'title' must be present under 'pre_merge_checks'."""
        self.assertIn("title", self.pre_merge)

    def test_title_is_mapping(self):
        """'title' value must be a dict."""
        self.assertIsInstance(self.pre_merge["title"], dict)

    def test_title_mode_is_warning(self):
        """'title.mode' must equal 'warning'."""
        self.assertEqual(self.pre_merge["title"]["mode"], "warning")

    def test_title_mode_is_valid(self):
        """'title.mode' must be one of the valid mode values."""
        self.assertIn(self.pre_merge["title"]["mode"], VALID_MODES)

    def test_title_requirements_exists(self):
        """'title.requirements' must be present."""
        self.assertIn("requirements", self.pre_merge["title"])

    def test_title_requirements_is_string(self):
        """'title.requirements' must be a string."""
        self.assertIsInstance(self.pre_merge["title"]["requirements"], str)

    def test_title_requirements_not_empty(self):
        """'title.requirements' must not be an empty string."""
        self.assertTrue(self.pre_merge["title"]["requirements"].strip())

    def test_title_requirements_mentions_character_limit(self):
        """'title.requirements' must reference the 50-character limit."""
        self.assertIn("50", self.pre_merge["title"]["requirements"])

    # --- description ---

    def test_description_key_exists(self):
        """'description' must be present under 'pre_merge_checks'."""
        self.assertIn("description", self.pre_merge)

    def test_description_is_mapping(self):
        """'description' value must be a dict."""
        self.assertIsInstance(self.pre_merge["description"], dict)

    def test_description_mode_is_error(self):
        """'description.mode' must equal 'error'."""
        self.assertEqual(self.pre_merge["description"]["mode"], "error")

    def test_description_mode_is_valid(self):
        """'description.mode' must be one of the valid mode values."""
        self.assertIn(self.pre_merge["description"]["mode"], VALID_MODES)

    # --- issue_assessment ---

    def test_issue_assessment_key_exists(self):
        """'issue_assessment' must be present under 'pre_merge_checks'."""
        self.assertIn("issue_assessment", self.pre_merge)

    def test_issue_assessment_is_mapping(self):
        """'issue_assessment' value must be a dict."""
        self.assertIsInstance(self.pre_merge["issue_assessment"], dict)

    def test_issue_assessment_mode_is_warning(self):
        """'issue_assessment.mode' must equal 'warning'."""
        self.assertEqual(self.pre_merge["issue_assessment"]["mode"], "warning")

    def test_issue_assessment_mode_is_valid(self):
        """'issue_assessment.mode' must be one of the valid mode values."""
        self.assertIn(self.pre_merge["issue_assessment"]["mode"], VALID_MODES)

    # --- custom_checks ---

    def test_custom_checks_key_exists(self):
        """'custom_checks' must be present under 'pre_merge_checks'."""
        self.assertIn("custom_checks", self.pre_merge)

    def test_custom_checks_is_list(self):
        """'custom_checks' must be a list."""
        self.assertIsInstance(self.pre_merge["custom_checks"], list)

    def test_custom_checks_is_not_empty(self):
        """'custom_checks' must contain at least one entry."""
        self.assertGreater(len(self.pre_merge["custom_checks"]), 0)

    def test_custom_checks_entries_are_mappings(self):
        """Each entry in 'custom_checks' must be a dict."""
        for check in self.pre_merge["custom_checks"]:
            with self.subTest(check=check):
                self.assertIsInstance(check, dict)

    def test_custom_checks_entries_have_name(self):
        """Each custom check must have a 'name' key."""
        for check in self.pre_merge["custom_checks"]:
            with self.subTest(check=check):
                self.assertIn("name", check)

    def test_custom_checks_entries_name_is_string(self):
        """Each custom check 'name' must be a non-empty string."""
        for check in self.pre_merge["custom_checks"]:
            with self.subTest(check=check):
                self.assertIsInstance(check["name"], str)
                self.assertTrue(check["name"].strip())

    def test_custom_checks_entries_have_mode(self):
        """Each custom check must have a 'mode' key."""
        for check in self.pre_merge["custom_checks"]:
            with self.subTest(check=check):
                self.assertIn("mode", check)

    def test_custom_checks_entries_mode_is_valid(self):
        """Each custom check 'mode' must be one of the valid mode values."""
        for check in self.pre_merge["custom_checks"]:
            with self.subTest(check=check):
                self.assertIn(check["mode"], VALID_MODES)

    def test_custom_checks_entries_have_instructions(self):
        """Each custom check must have an 'instructions' key."""
        for check in self.pre_merge["custom_checks"]:
            with self.subTest(check=check):
                self.assertIn("instructions", check)

    def test_custom_checks_entries_instructions_not_empty(self):
        """Each custom check 'instructions' must be a non-empty string."""
        for check in self.pre_merge["custom_checks"]:
            with self.subTest(check=check):
                self.assertIsInstance(check["instructions"], str)
                self.assertTrue(check["instructions"].strip())

    def test_custom_checks_first_entry_name(self):
        """The first custom check must be 'Undocumented Breaking Changes'."""
        self.assertEqual(self.pre_merge["custom_checks"][0]["name"], "Undocumented Breaking Changes")

    def test_custom_checks_first_entry_mode_is_warning(self):
        """The first custom check mode must be 'warning'."""
        self.assertEqual(self.pre_merge["custom_checks"][0]["mode"], "warning")


class TestNegativeAndBoundaryCases(unittest.TestCase):
    """Boundary and negative cases to strengthen confidence in config integrity."""

    def setUp(self):
        self.config = load_config()
        self.reviews = self.config["reviews"]
        self.pre_merge = self.reviews["pre_merge_checks"]

    def test_no_extra_top_level_keys(self):
        """Config must have exactly one top-level key ('reviews'); no stray keys."""
        self.assertEqual(len(self.config), 1)

    def test_profile_is_not_none(self):
        """'profile' must not be None (an empty YAML key would parse as None)."""
        self.assertIsNotNone(self.reviews["profile"])

    def test_pre_merge_modes_are_not_disabled(self):
        """
        None of the pre_merge_checks sub-checks that have a 'mode' field should
        be set to 'disabled', ensuring all checks are actively enforced.
        """
        for key, value in self.pre_merge.items():
            if isinstance(value, dict) and "mode" in value:
                with self.subTest(check=key):
                    self.assertNotEqual(
                        value["mode"],
                        "disabled",
                        msg=f"pre_merge_checks.{key}.mode should not be 'disabled'",
                    )

    def test_path_filters_patterns_contain_java_extension(self):
        """All path filter patterns must end with '*.java' (Java repo guard)."""
        for pattern in self.reviews["path_filters"]:
            with self.subTest(pattern=pattern):
                self.assertTrue(
                    pattern.endswith("*.java"),
                    msg=f"Pattern does not end with '*.java': {pattern}",
                )

    def test_docstrings_threshold_not_zero(self):
        """'docstrings.threshold' must not be 0 — a zero threshold is effectively disabled."""
        self.assertNotEqual(self.pre_merge["docstrings"]["threshold"], 0)

    def test_reviews_bool_flags_are_actual_booleans_not_strings(self):
        """
        YAML allows 'true' as a string; verify review_status and review_details
        are parsed as Python bool, not the string 'true'.
        """
        self.assertNotIsInstance(self.reviews["review_status"], str)
        self.assertNotIsInstance(self.reviews["review_details"], str)

    def test_custom_checks_instructions_mention_changelog(self):
        """
        The breaking-changes custom check instructions must reference CHANGELOG.md
        as required by the project's documentation policy.
        """
        breaking_change_check = next(
            (c for c in self.pre_merge["custom_checks"] if c["name"] == "Undocumented Breaking Changes"),
            None,
        )
        self.assertIsNotNone(breaking_change_check, msg="'Undocumented Breaking Changes' custom check not found")
        self.assertIn("CHANGELOG.md", breaking_change_check["instructions"])

    def test_path_instructions_path_is_also_in_path_filters(self):
        """
        Every path in 'path_instructions' should have a matching glob in
        'path_filters' to ensure instructions are reachable by the reviewer.
        """
        filters = set(self.reviews["path_filters"])
        for entry in self.reviews["path_instructions"]:
            with self.subTest(path=entry["path"]):
                self.assertIn(
                    entry["path"],
                    filters,
                    msg=f"path_instructions path '{entry['path']}' has no matching path_filter",
                )


if __name__ == "__main__":
    unittest.main()