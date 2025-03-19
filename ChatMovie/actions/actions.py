from typing import Any, Text, Dict, List
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker

class ActionRecomendarFilme(Action):
    def name(self) -> Text:
        return "action_recomendar_filme"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Obtém o gênero do slot e normaliza o texto
        genero = tracker.get_slot("genero")
        genero = genero.lower().strip() if genero else ""
        
        if not genero:  # Caso o gênero não tenha sido especificado
            dispatcher.utter_message(text="Parece que você não mencionou um gênero. Por favor, me diga qual gênero de filme você prefere. Ex: Comédia, Ação, Drama...")
            return []

        # Chama a função para obter recomendações de filmes
        filmes = self.obter_recomendacoes(genero)

        # Verifica se há filmes para o gênero fornecido
        if filmes:
            dispatcher.utter_message(text=f"Para o gênero {genero}, recomendo: {', '.join(filmes)}")
        else:
            # Se o gênero não for encontrado, mostra mensagem com gêneros válidos
            dispatcher.utter_message(
                text=f"Desculpe, não encontrei recomendações para '{genero}'. Por favor, escolha entre: Comédia, Ação, Drama, Suspense, Romance, Ficção Científica, Terror, Aventura, Mistério, Fantasia, Documentário, Biografia, Musical."
            )
        
        return []
    
    def obter_recomendacoes(self, genero: Text) -> List[Text]:
        filmes_por_genero = {
            "comédia": ["O Máskara", "Ace Ventura", "Os Incríveis"],
            "ação": ["Vingadores: Ultimato", "John Wick", "Mad Max: Estrada da Fúria"],
            "drama": ["À Procura da Felicidade", "Forrest Gump", "O Pianista"],
            "suspense": ["O Sexto Sentido", "Garota Exemplar", "Corra!"],
            "romance": ["Diário de uma Paixão", "Como Se Fosse a Primeira Vez", "Orgulho e Preconceito"],
            "ficção científica": ["Blade Runner 2049", "Matrix", "Interstellar"],
            "terror": ["O Exorcista", "O Iluminado", "A Bruxa"],
            "aventura": ["Indiana Jones", "Piratas do Caribe", "Jurassic Park"],
            "mistério": ["Sherlock Holmes", "O Código Da Vinci", "Os Suspeitos"],
            "fantasia": ["Harry Potter", "Senhor dos Anéis", "As Crônicas de Nárnia"],
            "documentário": ["Won't You Be My Neighbor?", "13th", "Free Solo"],
            "biografia": ["A Teoria de Tudo", "O Jogo da Imitação", "Steve Jobs"],
            "musical": ["La La Land", "O Rei do Show", "Os Miseráveis"]
        }
        return filmes_por_genero.get(genero, [])

    def obter_generos_disponiveis(self) -> List[Text]:
        return ["comédia", "ação", "drama", "suspense", "romance", "ficção científica", "terror", 
                "aventura", "mistério", "fantasia", "documentário", "biografia", "musical"]
