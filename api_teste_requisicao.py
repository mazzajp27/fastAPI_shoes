import requests
import json

def buscar_tenis():
    url = "http://127.0.0.1:8000/all_shoes"
    
    resposta = requests.get(url)
    print("Status code da requisição:", resposta.status_code)
    return resposta

def avaliacao(resposta):
    if resposta.status_code == 200:
        dados_da_resposta = resposta.json()
        return dados_da_resposta
    else:
        print(f"Erro: Status code {resposta.status_code}")
        return None

def exibir_json(dados): 
    print(json.dumps(dados, indent=4))

def salvar_arquivo(dados):
    with open('meu_arquivo_shoes_oficial.json', 'w') as f:
        json.dump(dados, f, indent=4)
    print("Arquivo JSON criado com sucesso")

if __name__ == '__main__':
    variavel_resposta = buscar_tenis()
    resposta_avaliacao = avaliacao(variavel_resposta)
    
    if resposta_avaliacao:
        exibir_json(resposta_avaliacao)
        salvar_arquivo(resposta_avaliacao)
    else:
        print("Erro ao processar a resposta.")
