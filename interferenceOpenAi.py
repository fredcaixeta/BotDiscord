import os
import requests
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função para criar uma conclusão usando a API da OpenAI
def OpenAICompletion(system_message, questions):
    # Lista para armazenar as mensagens formatadas
    formatted_questions = [
        {
            "role": "system",
            "content": system_message
        }
    ]

    # Verifica e formata as perguntas
    for question in questions:
        if not isinstance(question, dict) or ('assistant' not in question and 'user' not in question):
            return {"error": "Each question must be a dict containing the keys 'assistant' or 'user'"}
        
        if 'assistant' in question:
            formatted_questions.append({
                "role": "assistant",
                "content": question['assistant']
            })
        
        if 'user' in question:
            formatted_questions.append({
                "role": "user",
                "content": question['user']
            })

    # Configuração da API
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"  # Use a chave da API do ambiente
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": formatted_questions
    }

    # Envio da requisição para a API
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

    # Verifica se a resposta é válida
    if response.status_code == 200:
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    else:
        return {"error": response.status_code, "message": response.text}

# Exemplo de uso
if __name__ == "__main__":
    system_message = "Você é um assistente amigável."
    questions = "Como vai assistente?"
    questions = [
        {"user": questions}
    ]

    response = OpenAICompletion(system_message, questions)
    print(response)
