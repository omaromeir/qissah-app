from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import logging
import openai

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

logging.basicConfig(level=logging.DEBUG)

# Set your OpenAI API key
openai.api_key = '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'

@app.route('/')
@cross_origin()
def hello():
    return "Hello, this is the Flask back end!"

@app.route('/api/story', methods=['POST', 'OPTIONS'])
@cross_origin()
def generate_story():
    story = "هذه القصة من علاااااام!"
    return jsonify({'story': story})
    # data = request.get_json()
    # if not data or 'theme' not in data or 'characters' not in data or 'otherThings' not in data:
    #     return jsonify({'error': 'Invalid request format, missing data'}), 400

    # # Extract inputs from the request
    # theme = data['theme']
    # characters = data['characters']
    # otherThings = data['otherThings']

    # # Generate story using OpenAI API
    # try:
    #     response = openai.Completion.create(
    #         engine="text-davinci-003",  # Use "gpt-3.5-turbo" or another model if preferred
    #         prompt=f"Write a story about {characters} in a {theme}. Include {otherThings}.",
    #         max_tokens=150,
    #         n=1,
    #         stop=None,
    #         temperature=0
    #     )
        
    #     story = response.choices[0].text.strip()  # Get the generated story

    #     return jsonify({'story': story})

    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

