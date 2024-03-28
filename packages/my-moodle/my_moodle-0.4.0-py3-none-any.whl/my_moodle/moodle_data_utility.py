"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Moodle data utility Class
"""

import html
import re
import time
import requests

from pandas import DataFrame
from IPython.core.display import HTML
from my_moodle.course_status import CourseStatus
from my_moodle.enrolled_users_fields import EnrolledUsersFields


class MoodleDataUtility:
    """Moodle data utility functions"""

    @staticmethod
    def create_tiny_url(url: str) -> str:
        """Shorten the URL using https://tinyurl.com

        Args:
            url (str): The URL to shorten

        Returns:
            str: The shortened URL
        """
        base_url = "http://tinyurl.com/api-create.php?url="
        response = requests.get(base_url + url, timeout=5)
        short_url = response.text
        return short_url

    @staticmethod
    def create_data_frame(
        courses: list,
        id_column: str = "id",
        fullname_column: str = "fullname",
        url_column: str = "viewurl",
    ) -> DataFrame:
        """Create a DataFrame from the courses list

        Args:
            courses (list): The list of courses
            id_column (str, optional): The column name for the course id. Defaults to "id".
            fullname_column (str, optional): The column name for the course fullname.
            Defaults to "fullname".
            url_column (str, optional): The column name for the course viewurl.
            Defaults to "viewurl".

        Returns:
            DataFrame: The DataFrame of courses
        """
        columns: list[str] = [id_column, fullname_column, url_column]
        courses_data_frame = DataFrame(courses, columns=columns)
        if courses == []:
            return courses_data_frame
        courses_data_frame = courses_data_frame[columns]
        return courses_data_frame

    @staticmethod
    def create_data_frame_with_tiny_url(
        courses: list,
        id_column: str = "id",
        fullname_column: str = "fullname",
        url_column: str = "viewurl",
    ) -> DataFrame:
        """Create a DataFrame from the courses list with a tiny url column

        Args:
            courses (list): The list of courses
            id_column (str, optional): The column name for the course id. Defaults to "id".
            fullname_column (str, optional): The column name for the course fullname.
            Defaults to "fullname".
            url_column (str, optional): The column name for the course viewurl.
            Defaults to "viewurl".

        Returns:
            DataFrame: The DataFrame of courses
        """

        for course in courses:
            course["tiny-url"] = MoodleDataUtility.create_tiny_url(course[url_column])
        columns: list[str] = [id_column, fullname_column, "tiny-url"]

        courses_data_frame = DataFrame(courses, columns=columns)
        if courses == []:
            return courses_data_frame
        courses_data_frame = courses_data_frame[columns]
        return courses_data_frame

    @staticmethod
    def courses_json_to_html(courses: list) -> HTML:
        """Display the courses as an HTML table

        Args:
            courses (list): The list of courses

        Returns:
            HTML: The HTML table
        """
        return HTML(
            MoodleDataUtility.create_data_frame(courses).to_html(
                render_links=True, escape=False, index=False
            )
        )

    @staticmethod
    def data_frame_to_html(courses_data_frame: DataFrame) -> HTML:
        """Display a DataFrame as an HTML table

        Args:
            courses_data_frame (DataFrame): The DataFrame of courses

        Returns:
            HTML: The HTML table
        """
        return HTML(
            courses_data_frame.to_html(render_links=True, escape=False, index=False)
        )

    @staticmethod
    def get_course_status(course: dict) -> CourseStatus:
        """Get the status of the course.

        Args:
            course (dict): Dictionary containing the course's details.

        Returns:
            str: The status of the course.
        """
        current_time = time.time()

        if current_time < course["startdate"]:
            return CourseStatus.UPCOMING
        elif course["startdate"] <= current_time <= course["enddate"]:
            return CourseStatus.ACTIVE

        return CourseStatus.PAST_FINISHED

    @staticmethod
    def get_courses_favoured(courses: list) -> list:
        """Get courses that are favoured.

        Args:
            courses (list): List of courses.

        Returns:
            list: List of favoured courses.
        """
        return [course for course in courses if course.get("isfavourite", False)]

    @staticmethod
    def get_courses_by_status(courses: list, status: CourseStatus) -> list:
        """Get courses by status.

        Args:
            courses (list): List of courses.
            status (CourseStatus): The status of the course to filter by.

        Returns:
            list: List of courses with the status.
        """
        return [
            course
            for course in courses
            if MoodleDataUtility.get_course_status(course) == status
        ]

    @staticmethod
    def is_student(enrolled_user: dict) -> bool:
        """Check if the enrolled user is a student.

        Args:
            enrolled_user (dict): Dictionary containing the enrolled user's details.

        Returns:
            bool: True if the user is a student, False otherwise.
        """
        roles = enrolled_user.get(EnrolledUsersFields.ROLES, [])
        if roles:
            role_names = [role[EnrolledUsersFields.ROLE_SHORTNAME] for role in roles]
            return "student" in role_names
        return False

    @staticmethod
    def parse_course_dir(course: dict) -> str:
        """Parse the course name from the course details.

        Args:
            course (dict): Dictionary containing the course's details.

        Returns:
            str: The course name.
        """
        full_name: str = course.get("fullname", "")
        course_id: str = course.get("id", "")
        return f"{MoodleDataUtility.convert_to_slug(full_name)}-id-{course_id}".lower()

    @staticmethod
    def clean_course_name(input_string: str) -> str:
        """Clean the course name, by placing the year at the end of the string.

        Args:
            input_string (str): The input string

        Returns:
            str: The slug
        """
        input_string = html.unescape(input_string).replace("&", "and")
        # Extract year "(23-24)"
        match = re.search(r"\(\d+-\d+\)", input_string)
        if match:
            extracted = match.group(0)
            input_string = input_string.replace(extracted, "").strip()
        else:
            extracted = ""
        return f"{input_string}{extracted}"

    @staticmethod
    def convert_to_slug(input_string: str) -> str:
        """Convert a string to a slug

        Args:
            input_string (str): The input string

        Returns:
            str: The slug
        """
        input_string = html.unescape(input_string).replace("&", "and")
        # Extract year "(23-24)"
        match = re.search(r"\(\d+-\d+\)", input_string)
        if match:
            extracted = match.group(0)
            input_string = input_string.replace(extracted, "").strip()
            extracted = "-year-" + re.sub(r"[^\w\s-]", "", extracted)
        else:
            extracted = ""

        # Remove non-alphanumeric characters except spaces and dashes
        slug = re.sub(r"[^\w\s-]", "", input_string)
        # Replace spaces with '-'
        slug = slug.replace(" ", "-")
        # Replace multiple dashes with one
        slug = re.sub(r"-+", "-", slug)
        # Convert to lowercase
        # slug = slug.lower()

        return f"{slug}{extracted}"

    @staticmethod
    def preprocess_enrolled_users(enrolled_users: list) -> list:
        """Preprocess enrolled users data before saving to CSV.

        Args:
            enrolled_users (list): List of enrolled users' details.

        Returns:
            list: Preprocessed enrolled users data.
        """
        if not enrolled_users:
            return []

        preprocessed_users = []
        for user in enrolled_users:
            if MoodleDataUtility.is_student(user):

                # Remove unwanted fields
                preprocessed_user = {
                    key: value
                    for key, value in user.items()
                    if key not in EnrolledUsersFields.get_unwanted_fields()
                }

                # Set profile image url to blank if it matches the specified value
                profile_image_url = preprocessed_user.get(
                    EnrolledUsersFields.PROFILE_IMAGE_URL
                )
                if profile_image_url.endswith(
                    EnrolledUsersFields.DEFAULT_PROFILE_IMAGE_URL
                ):
                    preprocessed_user[EnrolledUsersFields.PROFILE_IMAGE_URL] = ""

                preprocessed_users.append(preprocessed_user)

        return preprocessed_users

    @staticmethod
    def process_courses(courses_data: dict) -> dict:
        """process courses data.

        Args:
            courses (dict): Courses data.

        Returns:
            dict: Processed courses data.
        """
        if not courses_data:
            return {}

        if "courses" in courses_data:
            for course in courses_data["courses"]:
                if course["courseimage"].startswith("data:image/"):
                    course["courseimage"] = ""

        return courses_data

    @staticmethod
    def process_course_contents_to_file_list(course_contents: list) -> list:  # #NOSONAR
        # function Cognitive Complexity from 22
        """process course contents to a list of files.

        Args:
            course_contents (list): List of course contents.

        Returns:
            list: List of course content files.
        """
        if not course_contents:
            return []

        files = []

        file_number = 0
        for course_content in course_contents:
            if "modules" in course_content:
                for module in course_content["modules"]:
                    if "contents" in module:
                        for content in module["contents"]:
                            if "fileurl" in content:
                                file_number += 1
                                files.append(
                                    {
                                        "filenumber": file_number,
                                        "id": module["id"],
                                        "name": content["filename"],
                                        "url": content["fileurl"],
                                    }
                                )
        return files

    @staticmethod
    def group_courses_by_category(courses_json: dict) -> dict:
        """Group courses by category.

        Args:
            courses_json (dict): Courses data.

        Returns:
            dict: Courses grouped by category.
        """
        courses_by_category = {}

        # Group courses by category
        for course in courses_json:
            course_category = course.get("coursecategory", "")
            if course_category:
                if course_category not in courses_by_category:
                    courses_by_category[course_category] = []
                courses_by_category[course_category].append(course)

        return courses_by_category

    @staticmethod
    def course_filename(number: int, filename: str) -> str:
        """Generate a course filename.

        Args:
            number (int): The course file number
            filename (str): The filename

        Returns:
            str: The generated filename
        """
        return f"{number:02d}-{MoodleDataUtility.cleaned_filename(filename)}"

    @staticmethod
    def cleaned_filename(filename: str) -> str:
        """Generate a clean filename.
        Removes illegal characters and replaces spaces with spaces.
        Collapses multiple whitespaces into one.

        Args:
            filename (str): The filename

        Returns:
            str: The generated filename
        """
        # Define the pattern to match illegal characters
        illegal_chars_pattern = r'[/:*?"<>|\\\0-\x1f\x7f]'

        # Replace illegal characters with an empty string
        cleaned_filename = re.sub(illegal_chars_pattern, " ", filename)

        # Remove leading/trailing whitespaces and collapse multiple whitespaces into one
        cleaned_filename = re.sub(r"\s+", " ", cleaned_filename).strip()

        # Replace spaces with underscores
        cleaned_filename = cleaned_filename.replace(" ", "-").lower()

        return cleaned_filename
