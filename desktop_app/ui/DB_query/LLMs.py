import openai
import logging
from octoai.client import OctoAI
from octoai.text_gen import ChatMessage
from openai import OpenAI


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class OCTOAI_LLM_Chatbot():
    def __init__(self, model_name, api_key):
        self.api_key = api_key
        self.model_name = model_name
        self.conversation_history = []

    def chat_completion(self, prompt, question):
        client = OctoAI(api_key=self.api_key)

        self.conversation_history.append({"role": "user", "content": question})

        # Construct messages correctly
        messages = [
            ChatMessage(role="system", content=prompt), 
        ChatMessage(role="user", content=question) ]

        try:
            chat_completion = client.text_gen.create_chat_completion(
                model=self.model_name,
                messages=messages,
                temperature=0.2,
                max_tokens=150
            )

            response = chat_completion.choices[0].message.content
            logger.debug(f"API Response: {response}")

            self.conversation_history.append({"role": "assistant", "content": response})

            return response
        except Exception as e:
            logger.error(f"Error during chat completion: {e}")
            return f"An error occurred while processing your request: {e}"

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    
class langdock_LLM_Chatbot():
    def __init__(self, model_name, api_key, base_url, context):
        self.api_key = api_key
        self.model_name = model_name
        self.conversation_history = []
        self.base_url = base_url
        self.context = context

    def chat_completion(self, context, question):
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)


        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ]

        self.conversation_history.append({"role": "user", "content": question})

        try:
            completion = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )

            response = completion.choices[0].message.content
            logger.debug(f"API Response: {response}")

            self.conversation_history.append({"role": "assistant", "content": response})

            return response
        except Exception as e:
            logger.error(f"Error during chat completion: {e}")
            return f"An error occurred while processing your request: {e}"

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    