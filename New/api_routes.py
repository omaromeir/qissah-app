from flask import Blueprint, jsonify, request
from langchain_openai import ChatOpenAI
from langchain import PromptTemplate
from ibm_watsonx_ai.foundation_models import ModelInference
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

import os

# Initialize API blueprint and ChromaDB client
api_blueprint = Blueprint('api', __name__)
chroma_client = Client()
collection = chroma_client.get_or_create_collection(name='story_chunks')

# IBM ALLAM model setup
model_id = 'sdaia/allam-1-13b-instruct'
allam_model = ModelInference(
    model_id = model_id,
    params= {"decoding_method": "greedy", "max_new_tokens": 1024, "repetition_penalty": 1.2},
    credentials= {
		"url": "https://eu-de.ml.cloud.ibm.com",
		"apikey": getpass.getpass("n_mMMf-M68fePv4tTMw5OgipRtv4tB1HLdMeOaf16GRL")
	}
)



@api_blueprint.route('/api/story', methods=['POST'])
def generate_story():

    # Extract child input details from the request
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

    # Construct retrieval query based on the child's input
    retrieval_prompt = f"A story with {characterType} about {characters} in a {storyLocation}. The story should have the main theme: {storyMoral} or additional elements: {otherThings}."
    
    # Generate an embedding for the retrieval query (modify as per model's retrieval function if needed)
    query_embedding = allam_model.embed_text(retrieval_prompt)  # ALLAM embedding for retrieval prompt

    # Retrieve relevant story chunks from ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3  # Retrieve top 3 similar story chunks
    )

    # Combine retrieved story chunks into a single context
    retrieved_content = " ".join([doc for doc in results["documents"][0]])

    # Define the structured prompt template
    prompt_template = PromptTemplate(
        input_variables=["retrieved_content", "characterType", "characterCount", "characters", "storyLocation", "storyMoral", "otherThings" ],
        template="""
        Based on the following input details:
        - Character Type: {characterType}
        - Number of characters: {characterCount}
        - Name of Charachters: {characters}
        - Setting: {storyLocation}
        - Main Theme: {storyMoral}
        - More details: {otherThings}
        - Retrieved Content: {retrieved_content}
        
        Based on the input details provided, write a short Arabic story for children aged 8-11, emphasizing Arabic culture. Ensure it has a clear beginning, middle, and end, and conclude with a unique ending type.
        
        
        """
    )

    # Format the final prompt using PromptTemplate
    formatted_prompt = prompt_template.format(
        retrieved_content=retrieved_content,
        characterType = characterType,
        characterCount = characterCount,
        characters = characters,
        storyLocation = storyLocation,
        storyMoral = storyMoral,
        otherThings = otherThings

    )
    # Generate story using IBM ALLAM model
    print("Submitting generation request to IBM ALLAM...")
    story_response = allam_model.generate(formatted_prompt)
    generated_story = story_response['text']  # Extract generated story text


    except Exception as e:
        return jsonify({'error': f"Story generation failed: {str(e)}"}), 500

    return jsonify({'story': generated_story})

@api_blueprint.route('/api/generate_image', methods=['POST'])
def generate_image():
    data = request.get_json()
    if not data or 'image_desc' not in data:
        return jsonify({'error': 'Invalid request format, missing image description'}), 400

    # Extract the image description from the request
    image_desc = data['image_desc']

    # Generate the image URL using DALL-E
    try:
        # Initialize the LLM and prompt template for image prompt generation
        llm = OpenAI(temperature=0.9)
        prompt = PromptTemplate(
            input_variables=["image_desc"],
            template="Generate a concise, detailed prompt (1000 characters or less) to generate an image, without any writing, with a sketch appearance, that is appropriate for kids, based on the following description: {image_desc}",
        )
        chain = prompt | llm

        # Generate the detailed prompt
        generated_prompt = chain.invoke(image_desc)
        print("Generated prompt for image:", generated_prompt)

        # Use the generated prompt with DALL-E API
        image_url = DallEAPIWrapper().run(generated_prompt)
        print("Generated image URL:", image_url)

        return jsonify({'image_url': image_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
