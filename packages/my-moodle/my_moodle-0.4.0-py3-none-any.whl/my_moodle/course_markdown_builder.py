"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
CourseMarkdownBuilder Class
"""

import html
from typing import Dict, Optional
from .moodle_data_utility import MoodleDataUtility
from .markdown_document import MarkdownDocument
from .markdown_methods import MarkdownLink


class CourseMarkdownBuilder:
    """Course Markdown Builder"""

    def __init__(self, program_name: str, course_name: str, course_url: str):
        """Initialise the CourseMarkdownBuilder

        Args:
            program_name (str): The program name
            course_name (str): The course name
            course_url (str): The course URL
        """
        self._markdown_document = MarkdownDocument()
        """Markdown document"""

        self._course_name = course_name
        self._course_url = course_url
        self._program_name = program_name

    def __str__(self) -> str:
        """Return the string representation of the CourseMarkdownBuilder

        Returns:
            str: The string representation of the CourseMarkdownBuilder
        """
        return str(self._markdown_document)

    def save_to_file(self, file_path: str, encoding: str = "utf-8") -> None:
        """Saves the markdown document to a file

        Args:
            file_path (str): The file path
        """
        with open(file_path, "w", encoding=encoding) as file:
            file.write(str(self))

    def process_course_contents(self, course_contents: dict) -> None:
        """Process course contents

        Args:
            course_contents (dict): The course contents JSON
        """

        self._markdown_document.write_h1(
            MarkdownLink(self._program_name, "/readme.md", self._program_name)
        )
        self._markdown_document.write_h2(self._course_name)
        self._markdown_document.write_paragraph(f"Course URL: <{self._course_url}>")

        for course_content in course_contents:
            # Write module heading
            module_name = course_content.get("name", "")
            self._markdown_document.write_h3(module_name)

            if course_content.get("visible", 1) == 0:
                self._markdown_document.write_paragraph("*Not available.*")
                continue
            # Process module contents (files)

            modules = course_content.get("modules", [])
            if not modules or len(modules) == 0:
                self._markdown_document.write_paragraph("*No content.*")
            else:
                self.process_modules(modules)
        self._markdown_document.write_hr()

    def process_modules(self, modules: list) -> None:
        """Process modules

        Args:
            modules (_type_): _description_
        """
        course_file_number = 1
        for module in modules:
            mod_name = module.get("modname", "")

            module_contents = module.get("contents", [])

            is_link = len(module_contents) == 0

            module_is_heading = module_contents and len(module_contents) > 1

            if mod_name == "label":
                description: str = module.get("description", "")
                description: str = html.unescape(description)  # Unescape HTML entities
                self._markdown_document.write_line()
                self._markdown_document.write_paragraph(description.strip())
                continue

            content_name = module.get("name", "")
            moodle_content_url = module.get("url", "")

            if module_is_heading:
                if len(module_contents) < 5:
                    self._markdown_document.write_bullet_link_line(
                        f"**{content_name}**"
                    )
                    course_file_number += self.process_module_folder_contents(
                        module_contents, course_file_number
                    )
                else:
                    local_uri = (
                        MoodleDataUtility.course_filename(
                            course_file_number, content_name
                        )
                        + "/"
                    )
                    local_link = MarkdownLink(content_name, local_uri, content_name)
                    moodle_link = MarkdownLink(
                        "moodle", moodle_content_url, content_name
                    )
                    self._markdown_document.write_bullet_link_line(
                        f"{local_link}: original at {moodle_link}"
                    )
                    course_file_number += 1

            else:
                if is_link:
                    moodle_link = MarkdownLink(
                        content_name, moodle_content_url, content_name
                    )
                    self._markdown_document.write_bullet_link_line(moodle_link)
                elif mod_name == "url":
                    url = self.get_local_uri(course_file_number, module_contents)

                    moodle_link = MarkdownLink(content_name, url, content_name)
                    self._markdown_document.write_bullet_link_line(moodle_link)
                else:
                    local_uri = self.get_local_uri(course_file_number, module_contents)
                    local_link = MarkdownLink(content_name, local_uri, content_name)
                    moodle_link = MarkdownLink(
                        "moodle", moodle_content_url, content_name
                    )
                    self._markdown_document.write_bullet_link_line(
                        f"{local_link}: original at {moodle_link}"
                    )
                    course_file_number += 1
            self._markdown_document.write_line()

    def process_module_folder_contents(
        self, module_contents: list, course_file_number: int
    ) -> int:
        """_summary_

        Args:
            module_contents (list): _description_
            course_file_number (int): _description_

        Returns:
            int: The number of files processed
        """
        for module_content in module_contents:
            moodle_file = MoodleFile(module_content)
            moodle_content_url = moodle_file.file_url
            content_name = moodle_file.file_name
            if moodle_file.is_file() and "fileurl" in module_content:
                local_uri = MoodleDataUtility.course_filename(
                    course_file_number, moodle_file.file_name
                )
                local_link = MarkdownLink(content_name, local_uri, content_name)
                moodle_link = MarkdownLink("moodle", moodle_content_url, content_name)
                self._markdown_document.write_bullet_link_line(
                    f"{local_link}: original at {moodle_link}", 1
                )
                course_file_number += 1
            elif moodle_file.is_url():
                moodle_link = MarkdownLink("moodle", moodle_content_url, content_name)
                self._markdown_document.write_bullet_link_line(
                    f"{local_link}: original at {moodle_link}"
                )
                moodle_link = MarkdownLink(
                        content_name, moodle_content_url, content_name
                    )
                self._markdown_document.write_bullet_link_line(moodle_link, 1)
        return course_file_number

    def get_local_uri(self, course_file_number: int, module_contents: list) -> str:
        """Get the local URI

        Args:
            course_file_number (int): The course file number
            module_contents (list): The module contents

        Returns:
            str: The local URI
        """
        local_uri = ""
        for module_content in module_contents:
            moodle_file = MoodleFile(module_content)
            if moodle_file.is_file() and "fileurl" in module_content:
                local_uri = MoodleDataUtility.course_filename(
                    course_file_number, moodle_file.file_name
                )
            elif moodle_file.is_url():
                local_uri = module_content["fileurl"]
        return local_uri


class MoodleFile:
    """MoodleFile represents a file in Moodle."""

    def __init__(self, json_data: Dict[str, any]):
        """
        Initializes a MoodleFile object with the given JSON data.

        Args:
            json_data (dict): The JSON data representing the Moodle file.
        """
        self.json_data = json_data

    @property
    def type(self) -> str:
        """
        Returns the type of the Moodle file.

        Returns:
            str: The filename.
        """
        return self.json_data["type"]

    @property
    def file_name(self) -> str:
        """
        Returns the filename of the Moodle file.

        Returns:
            str: The filename.
        """
        return self.json_data["filename"]

    @property
    def file_path(self) -> str:
        """
        Returns the filepath of the Moodle file.

        Returns:
            str: The filepath.
        """
        return self.json_data["filepath"]

    @property
    def file_size(self) -> int:
        """
        Returns the filesize of the Moodle file.

        Returns:
            int: The filesize.
        """
        return self.json_data["filesize"]

    @property
    def file_url(self) -> str:
        """
        Returns the file URL of the Moodle file.

        Returns:
            str: The file URL.
        """
        return self.json_data["fileurl"]

    @property
    def time_created(self) -> int:
        """
        Returns the time created of the Moodle file.

        Returns:
            int: The time created.
        """
        return self.json_data["timecreated"]

    @property
    def time_modified(self) -> int:
        """
        Returns the time modified of the Moodle file.

        Returns:
            int: The time modified.
        """
        return self.json_data["timemodified"]

    @property
    def mime_type(self) -> str:
        """
        Returns the mimetype of the Moodle file.

        Returns:
            str: The mimetype.
        """
        return self.json_data["mimetype"]

    @property
    def is_external_file(self) -> bool:
        """
        Returns whether the file is external or not.

        Returns:
            bool: True if the file is external, False otherwise.
        """
        return self.json_data["isexternalfile"]

    @property
    def author(self) -> Optional[str]:
        """
        Returns the author of the Moodle file if available.

        Returns:
            Optional[str]: The author or None if not available.
        """
        return self.json_data.get("author")

    @property
    def license(self) -> Optional[str]:
        """
        Returns the license of the Moodle file if available.

        Returns:
            Optional[str]: The license or None if not available.
        """
        return self.json_data.get("license")

    def is_file(self) -> bool:
        """Is the Moodle file a file?

        Returns:
            bool: True if the Moodle file is a file, False otherwise.
        """
        return self.type == "file"

    def is_url(self) -> bool:
        """Is the Moodle file a URL?

        Returns:
            bool: True if the Moodle file is a URL, False otherwise.
        """
        return self.type == "url"

    def create_local_filename(self) -> str:
        """Create a local filename

        Returns:
            str: The local filename
        """
        return self.file_name
