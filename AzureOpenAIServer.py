from azure.identity import DefaultAzureCredential
import openai

class AzureOpenAIServer():
    def __init__(self):
        # Request credential
        default_credential = DefaultAzureCredential()
        token = default_credential.get_token("https://cognitiveservices.azure.com/.default")

        # Setup parameters
        openai.api_type = "azure_ad"
        openai.api_key = token.token
        openai.api_base = "https://flatironhealth-d-hackathon.openai.azure.com/"
        openai.api_version = "2023-05-15"

    def get_embedding(self, texts_to_embed):
        model = "text-embedding-ada-002"
        # Embed a line of text
        response = openai.Embedding.create(
            engine=model,
            model=model,
            input=texts_to_embed
        )
        # Extract the AI output embedding as a list of floats
        embeddings = response["data"]
        
        return embeddings