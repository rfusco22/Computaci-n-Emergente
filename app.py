from flask import Flask, render_template, request, jsonify
import json
import random
import string
import nltk
from nltk.stem import SnowballStemmer
import os

# Descargar recursos necesarios de NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

app = Flask(__name__)

class TouristChatbot:
    def __init__(self):
        self.stemmer = SnowballStemmer('spanish')
        self.load_intents()
        
    def load_intents(self):
        """Cargar intents desde el archivo JSON"""
        try:
            with open('data/intents.json', 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {
                "intents": [
                    {
                    "tag": "lugares_turisticos",
                    "patterns": [
                        "¿Qué lugares puedo visitar en la ciudad?",
                        "Recomendaciones turísticas",
                        "¿Qué ver en Bogotá?"
                    ],
                    "responses": [
                        "Puedes visitar Monserrate, el Museo del Oro y la Candelaria.",
                        "Te recomiendo el centro histórico y parques naturales."
                    ]
                    },
                    {
                    "tag": "restaurantes",
                    "patterns": [
                        "¿Dónde puedo comer bien?",
                        "Restaurantes recomendados",
                        "Quiero probar comida típica"
                    ],
                    "responses": [
                        "Puedes probar 'Andrés Carne de Res' o 'Casa Vieja'.",
                        "Te recomiendo restaurantes de comida local como 'El Cielo'."
                    ]
                    },
                    {
                    "tag": "clima_ciudad",
                    "patterns": [
                        "¿Qué clima hace hoy?",
                        "¿Va a llover?",
                        "¿Debo llevar abrigo hoy?"
                    ],
                    "responses": [
                        "Hoy se espera un clima soleado con 23°C.",
                        "Se pronostican lluvias por la tarde, lleva paraguas."
                    ]
                    },
                    {
                    "tag": "horarios_lugares",
                    "patterns": [
                        "¿A qué hora abre el museo?",
                        "Horarios del parque",
                        "¿Hasta qué hora funciona Monserrate?"
                    ],
                    "responses": [
                        "El Museo del Oro abre de 9 a.m. a 5 p.m.",
                        "Monserrate está abierto todos los días hasta las 10 p.m."
                    ]
                    },
                    {
                    "tag": "transporte_ciudad",
                    "patterns": [
                        "¿Cómo me muevo en la ciudad?",
                        "¿Hay transporte público?",
                        "¿Cómo llego al centro?"
                    ],
                    "responses": [
                        "Puedes usar TransMilenio o taxis.",
                        "Te recomiendo Uber o transporte público para llegar al centro."
                    ]
                    }
                ]
                }

    
    def preprocess_text(self, text):
        """Preprocesar texto"""
        text = text.lower()
        text = ''.join([c for c in text if c not in string.punctuation])
        return text
    
    def tokenize_and_stem(self, text):
        """Tokenizar y aplicar stemming"""
        words = nltk.word_tokenize(text, language='spanish')
        words = [self.stemmer.stem(word) for word in words]
        return words
    
    def find_intent(self, user_input):
        """Encontrar la intención más similar"""
        user_input = self.preprocess_text(user_input)
        user_words = set(self.tokenize_and_stem(user_input))
        
        best_match = None
        highest_score = 0
        
        for intent in self.data['intents']:
            for pattern in intent['patterns']:
                pattern_processed = self.preprocess_text(pattern)
                pattern_words = set(self.tokenize_and_stem(pattern_processed))
                
                # Calcular similitud usando intersección de palabras
                if pattern_words and user_words:
                    similarity = len(user_words.intersection(pattern_words)) / len(user_words.union(pattern_words))
                    
                    if similarity > highest_score:
                        highest_score = similarity
                        best_match = intent['tag']
        
        return best_match if highest_score > 0.1 else None
    
    def get_response(self, tag):
        """Obtener respuesta para un tag específico"""
        for intent in self.data['intents']:
            if intent['tag'] == tag:
                return random.choice(intent['responses'])
        return "🤔 Lo siento, no entiendo tu pregunta. ¿Podrías ser más específico sobre turismo en Bogotá?"

# Inicializar el chatbot
chatbot = TouristChatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Por favor, escribe un mensaje.'})
    
    # Encontrar intención y generar respuesta
    intent = chatbot.find_intent(user_message)
    response = chatbot.get_response(intent) if intent else chatbot.get_response(None)
    
    return jsonify({
        'response': response,
        'intent': intent
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
