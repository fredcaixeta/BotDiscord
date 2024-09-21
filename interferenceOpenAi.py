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
        "model": "gpt-4",  # Ajuste conforme a sua necessidade
        "messages": formatted_questions,
        "temperature": 0.7  # Ajuste a criatividade da resposta, se necessário
    }

    # Envio da requisição para a API
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

    # Verifica se a resposta é válida
    if response.status_code == 200:
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    else:
        return {"error": response.status_code, "message": response.text}

# Exemplo de uso com loop de interação
if __name__ == "__main__":
    system_message = (
        "Você é um banqueiro medieval de RPG amigável. O personagem que fala com você é um nórdico, "
        "que não tem uma conta no banco. Você retornará uma resposta em um formato list com duas informações - "
        "a primeira é a resposta ao personagem, a segunda é a resposta ao código (True caso ele tenha se registrado, False caso contrário). "
        "Você quer que ele se registre. Se ele desejar se registrar, apenas fale que ele acaba de ser registrado. "
        "Responda o personagem com um máximo de 50 caracteres."
    )

    # Inicializa o array de perguntas e respostas
    questions = []

    while True:
        # Input do usuário
        user_input = input("Você (digite 'sair' para encerrar): ")
        
        if user_input.lower() == "sair":
            print("Encerrando conversa...")
            break

        # Adiciona a fala do usuário na lista de perguntas
        questions.append({"user": user_input})

        # Envia a conversa para o modelo da OpenAI e obtém a resposta
        response = OpenAICompletion(system_message, questions)

        # Adiciona a resposta do NPC às perguntas
        questions.append({"assistant": response})
        
        for question in questions:
            print(question)