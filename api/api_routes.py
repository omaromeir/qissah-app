from flask import Blueprint, jsonify, request
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import PromptTemplate
import os

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/story', methods=['POST'])
def generate_story():
    print("LANGCHAIN_API_KEY:", os.environ.get("LANGCHAIN_API_KEY"))
    print("OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))
    data = request.get_json()
    
    # Check if necessary fields are provided
    required_fields = ['theme', 'characterType', 'characterCount', 'characters', 'storyLocation', 'storyMoral', 'otherThings']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Invalid request format, missing data'}), 400

    # Extract inputs from the request
    theme = data['theme']
    characterType = data['characterType']
    characterCount = data['characterCount']
    characters = data['characters']
    storyLocation = data['storyLocation']
    storyMoral = data['storyMoral']
    otherThings = data['otherThings']

    # Generate story using OpenAI API
    try:
        if "LANGCHAIN_API_KEY" not in os.environ or "OPENAI_API_KEY" not in os.environ:
            raise EnvironmentError("API keys not set. Please set LANGCHAIN_API_KEY and OPENAI_API_KEY as environment variables.")

        # Initialize the model
        model = ChatOpenAI(model="gpt-4o-mini")

        # Define messages based on the user inputs
        messages = [
            SystemMessage(content="This is a children's story in Arabic. Make it simple and clear. Make it very short. It must be appropriate for 9-10 year olds. It must be in simple, standard Arabic."),
            HumanMessage(content=f"Write a story about {characters} in a {theme}. The story should have {characterCount} characters, include a location like {storyLocation}, and convey the moral values: {storyMoral}. Additional elements: {otherThings}.")
        ]

        # Invoke the model with the messages
        response = model.invoke(messages)
        story_content = response.content  # Access the content of the response
        print("Generated Story:", story_content)

    except Exception as e:
        return jsonify({'error': f"Story generation failed: {str(e)}"}), 500

    return jsonify({'story': story_content})

@api_blueprint.route('/api/generate_image', methods=['POST'])
def generate_image():
    data = request.get_json()
    if not data or 'image_desc' not in data:
        return jsonify({'error': 'Invalid request format, missing image description'}), 400

    # Extract the image description from the request
    image_desc = data['image_desc']

    # Generate the image URL using DALL-E
    try:
        # Initialize the chat-based LLM model
        llm = ChatOpenAI(model="gpt-4", temperature=0.9)  # Update with your actual model if different

        # Create the prompt for generating an image
        prompt_text = f"Generate a concise, detailed prompt (1000 characters or less) to generate an image, without any writing, with a sketch appearance, that is appropriate for kids, based on the following description: {image_desc}"
        
        # Generate the prompt response using the model
        response = llm.invoke([{"role": "user", "content": prompt_text}])
        generated_prompt = response.content
        print("Generated prompt for image:", generated_prompt)

        # Use the generated prompt with DALL-E API
        image_url = DallEAPIWrapper().run(generated_prompt)
        print("Generated image URL:", image_url)

        return jsonify({'image_url': image_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
