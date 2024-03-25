"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Moodle data downloader Class
"""

from pathlib import Path
import os
import requests

from .api_controller import ApiController
from .course_markdown_builder import CourseMarkdownBuilder
from .csv_utility import CsvUtility
from .enrolled_users_fields import EnrolledUsersFields
from .json_utility import JsonUtility
from .program_markdown_builder import ProgramMarkdownBuilder
from .moodle_data_utility import MoodleDataUtility


class MoodleDataDownloader:
    """Moodle data downloader"""

    def __init__(
        self,
        program_name: str,
        server: str,
        token: str,
        data_dir: str = "data",
        test_data_dir: str = "test-data",
        debug: bool = False,
        timeout: float = 300.0,
        rest_format: str = "json",
    ):
        self.program_name = program_name
        self._api_controller: ApiController = ApiController(
            server, token, rest_format, timeout
        )
        """Test data directory"""
        self._test_data_dir: str = test_data_dir
        self.data_dir = data_dir
        self.debug = debug

    @property
    def api_controller(self) -> ApiController:
        """API controller

        Returns:
            ApiController: The API controller
        """
        return self._api_controller

    @property
    def test_data_dir(self) -> str:
        """Test data directory

        Returns:
            str: The test data directory
        """
        return self._test_data_dir

    def create_directory(self, directory: str) -> str:
        """Create a directory

        Args:
            directory (str): The directory to create

        Returns:
            str: The directory path
        """
        directory_path = Path(self.data_dir, directory)
        os.makedirs(directory_path, exist_ok=True)
        return directory_path.absolute()

    def download_my_data(self):
        """Download my data"""
        courses_json = self.download_courses()

        program_builder = ProgramMarkdownBuilder(self.program_name)
        program_builder.process_courses_json(courses_json)
        program_builder.save_to_file(Path(self.data_dir, "readme.md").absolute())

        self.download_courses_contents(courses_json)

    def download_courses_contents(self, courses: list) -> None:
        """Download courses contents

        Args:
            courses (list): The courses
        """
        for course in courses:
            if course.get("coursecategory") != "N-TUTORR":
                course_id: str = course.get("id", "")
                course_name: str = MoodleDataUtility.clean_course_name(
                    course.get("fullname", "")
                )
                directory_path: str = self.create_directory(
                    MoodleDataUtility.parse_course_dir(course)
                )
                course_url: str = course.get("viewurl", "")

                self.download_enrolled_students(
                    course_id,
                    course_name,
                    Path(directory_path, "enrolled-students.csv").absolute(),
                )
                self.download_course_contents(
                    course_id, directory_path, course_name, course_url
                )

    def download_course_contents(
        self, course_id: str, directory_path: str, course_name: str, course_url: str
    ) -> None:
        """Download all files from a course

        Args:
            course_id (str): The course id
            directory_path (str): The directory path
        """
        course_contents = self.api_controller.get_course_contents(course_id)

        if self.debug:
            os.makedirs(self.test_data_dir, exist_ok=True)

            JsonUtility.save_json_to_file(
                course_contents,
                Path(
                    self.test_data_dir,
                    f"course-{MoodleDataUtility.convert_to_slug(course_name)}-contents.json".lower(),
                ).absolute(),
            )

        course_markdown_builder = CourseMarkdownBuilder(
            self.program_name, course_name, course_url
        )
        course_markdown_builder.process_course_contents(course_contents)

        course_markdown_builder.save_to_file(
            Path(directory_path, "readme.md").absolute()
        )

        files = MoodleDataUtility.process_course_contents_to_file_list(course_contents)

        self.download_files(directory_path, files)

    def download_files(self, directory_path: str, files: list) -> None:
        """Download files to a directory

        Args:
            directory_path (str): The directory path
            files (list): The files
        """
        for file in files:
            message = f'id: {file["id"]}, Filename: {file["name"]} , URL: {file["url"]}'
            print(message)
            file_name: str = MoodleDataUtility.course_filename(
                file["filenumber"], file["name"]
            )
            file_path: Path = Path(directory_path, file_name)
            file_url: str = (
                f"{file['url']}?forcedownload=1&token={self.api_controller.token}"
            )
            self.download_file(
                file_url, file_path.absolute(), self.api_controller.timeout
            )

    @staticmethod
    def download_file(file_url: str, save_path: str, timeout: float) -> None:
        """Download a file from Moodle"""
        try:
            response = requests.get(file_url, stream=True, timeout=timeout)
            response.raise_for_status()

            if response.status_code == 200:
                with open(save_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Saved to: {save_path}")
            else:
                print("Download refused:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Failed to download file:", str(e))
            print()

    def download_courses(self) -> list:
        """Download courses

        Returns:
            list: The courses data
        """
        courses_data: list = self.api_controller.get_enrolled_courses()

        if self.debug:
            os.makedirs(self.test_data_dir, exist_ok=True)
            filename: str = (
                f"program-{MoodleDataUtility.cleaned_filename(self.program_name)}-courses.json"
            )
            JsonUtility.save_json_to_file(
                MoodleDataUtility.process_courses(courses_data),
                Path(self.test_data_dir, filename).absolute(),
            )

        return courses_data["courses"]

    def download_favorite_courses_contents(self) -> None:
        """Download favorite courses

        Returns:
            list: The favorite courses data
        """
        favorite_courses_data: list = MoodleDataUtility.get_courses_favoured(
            self.download_courses()
        )

        self.download_courses_contents(favorite_courses_data)

    def download_enrolled_students(
        self, course_id: str, course_name: str, filename: str
    ) -> None:
        """Download enrolled students

        Args:
            course_id (str): The course id
            filename (str): The filename
        """
        enrolled_users: list = self.api_controller.get_course_enrolled_users(course_id)

        if self.debug:
            os.makedirs(self.test_data_dir, exist_ok=True)

            JsonUtility.save_json_to_file(
                enrolled_users,
                Path(
                    self.test_data_dir, f"enrolled-users-{course_name.lower()}.json"
                ).absolute(),
            )

        enrolled_users: list = MoodleDataUtility.preprocess_enrolled_users(
            enrolled_users
        )
        if enrolled_users:
            CsvUtility.save_json_fields_list_to_csv(
                enrolled_users, EnrolledUsersFields.get_field_order(), filename
            )
            print(f"Enrolled users saved to {filename}")
        else:
            print("No enrolled users found.")
