import requests 
from typing import Any, Text, Dict, List 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionInformaClima(Action):
    def name(self) -> Text:
        return "action_informa_clima"
    
    def run (self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        city = tracker.get_slot("city")

        weather_data = self.get_weather(city)

        print(f"City: {city}")
        print(f"Weather Data: {weather_data}")

        if weather_data:
            response = f"O clima na cidade de {city} está em: {weather_data['current']['temp_c']} °C"
        else:
            response = f"Me desculpe, mas não consegui obter a situação do clima da diade de{city}"
        
        dispatcher.utter_message(text=response)
        return []

    def get_weather(self, city: str) -> Dict[Text, Any]:
        api_key = "3ff3169e46ac47a3a44233514252503"
        base_url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "q": city,
            "aqi": "no",
            "key": api_key
        }

        try:
            print(f"API Resquest URL: {base_url}?{params}")
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            api_response = response.json()
            print(f"API Response: {api_response}")
            return api_response
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return None