# Importa o conector do MySQL
import mysql.connector

# Importa tipos para anotação
from typing import Any, Text, Dict, List

# Importa classes base do Rasa SDK
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from datetime import date


# -------------------------------------------------------
# Função auxiliar para conectar ao banco de dados
# -------------------------------------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="techrepair"
    )


# -------------------------------------------------------
# Ação 1: Cadastrar Chamado (INSERT)
# O formulário chamado_form já coletou: nome, telefone, modelo, problema
# -------------------------------------------------------
class ActionCadastrarChamado(Action):

    def name(self) -> Text:
        return "action_cadastrar_chamado"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Pega os valores dos slots já preenchidos pelo formulário
        nome = tracker.get_slot("nome")
        telefone = tracker.get_slot("telefone")
        modelo = tracker.get_slot("modelo")
        problema = tracker.get_slot("problema")

        # Abre a conexão com o banco
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Verifica se o cliente já existe pelo telefone
            cursor.execute("SELECT id FROM clientes WHERE telefone = %s", (telefone,))
            cliente = cursor.fetchone()

            if cliente:
                # Se já existe, usa o id dele
                id_cliente = cliente["id"]
            else:
                # Se não existe, cadastra o cliente
                cursor.execute(
                    "INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)",
                    (nome, telefone, "nao informado")
                )
                conn.commit()
                id_cliente = cursor.lastrowid

            # Cadastra o dispositivo
            cursor.execute(
                "INSERT INTO dispositovos (modelo, marca, id_clientes) VALUES (%s, %s, %s)",
                (modelo, "Não informada", id_cliente)
            )
            conn.commit()
            id_dispositivo = cursor.lastrowid

            # Cria a ordem de serviço com status 'Aguardando'
            data_hoje = date.today().strftime("%Y-%m-%d")
            cursor.execute(
                "INSERT INTO ordens_servico (descricao_problema, data_abertura, status, id_tecnicos, id_dispositivos) VALUES (%s, %s, %s, %s, %s)",
                (problema, data_hoje, "Aguardando", 1, id_dispositivo)
            )
            conn.commit()
            id_ordem = cursor.lastrowid

            # Envia confirmação ao usuário
            dispatcher.utter_message(
                text=f"✅ Chamado #{id_ordem} aberto com sucesso!\n"
                     f"📱 Aparelho: {modelo}\n"
                     f"🔧 Problema: {problema}\n"
                     f"📋 Status inicial: Aguardando"
            )

        except Exception as e:
            dispatcher.utter_message(text=f"Erro ao cadastrar chamado: {str(e)}")

        # Fecha a conexão
        conn.close()

        # Limpa os slots depois de usar
        return [
            SlotSet("nome", None),
            SlotSet("telefone", None),
            SlotSet("modelo", None),
            SlotSet("problema", None)
        ]


# -------------------------------------------------------
# Ação 2: Consultar Status (SELECT)
# O formulário consulta_form já coletou: id_ordem
# -------------------------------------------------------
class ActionConsultarStatus(Action):

    def name(self) -> Text:
        return "action_consultar_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Pega o valor do slot preenchido pelo formulário
        id_ordem = tracker.get_slot("id_ordem")

        # Abre a conexão com o banco
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Tenta buscar como ID numérico primeiro
            if id_ordem.isdigit():
                query = """
                    SELECT os.id, os.descricao_problema, os.status, os.data_abertura,
                           d.modelo, c.nome
                    FROM ordens_servico os
                    JOIN dispositovos d ON os.id_dispositivos = d.id
                    JOIN clientes c ON d.id_clientes = c.id
                    WHERE os.id = %s
                """
                cursor.execute(query, (int(id_ordem),))
            else:
                # Se não é número, busca pelo telefone do cliente
                query = """
                    SELECT os.id, os.descricao_problema, os.status, os.data_abertura,
                           d.modelo, c.nome
                    FROM ordens_servico os
                    JOIN dispositovos d ON os.id_dispositivos = d.id
                    JOIN clientes c ON d.id_clientes = c.id
                    WHERE c.telefone = %s
                    ORDER BY os.id DESC
                    LIMIT 1
                """
                cursor.execute(query, (id_ordem,))

            resultado = cursor.fetchone()

            if resultado:
                dispatcher.utter_message(
                    text=f"📋 Ordem #{resultado['id']}\n"
                         f"👤 Cliente: {resultado['nome']}\n"
                         f"📱 Aparelho: {resultado['modelo']}\n"
                         f"🔧 Problema: {resultado['descricao_problema']}\n"
                         f"📅 Abertura: {resultado['data_abertura']}\n"
                         f"📌 Status: {resultado['status']}"
                )
            else:
                dispatcher.utter_message(
                    text="Nenhuma ordem encontrada com este ID. Verifique o número e tente novamente."
                )

        except Exception as e:
            dispatcher.utter_message(text=f"Erro ao consultar: {str(e)}")

        # Fecha a conexão
        conn.close()

        return [SlotSet("id_ordem", None)]


# -------------------------------------------------------
# Ação 3: Atualizar Email (UPDATE)
# O formulário email_form já coletou: telefone, novo_email
# -------------------------------------------------------
class ActionAtualizarEmail(Action):

    def name(self) -> Text:
        return "action_atualizar_email"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Pega os valores dos slots preenchidos pelo formulário
        telefone = tracker.get_slot("telefone")
        novo_email = tracker.get_slot("novo_email")

        # Abre a conexão com o banco
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Verifica se o cliente existe
            cursor.execute("SELECT id, nome FROM clientes WHERE telefone = %s", (telefone,))
            cliente = cursor.fetchone()

            if cliente:
                # Atualiza o email
                cursor.execute(
                    "UPDATE clientes SET email = %s WHERE telefone = %s",
                    (novo_email, telefone)
                )
                conn.commit()

                dispatcher.utter_message(
                    text=f"✅ E-mail atualizado com sucesso!\n"
                         f"👤 Cliente: {cliente['nome']}\n"
                         f"📧 Novo e-mail: {novo_email}"
                )
            else:
                dispatcher.utter_message(
                    text="Não encontrei nenhum cliente com esse telefone. Verifique e tente novamente."
                )

        except Exception as e:
            dispatcher.utter_message(text=f"Erro ao atualizar: {str(e)}")

        # Fecha a conexão
        conn.close()

        return [
            SlotSet("telefone", None),
            SlotSet("novo_email", None)
        ]
