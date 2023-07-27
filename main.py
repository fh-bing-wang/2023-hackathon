import os
from AzureOpenAIServer import AzureOpenAIServer
from dotenv import load_dotenv
from RedisServer import RedisServer
import argparse

parser = argparse.ArgumentParser(description="Get echo flag")
parser.add_argument('--echo', action='store_true', help='Print results')
args = parser.parse_args()
echo = args.echo

load_dotenv()

redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASSWORD') or ''
redisServer = RedisServer(redis_host, redis_port, redis_password)

openAIServer = AzureOpenAIServer()

patient_id = 'patient_a'

def handle_command(user_input):
    if user_input.lower() == 'exit':
        return

    vector = openAIServer.get_query_embedding(user_input)
    results = redisServer.query_database(vector, f"{patient_id}_docs", 'doc')

    
    if len(results) == 0:
        return openAIServer.get_chat_response(user_input)

    
    medical_history = '\n'.join(results)
    edited_prompt = f"This is the medical history of a patient: {medical_history}.\n According to this history, {user_input}"

    if echo:
        print(f'Editing prompt to:\n {edited_prompt}\n')
    return openAIServer.get_chat_response(edited_prompt)

# Main loop to continuously take user input and provide responses
def main():
    print("You are abstracting data for patient_a! Please enter a question you have:")
    while True:
        user_input = input("Ask something: ")
        response = handle_command(user_input)
        print("Chat Bot:", response)
        if user_input.lower() == 'exit':
            return

if __name__ == '__main__':
    main()
