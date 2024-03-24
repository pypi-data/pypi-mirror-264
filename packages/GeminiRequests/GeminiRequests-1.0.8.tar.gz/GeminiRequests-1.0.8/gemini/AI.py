import os

import requests


def pick(filename, data):
    import pickle
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def unpick(filename):
    import pickle
    with open(filename, 'rb') as f:
        return pickle.load(f)


class GenerativeAI:
    def __init__(self, gemini_api_key: str = None, model: str = "gemini-pro", history_file: str = None):
        """
        Initialize the GenerativeAI class.

        Parameters:
            gemini_api_key (str): The Gemini API key. Default is None.
            model (str): The model to use. Default is "gemini-pro".
            history_file (str): The file to store history. Default is None.
        """
        self.api_key = gemini_api_key
        self.model = model

        if gemini_api_key is None:
            raise Exception("""
################################################
Gemini API key is required.
Please set your gemini api key 
ai = GenerativeAI(gemini_api_key="YOUR_API_KEY")""")

        self.url = self.source_url()

        # Headers for the request
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.history_file = history_file

        if self.history_file is not None:
            try:
                open(self.history_file, "r")
            except FileNotFoundError:
                pick(self.history_file, [])
            self.history = unpick(self.history_file)
        else:
            self.history = []

    def source_url(self) -> str:
        """
        Returns the URL for generating content using the specified model and API key.

        :return: A string representing the URL for generating content.
        """
        return f'https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}'

    def update_history(self, data_list=None, history_file=None) -> None:
        """
        Updates the history data either from a provided list or a history file.

        :param data_list: List of data to update the history with (default is None).
        :param history_file: Name of the history file to update the history from (default is None).
        """
        if data_list:
            self.history = data_list
        elif history_file:
            filename = history_file
            if "data" not in os.listdir():
                os.mkdir("data")
            if filename not in os.listdir("data"):
                filename = f"data/{filename}"
                pick(filename, [])
            self.history = unpick(filename)
        else:
            self.history = [""]

    def clear_history(self) -> None:
        """
        Clears the history list by assigning an empty list to the 'history' attribute.
        """
        self.history = []

    def generate_text(self, text: str) -> str:
        """
        Generates text based on the given input text.

        Parameters:
            text (str): The input text to generate from.

        Returns:
            str: The generated text.
        """
        self.update_history(self.history + [{"role": "user", "parts": [{"text": text}]}])

        data = {
            "contents": self.history,
        }
        response = requests.post(self.url, json=data, headers=self.headers)

        result = response.json()['candidates'][0]['content']['parts'][0]['text']
        self.update_history(self.history + [{"role": "assistant", "parts": [{"text": result}]}])

        return result



