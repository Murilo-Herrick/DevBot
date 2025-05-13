from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionFornecerSuporte(Action):
    def name(self) -> str:
        return "action_fornecer_suporte"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain) -> list:
        problema = tracker.get_slot("problema")
        
        if problema == "acesso":
            dispatcher.utter_message(text="Parece que você está tendo problemas para acessar sua conta. Vamos tentar uma solução. Tente redefinir sua senha no link abaixo: [Link para redefinir senha].")
        elif problema == "plano":
            dispatcher.utter_message(text="Se deseja mudar seu plano, temos algumas opções disponíveis. Você pode conferir os planos [aqui](link para os planos).")
        elif problema == "aplicativo":
            dispatcher.utter_message(text="Lamento saber que o aplicativo não está funcionando. Tente fechar e reabrir o aplicativo. Se o problema persistir, acesse o nosso artigo de ajuda [link para ajuda].")
        else:
            dispatcher.utter_message(text="Parece que seu problema é um pouco mais complexo. Vou encaminhá-lo para um atendente humano para que ele possa ajudar melhor. Um momento, por favor...")

        return []
