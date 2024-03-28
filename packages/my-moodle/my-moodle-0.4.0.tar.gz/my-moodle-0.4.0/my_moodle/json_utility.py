"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
JSON utility Class
"""

import json


class JsonUtility:
    """JSON Utility functions"""

    @staticmethod
    def load_json_from_file(file_path: str, encoding: str = "utf-8") -> dict:
        """Load JSON from file

        Args:
            file_path (str): The file path

        Returns:
            dict: The JSON data
        """
        with open(file_path, "r", encoding=encoding) as json_file:
            return json.load(json_file)

    @staticmethod
    def save_json_to_file(
        json_dict: dict, file_path: str, indent: int = 2, encoding: str = "utf-8"
    ) -> None:
        """Save

        Args:
            json_dict (dict): _description_
            file_path (str): _description_
        """
        with open(file_path, "w", encoding=encoding) as json_file:
            json_file.write(json.dumps(json_dict, indent=indent))
        print(f"JSON data saved to {file_path}")
