from azure.identity import DefaultAzureCredential
import openai

# Request credential
default_credential = DefaultAzureCredential()
token = default_credential.get_token("https://cognitiveservices.azure.com/.default")

# Setup parameters
openai.api_type = "azure_ad"
openai.api_key = token.token
openai.api_base = "https://flatironhealth-d-hackathon.openai.azure.com/"
openai.api_version = "2023-05-15"

# # create a chat completion
# chat_completion = openai.ChatCompletion.create(
#     engine="gpt-35-turbo", model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}]
# )

# # print the completion
# print(chat_completion.choices[0].message.content)

def get_embedding(text_to_embed):
	model = "text-embedding-ada-002"
	# Embed a line of text
	response = openai.Embedding.create(
		engine=model,
    	model=model,
    	input=[text_to_embed]
	)
	# Extract the AI output embedding as a list of floats
	embedding = response["data"][0]["embedding"]
    
	return embedding
