"""
The EmoBoostLLM module integrates sentiment analysis with conversational AI, enhancing
the interaction through emotional awareness. It employs facial emotion detection to
inform the conversational model of the user's current emotional state, allowing the AI
to generate responses that are not only contextually relevant but also emotionally congruent.

This module defines the EmoBoostLLM class, which serves as the core of the application,
orchestrating the interaction between the sentiment detection mechanism and the OpenAI
conversational model. The sentiment detector utilizes a webcam to analyze the user's facial
expressions in real-time, identifying emotional states that inform the conversational AI's
responses.

The EmoBoostLLM class leverages the OpenAI GPT model for generating text responses. It enhances
these interactions by including emotional context, aiming to create a more empathetic and engaging
user experience. The module utilizes the 'dima806/facial_emotions_image_detection' model from
Hugging Face for emotion classification, which is integrated into the conversation flow to adapt
responses based on detected sentiments.

This module provides a structured approach to building emotionally aware conversational AI systems,
suitable for applications requiring nuanced user engagement. It demonstrates the integration of
computer vision for emotion recognition with advanced natural language processing, showcasing
the potential for creating more responsive and understanding AI agents.

Main Components:
- SentimentDetector: Utilizes computer vision to identify emotional states from the user's facial expressions.
- ConversationManager: Manages the interaction with the OpenAI GPT model, incorporating emotional context into responses.
- EmoBoostLLM: Orchestrates the overall application flow, combining sentiment analysis with conversational AI.

Example Usage:
    >>> from emoboostllm import EmoBoostLLM
    >>> app = EmoBoostLLM(webcam_index=0)
    >>> app.run()

Note: Ensure that a valid OpenAI API key is configured and that webcam access is granted for emotion detection.

Author: Ricard Santiago Raigada García
Date: 27/03/24
"""
import json
import time
import openai
import threading
from boosting_cv_llm_sentiment.config import Config
from boosting_cv_llm_sentiment.llm_module.conversation_manager import ConversationManager
from boosting_cv_llm_sentiment.cv_module.emotion_recognition import SentimentDetector


class EmoBoostLLM:
    """
    EmoBoostLLM integrates a sentiment analysis module with a conversational AI model,
    enhancing the conversation with emotional awareness. It leverages facial emotion detection
    to inform the conversational model about the user's current emotional state, allowing for
    responses that are not only contextually relevant but also emotionally congruent.

    Attributes:
        sentiment_detector (SentimentDetector): An instance of the SentimentDetector class
            to detect emotions from the webcam.
        conv_manager (ConversationManager): Manages conversation interactions with an OpenAI model,
            enriched with emotional context.
        running (bool): A flag to control the main application loop.

    Args:
        webcam_index (int): The device index of the webcam used for emotion detection.
        api_key (str, optional): The API key for OpenAI. If None, it attempts to obtain from Config.

    Methods:
        start: Initializes and starts the necessary components for the application.
        stop: Stops active components and terminates the application.
        run: Executes the main loop of the application, capturing emotional context and generating responses.
    """

    def __init__(self, webcam_index=0, api_key=None):
        """
        Initializes the application with the specified webcam index and OpenAI API key.
        """
        # Si api_key es None, intenta obtenerla de la configuración
        if api_key is None:
            openai.api_key = Config.get_api_key()
        client = openai.OpenAI()
        self.sentiment_detector = SentimentDetector(webcam_index=webcam_index)
        self.conv_manager = ConversationManager(client=client)
        self.running = False

    def start(self):
        """
        Starts the sentiment detector and any other necessary components of the application.
        Sets the running flag to True.
        """
        self.running = True
        self.sentiment_detector.start()
        # Agrega aquí cualquier otro componente que necesite ser iniciado

    def stop(self):
        """
        Stops the sentiment detector and any other active components of the application.
        Sets the running flag to False.
        """
        self.running = False
        self.sentiment_detector.stop()
        # Asegúrate de detener aquí cualquier otro componente que esté
        # corriendo

    def run(self):
        """
        Executes the main loop of the application, capturing user inputs and generating
        emotionally aware responses using the conversational AI model.

        Returns:
            str: A JSON string containing the list of user inputs, assistant responses,
            and timestamps for each interaction.
        """
        self.start()

        responses = []

        try:
            # Initial system message
            self.conv_manager.add_system_message(
                "You are an advanced conversational AI with the ability to understand and empathize with human emotions. You have been programmed to recognize sentiment tags that are extracted from facial detection systems. These tags indicate the emotional state of the user, such as happiness, sadness, anger, or neutrality. Your responses should reflect an understanding of these emotions, adapting your tone and content to provide support, comfort, enthusiasm, or neutrality as appropriate while you respond to the request that the user makes to you. Your goal is to engage in a conversation that is empathetic, emotionally aware, and helpful, making the user feel understood and assisted."
            )

            while self.running:
                user_input = input("You: ")
                if user_input.lower() == "exit":
                    break

                self.sentiment_detector.capture_and_detect_sentiment()
                new_sentiments = self.sentiment_detector.get_new_sentiments()
                prompt_text = "User sentiment: " + \
                    ", ".join([sent[0] for sent in new_sentiments])
                prompt_text = prompt_text + user_input

                self.conv_manager.add_user_message(prompt_text)
                response = self.conv_manager.generate_response()
                print(f"Assistant: {response}")

                # Store the response in the response list
                responses.append({
                    'user_input': user_input,
                    'assistant_response': response,
                    'timestamp': time.time()
                })

        except KeyboardInterrupt:
            print("\nStopping the application at the user's request...")
        finally:
            self.stop()

        return json.dumps(responses, ensure_ascii=False, indent=4)
