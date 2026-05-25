# importando o mysql connector pra conectar no banco
import mysql.connector

# imports de tipagem
from typing import Any, Text, Dict, List

# imports do rasa pra criar as actions
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from datetime import date


# funcao que faz a conexao com o banco de dados mysql
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="techrepair"
    )


# acao pra cadastrar o chamado no banco
# o formulario ja pegou os dados: nome, telefone, email, modelo e problema
class ActionCadastrarChamado(Action):

    def name(self) -> Text:
        return "action_cadastrar_chamado"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # pegando os dados que o usuario digitou no chat
        nome = tracker.get_slot("nome")
        telefone = tracker.get_slot("telefone")
        email = tracker.get_slot("email") or "nao informado"
        modelo = tracker.get_slot("modelo")
        problema = tracker.get_slot("problema")

        # conectando no banco
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # vendo se esse cliente ja ta cadastrado pelo telefone
            cursor.execute("SELECT id FROM clientes WHERE telefone = %s", (telefone,))
            cliente = cursor.fetchone()

            if cliente:
                # ja existe, entao pega o id dele
                id_cliente = cliente["id"]
            else:
                # nao existe, entao cadastra um novo
                cursor.execute(
                    "INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)",
                    (nome, telefone, email)
                )
                conn.commit()
                id_cliente = cursor.lastrowid

            # cadastrando o celular do cliente
            cursor.execute(
                "INSERT INTO dispositovos (modelo, marca, id_clientes) VALUES (%s, %s, %s)",
                (modelo, "Não informada", id_cliente)
            )
            conn.commit()
            id_dispositivo = cursor.lastrowid

            # criando a ordem de servico, comeca como 'Aguardando'
            data_hoje = date.today().strftime("%Y-%m-%d")
            cursor.execute(
                "INSERT INTO ordens_servico (descricao_problema, data_abertura, status, id_tecnicos, id_dispositivos) VALUES (%s, %s, %s, %s, %s)",
                (problema, data_hoje, "Aguardando", 1, id_dispositivo)
            )
            conn.commit()
            id_ordem = cursor.lastrowid

            # manda a mensagem de confirmacao pro usuario
            dispatcher.utter_message(
                text=f"✅ Chamado #{id_ordem} aberto com sucesso!\n"
                     f"📱 Aparelho: {modelo}\n"
                     f"🔧 Problema: {problema}\n"
                     f"📋 Status inicial: Aguardando"
            )

        except Exception as e:
            dispatcher.utter_message(text=f"Erro ao cadastrar chamado: {str(e)}")

        # fechando a conexao
        conn.close()

        # limpando os slots pra nao dar problema depois
        return [
            SlotSet("nome", None),
            SlotSet("telefone", None),
            SlotSet("email", None),
            SlotSet("modelo", None),
            SlotSet("problema", None)
        ]


# acao pra consultar o status de um chamado
# o formulario ja pegou o id da ordem ou telefone
class ActionConsultarStatus(Action):

    def name(self) -> Text:
        return "action_consultar_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # pegando o que o usuario informou
        id_ordem = tracker.get_slot("id_ordem")

        # conectando no banco
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # se for numero, busca pelo id da ordem
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
                # se nao for numero, busca pelo telefone
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

        # fechando a conexao
        conn.close()

        return [SlotSet("id_ordem", None)]


# acao pra atualizar o email do cliente
# o formulario ja pegou o telefone e o novo email
class ActionAtualizarEmail(Action):

    def name(self) -> Text:
        return "action_atualizar_email"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # pegando os dados que o usuario informou
        telefone = tracker.get_slot("telefone")
        novo_email = tracker.get_slot("novo_email")

        # conectando no banco
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # procurando o cliente pelo telefone
            cursor.execute("SELECT id, nome FROM clientes WHERE telefone = %s", (telefone,))
            cliente = cursor.fetchone()

            if cliente:
                # achei o cliente, atualiza o email
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

        # fechando a conexao
        conn.close()

        return [
            SlotSet("telefone", None),
            SlotSet("novo_email", None)
        ]
