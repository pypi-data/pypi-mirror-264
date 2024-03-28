"""
This module contains the configuration class for the Boosting CV-LLM Sentiment package.

Used to manage application settings, including obtaining
the API key needed to interact with the OpenAI API.

Configurations can be set using environment variables.

Author: Ricard Santiago Raigada García
Date: 27/03/2024
"""

import os


class Config:
    """
    The Config class manages the configuration of the application.

    Attributes:
        OPENAI_API_KEY (str): API key for the OpenAI API obtained from the environment variable.

    Methods:
        get_api_key: Returns the API key if available, otherwise throws an error.
    """

    @staticmethod
    def get_api_key():
        """
        Gets the OpenAI API key from an environment variable.

        Returns:
            str: The OpenAI API key.

        Lance:
            ValueError: If the API key is not set in the environment variable.
        """
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key is None:
            raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY\
                environment variable.")
        return openai_api_key
