"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
CourseMarkdownBuilder Class
"""

from .moodle_data_utility import MoodleDataUtility
from .markdown_document import MarkdownDocument
from .markdown_methods import MarkdownLink


class ProgramMarkdownBuilder:
    """Program Markdown Builder"""

    def __init__(self, program_name: str):
        """Initialise the CourseMarkdownBuilder

        Args:
            program_name (str): The program name
            course_name (str): The course name
            course_url (str): The course URL
        """
        self._markdown_document = MarkdownDocument()
        """Markdown document"""

        self._program_name = program_name

    def __str__(self) -> str:
        """Return the string representation of the CourseMarkdownBuilder

        Returns:
            str: The string representation of the CourseMarkdownBuilder
        """
        return str(self._markdown_document)

    def add_program(self, program_name: str) -> None:
        """Add a program

        Args:
            program_name (str): The program name
        """
        self._markdown_document.write_h1(program_name)

    def add_category(self, category_name: str) -> None:
        """Add a category

        Args:
            category_name (str): The category name
        """
        self._markdown_document.write_h2(category_name)

    def add_course(self, course_name: str, course_path: str) -> None:
        """Add a course

        Args:
            course_name (str): The course name
            course_path (str): The course path
        """
        self._markdown_document.write_bullet_link_line(
            MarkdownLink(course_name, f"{course_path}/readme.md", course_name)
        )

    def save_to_file(self, file_path: str, encoding: str = "utf-8") -> None:
        """Saves the markdown document to a file

        Args:
            file_path (str): The file path
        """
        with open(file_path, "w", encoding=encoding) as file:
            file.write(str(self))

    def process_courses_json(self, courses_json: dict) -> None:
        """Process the courses json

        Args:
            courses_json (dict): The courses json.
        """

        self.add_program(self._program_name)
        courses_by_category = MoodleDataUtility.group_courses_by_category(courses_json)
        for category, courses in courses_by_category.items():
            self.add_category(category)
            courses = sorted(courses, key=lambda x: x.get("fullname", ""))
            for course in courses:
                course_id = course.get("id", "")
                full_name = course.get("fullname", "")
                path = f"{MoodleDataUtility.convert_to_slug(full_name)}-id-{course_id}"
                self.add_course(
                    MoodleDataUtility.clean_course_name(full_name), path.lower()
                )
            self._markdown_document.write_line()
        self._markdown_document.write_hr()
