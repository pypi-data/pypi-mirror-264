"""
Test cases for the project.
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
"""

import unittest
from my_moodle import ProgramMarkdownBuilder, JsonUtility


class ProgramBuilderTestSuite(unittest.TestCase):
    """Module for testing the MoodleDataDownloader class."""

    def test_program_builder(self) -> None:
        """Test the ProgramMarkdownBuilder class."""

        program_name = "Business with Computing"

        test_file_path = "test-data/program-business-with-computing-courses.json"
        courses_json = JsonUtility.load_json_from_file(test_file_path)
        program_builder = ProgramMarkdownBuilder(program_name)
        program_builder.process_courses_json(courses_json.get("courses", []))

        program_builder.save_to_file("data/readme.md")


if __name__ == "__main__":
    unittest.main()
