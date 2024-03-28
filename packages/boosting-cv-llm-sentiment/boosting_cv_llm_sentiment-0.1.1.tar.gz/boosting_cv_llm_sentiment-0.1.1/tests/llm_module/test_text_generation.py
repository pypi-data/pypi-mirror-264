import unittest
from boosting_cv_llm_sentiment.llm_module.text_generation import send_prompt_to_openai

class TestTextGeneration(unittest.TestCase):

    def test_send_prompt_to_openai(self):
        # Llamar a la función con un prompt de prueba
        prompt_text = "tag: enfadado, quiero comprar un coche"
        response = send_prompt_to_openai(prompt_text)

        # Verificar que el resultado no esté vacío
        self.assertIsNotNone(response)

        # Verificar que el resultado sea una cadena de caracteres
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()
