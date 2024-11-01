from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import logging
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
@cross_origin()
def hello():
    return "Hello, this is the Flask back end!"

@app.route('/api/story', methods=['POST', 'OPTIONS'])
@cross_origin()
def generate_story():
    # story = "هذه القصة من علاااااام!"
    # return jsonify({'story': story})
    data = request.get_json()
    if not data or 'theme' not in data or 'characters' not in data or 'otherThings' not in data:
        return jsonify({'error': 'Invalid request format, missing data'}), 400

    # Extract inputs from the request
    theme = data['theme']
    characters = data['characters']
    otherThings = data['otherThings']

    # Generate story using OpenAI API
    try:
        # Ensure API keys are available in environment variables
        if "LANGCHAIN_API_KEY" not in os.environ or "OPENAI_API_KEY" not in os.environ:
            raise EnvironmentError("API keys not set. Please set LANGCHAIN_API_KEY and OPENAI_API_KEY as environment variables.")

        # Initialize the model
        model = ChatOpenAI(model="gpt-4o-mini")

        # Define messages based on the user inputs
        messages = [
            SystemMessage(content="This is a children's story in Arabic. Make it simple and clear. Make it very short. It must be in simple, standard Arabic."),
            HumanMessage(content=f"Write a story about {characters} in a {theme}. Include {otherThings}."),
        ]

        print("Messages:", messages)

        # Invoke the model with the messages
        response = model.invoke(messages)
        print("Response:", response)

        return jsonify({'story': response.content})  # Access the content of the response

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

