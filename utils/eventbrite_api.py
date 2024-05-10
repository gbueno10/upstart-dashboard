import requests
import pandas as pd
from dotenv import load_dotenv


def verificar_usuario(token):
    url = "https://www.eventbriteapi.com/v3/users/me/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Retorna os dados do usuário
    else:
        return response.status_code, response.text  # Retorna código de erro e mensagem

token_privado = 'KA5CJABXFH733E2TDWYI'
usuario = verificar_usuario(token_privado)

#print(usuario)

def obter_id_organizacao(token):
    url = "https://www.eventbriteapi.com/v3/users/me/organizations/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['organizations'][0]['id']
    else:
        return response.status_code, response.text





def obter_numero_de_inscritos(token, evento_id):
    """
    Esta função retorna o número total de inscritos em um evento específico.
    """
    url = f"https://www.eventbriteapi.com/v3/events/{evento_id}/attendees/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    inscritos_total = 0
    has_more_items = True
    while has_more_items:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            inscritos_total += len(data['attendees'])
            pagination = data['pagination']
            if pagination['has_more_items']:
                # Atualizar a URL com o parâmetro de continuação apropriado
                url = f"https://www.eventbriteapi.com/v3/events/{evento_id}/attendees/?continuation={pagination['continuation']}"
            else:
                has_more_items = False
        else:
            return response.status_code, response.text

    return inscritos_total
    
#evento_id = '858229536647'
#numero_de_inscritos = obter_numero_de_inscritos(token_privado, evento_id)
#print(f"Número de inscritos: {numero_de_inscritos}")


def obter_resumo_eventos(token, org_id):
    url = f"https://www.eventbriteapi.com/v3/organizations/{org_id}/events/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        eventos = response.json()['events']
        eventos_simplificados = []
        for evento in eventos:
            evento_id = evento['id']
            inscritos = obter_numero_de_inscritos(token, evento_id)
            capacidade = evento.get('capacity', 0)  # Garante que não haverá erro se 'capacity' estiver ausente
            percentual_ocupacao = (inscritos / capacidade * 100) if capacidade else 0
            evento_simplificado = {
                'Nome': evento['name']['text'],
                'Descrição': evento['description']['text'],
                'URL': evento['url'],
                'Data de Início': evento['start']['local'],
                'Data de Término': evento['end']['local'],
                'Capacidade': capacidade,
                'Inscritos': inscritos,
                'Percentual de Ocupação': f"{percentual_ocupacao:.2f}%",
                'Status': evento['status'],
                'Evento Online': evento['online_event'],
                'Resumo': evento['summary'],
                'ID': evento['id']
            }
            eventos_simplificados.append(evento_simplificado)
        return pd.DataFrame(eventos_simplificados)
    else:
        return response.status_code, response.text
    
#display(obter_resumo_eventos(token_privado, org_id))



def obter_ids_eventos(token, org_id):
    url = f"https://www.eventbriteapi.com/v3/organizations/{org_id}/events/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    eventos_dict = {}
    if response.status_code == 200:
        eventos = response.json()['events']
        for evento in eventos:
            eventos_dict[evento['name']['text']] = evento['id']
        return eventos_dict
    else:
        return response.status_code, response.text


def obter_todos_participantes(token, eventos_dict):
    participantes_totais = []
    for evento_nome, evento_id in eventos_dict.items():
        has_more_items = True
        continuation_token = None  # Token para controle da paginação

        while has_more_items:
            url = f"https://www.eventbriteapi.com/v3/events/{evento_id}/attendees/"
            if continuation_token:
                url += f"?continuation={continuation_token}"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for item in data['attendees']:
                    participante = {
                        'Nome': item['profile']['name'],
                        'Email': item['profile']['email'],
                        'Status do Ingresso': 'Usado' if item['barcodes'][0]['status'] == 'used' else 'Não usado',
                        'Check-in': 'Feito' if item['checked_in'] else 'Pendente',
                        'Classe do Ingresso': item['ticket_class_name'],
                        'Nome do Evento': evento_nome,
                        'ID do Evento': evento_id
                    }
                    participantes_totais.append(participante)
                pagination = data['pagination']
                has_more_items = pagination['has_more_items']
                continuation_token = pagination.get('continuation')  # Atualiza o token de continuação
            else:
                return pd.DataFrame(), f"Erro: {response.status_code}, {response.text}"
    return pd.DataFrame(participantes_totais)

