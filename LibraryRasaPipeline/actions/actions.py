import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionBuscarLivroTitulo(Action):
    def name(self) -> Text:
        return "action_buscar_livro_titulo"

    def run(self, dispatcher, tracker, domain):
        titulo = tracker.get_slot("titulo_livro")
        if not titulo:
            dispatcher.utter_message(text="Qual o título do livro que você procura?")
            return []

        url = f"https://openlibrary.org/search.json?title={titulo}"
        response = requests.get(url)
        data = response.json()

        if data["docs"]:
            livro = data["docs"][0]
            nome = livro.get("title", "Título não encontrado")
            autor = ", ".join(livro.get("author_name", ["Autor desconhecido"]))
            ano = livro.get("first_publish_year", "Ano desconhecido")
            dispatcher.utter_message(text=f"Encontrei esse livro pra você:\n📚 *{nome}*\n✍️ Autor: {autor}\n📅 Ano: {ano}")
        else:
            dispatcher.utter_message(text=f"Não encontrei nenhum livro com o título *{titulo}*. Você quer tentar outro?")
        return []



class ActionBuscarLivroAutor(Action):
    def name(self) -> Text:
        return "action_buscar_livro_autor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        autor = tracker.get_slot("nome_autor")
        if not autor:
            dispatcher.utter_message(text="Desculpe, não entendi o nome do autor.")
            return []

        url = f"http://openlibrary.org/search.json?author={autor}"
        response = requests.get(url)
        data = response.json()

        if data['num_found'] > 0:
            book = data['docs'][0]
            mensagem = f"Um dos livros encontrados de *{autor}*:\n📚 *{book.get('title')}*"
            if 'first_publish_year' in book:
                mensagem += f"\n📅 Ano de publicação: {book['first_publish_year']}"
            dispatcher.utter_message(text=mensagem)
        else:
            dispatcher.utter_message(text=f"Não encontrei livros do autor {autor}.")

        return []


class ActionBuscarLivroAssunto(Action):
    def name(self) -> Text:
        return "action_buscar_livro_assunto"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        assunto = tracker.get_slot("assunto_livro")
        if not assunto:
            dispatcher.utter_message(text="Desculpe, não entendi o assunto que você quer.")
            return []

        url = f"http://openlibrary.org/search.json?subject={assunto}"
        response = requests.get(url)
        data = response.json()

        if data['num_found'] > 0:
            book = data['docs'][0]
            mensagem = f"Um livro sobre *{assunto}*:\n📚 *{book.get('title')}*"
            if 'author_name' in book:
                mensagem += f"\n✍️ Autor: {', '.join(book['author_name'])}"
            dispatcher.utter_message(text=mensagem)
        else:
            dispatcher.utter_message(text=f"Não encontrei livros sobre {assunto}.")

        return []


class ActionBuscarLivroIsbn(Action):
    def name(self) -> Text:
        return "action_buscar_livro_isbn"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        isbn = tracker.get_slot("isbn")
        if not isbn:
            dispatcher.utter_message(text="Desculpe, não entendi o ISBN informado.")
            return []

        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        response = requests.get(url)
        data = response.json()

        book_key = f"ISBN:{isbn}"
        if book_key in data:
            book = data[book_key]
            mensagem = f"📚 *{book.get('title', 'Título não encontrado')}*"
            if 'authors' in book:
                autores = ", ".join([a['name'] for a in book['authors']])
                mensagem += f"\n✍️ Autor: {autores}"
            if 'publish_date' in book:
                mensagem += f"\n📅 Publicado em: {book['publish_date']}"
            dispatcher.utter_message(text=mensagem)
        else:
            dispatcher.utter_message(text=f"Não encontrei nenhum livro com o ISBN {isbn}.")

        return []
