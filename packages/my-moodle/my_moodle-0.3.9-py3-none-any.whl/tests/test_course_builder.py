"""
Test cases for the project.
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
"""

import unittest
from my_moodle import CourseMarkdownBuilder, JsonUtility, MoodleDataUtility


class CourseBuilderTestSuite(unittest.TestCase):
    """Module for testing the MoodleDataDownloader class."""

    def test_course_builder(self) -> None:
        """Test the CourseMarkdownBuilder class."""

        program_name = "Business with Computing"
        test_file_path = "test-data/program-business-with-computing-courses.json"
        courses_json = JsonUtility.load_json_from_file(test_file_path).get(
            "courses", []
        )

        for course in courses_json:
            if course.get("coursecategory") == "N-TUTORR":
                continue

            course_name: str = MoodleDataUtility.clean_course_name(
                    course.get("fullname", "")
                )
            course_builder = CourseMarkdownBuilder(
                program_name, course_name, course.get("viewurl")
            )
            course_name1: str = MoodleDataUtility.convert_to_slug(
                MoodleDataUtility.clean_course_name(course.get("fullname", ""))
            )
            course_contents_file = f"test-data/course-{course_name1}-contents.json"
            course_dir = MoodleDataUtility.parse_course_dir(course)
            print(course_contents_file)
            courses_contents_json = JsonUtility.load_json_from_file(
                course_contents_file
            )
            course_builder.process_course_contents(courses_contents_json)
            course_builder.save_to_file(f"data/{course_dir}/readme.md")


if __name__ == "__main__":
    unittest.main()
