"""
This module provides the SentimentDetector class, which leverages a pre-trained model from Hugging Face
for detecting facial emotions in images captured via webcam. The detected emotions are intended to enhance
the interaction within conversational AI systems by providing sentiment context.

The class uses the 'dima806/facial_emotions_image_detection' model through the Transformers library's
image classification pipeline. It continuously captures webcam images, predicts emotional states, and
manages a sentiment history for dynamic interaction adjustments based on the user's emotional cues.

Note: Use of this model in commercial applications must comply with the terms of the Apache-2.0 license
and you should consider Hugging Face's policies on using pre-trained models.

Usage of this model in commercial applications must adhere to the Apache-2.0 license terms, and users
should consider the policies of Hugging Face regarding pre-trained model usage.

Model license: Apache-2.0. Please see the model page on Hugging Face
For more details on licensing and proper use:
https://huggingface.co/dima806/facial_emotions_image_detection

Author: Ricard Santiago Raigada García
Date: 27/03/24
"""
import cv2
from datetime import datetime
from transformers import pipeline
from PIL import Image
import numpy as np
import threading
import time


class SentimentDetector:
    """
    Detects facial emotions from webcam images using a pre-trained Hugging Face model.

    Attributes:
        webcam_index (int): Index of the webcam device to use for image capture.
        sentiments (list): A list to store detected sentiments and their corresponding timestamps.
        last_interaction (float): Timestamp of the last interaction, used to filter new sentiments.
        pipe (transformers.Pipeline): The Transformers pipeline configured for image classification.
        running (bool): Flag to control the continuous detection loop.

    Args:
        webcam_index (int): The device index of the webcam. Defaults to 0.
        device (int): The device index to use for processing. Defaults to 0 (useful for specifying GPU).

    Methods:
        capture_image: Captures an image from the webcam and converts it to RGB format.
        start: Initiates the continuous detection loop in a separate thread.
        stop: Stops the detection loop and joins the thread.
        capture_and_detect_loop: Continuously captures images and detects sentiments.
        capture_and_detect_sentiment: Captures an image and uses the model to detect sentiment.
        get_new_sentiments: Retrieves sentiments detected since the last interaction.
    """

    def __init__(self, webcam_index=0, device=0):
        """
        Initializes the SentimentDetector with a specific webcam and processing device.
        """
        self.webcam_index = webcam_index
        self.sentiments = []
        self.last_interaction = time.time()
        self.pipe = pipeline("image-classification",
                             model="dima806/facial_emotions_image_detection")
        self.running = False

    def capture_image(self):
        """
        Captures a single frame from the webcam and converts it from BGR to RGB format.

        Returns:
            numpy.ndarray: The captured image frame in RGB format, or None if capture failed.
        """
        cap = cv2.VideoCapture(self.webcam_index)

        ret, frame = cap.read()
        cap.release()
        if ret:
            # Convert the frame from BGR (OpenCV) to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame_rgb
        else:
            return None

    def start(self):
        """
        Starts the continuous emotion detection loop in a background thread.
        """
        self.running = True
        self.thread = threading.Thread(target=self.capture_and_detect_loop)
        self.thread.start()

    def stop(self):
        """
        Stops the continuous emotion detection loop and waits for the thread to finish.
        """
        self.running = False
        self.thread.join()

    def capture_and_detect_loop(self):
        """
        The main loop for continuous image capture and emotion detection.
        """
        while self.running:
            self.capture_and_detect_sentiment()
            time.sleep(0.5)

    def capture_and_detect_sentiment(self):
        """
        Captures an image from the webcam, detects the predominant emotional sentiment,
        and adds it to the sentiments history with a timestamp.
        """
        frame = self.capture_image()
        if frame is not None:
            # Convert the RGB frame to a PIL image object
            image = Image.fromarray(frame)
            # image.save("temp_image_check.jpg")

            try:
                # To the pipeline
                results = self.pipe(image)

                # The most likely outcome
                if results:
                    top_result = results[0]
                    detected_sentiment = top_result["label"]
                    # print(f"Detected Sentiment: {detected_sentiment}")  #
                    # Para depuración

                    # Add the detected sentiment and current timestamp to the
                    # list
                    self.sentiments.append((detected_sentiment, time.time()))

            except Exception as e:
                print(f"Error detecting sentiment: {e}")

    def get_new_sentiments(self):
        """
        Retrieves new sentiments detected since the last interaction.

        Returns:
            list: A list of new sentiments and their timestamps since the last interaction.
        """
        new_sentiments = [
            sent for sent in self.sentiments if sent[1] > self.last_interaction]
        self.last_interaction = time.time()
        self.sentiments = []  # Clear the list after getting the new feelings back
        return new_sentiments
