from flask import Blueprint, jsonify, request
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from ibm_watsonx_ai.foundation_models import ModelInference
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from sentence_transformers import SentenceTransformer
from chromadb import Client
from chromadb.config import Settings
import os

# Initialize API blueprint and ChromaDB client
api_blueprint = Blueprint('api', __name__)
chroma_client = Client()
collection = chroma_client.get_or_create_collection(name='story_chunks')

# IBM ALLAM model setup
# Define model parameters
model_id = "sdaia/allam-1-13b-instruct"  # Defining model ID
project_id = "07954e26-b0dd-45e4-a22f-0ae8e0a8593a"  # Defining project ID
parameters = {'decoding_method': 'greedy', 'max_new_tokens': 3024, 'repetition_penalty': 1.2}
# Initilaize ALLAM model
allam_model = ModelInference(
    model_id=model_id,
    params=parameters,
    project_id=project_id,
    credentials={
        "url": "https://eu-de.ml.cloud.ibm.com",
        "apikey": "n_mMMf-M68fePv4tTMw5OgipRtv4tB1HLdMeOaf16GRL"
    }
    
)

@api_blueprint.route('/api/story', methods=['POST'])
def generate_story():
    try:
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

        # Define the structured prompt template
        prompt_template = f"""
        بناءً على التفاصيل التالية:
        - الموضوع: {theme}
        - نوع الشخصية: {characterType}
        - عدد الشخصيات: {characterCount}
        - أسماء الشخصيات: {characters}
        - البيئة: {storyLocation}
        - تفاصيل إضافية: {storyMoral}, {otherThings}

        اكتب قصة باللغة العربية لطفل يتراوح عمره بين 8 و11 سنة، مع التركيز على الثقافة العربية.
        استخدم التفاصيل المدخلة من قبل الطفل لجعل القصة قريبة وممتعة له.

        ابدأ بعبارة افتتاحية جذابة ومبتكرة تثير فضول الطفل وتشده لمواصلة القراءة، بحيث تتجنب العبارات التقليدية التي تُستخدم عادة في القصص مثل "كان ياماكان".  قدم الشخصيات وحدد البيئة، ثم ابني الأحداث معطيات الطفل وأضف تفاصيل لتعميق الحبكة. عند كتابة نهاية القصة، تجنّب النهايات النمطية والمعتادة مثل "وعاشوا بسعادة للأبد" أو "انتهى اليوم بكل سعادة" أو "منذ ذلك اليوم" أو "هكذا، ". بدلاً من ذلك، اختتم القصة بنهاية الأحداث فقط. ولا تصرح بالمغزى الأخلاقي للقصة.

        أضف عنوان للقصة.
        """

        # Generate story using IBM ALLAM model
        print("Submitting generation request to IBM ALLAM...")
        story_response = allam_model.generate(prompt_template)  # Extract generated story text

        # Assume `story_response` contains the generated story in a field called `generated_text`
        generated_story = story_response['results'][0]['generated_text']
        print(story_response)

    except Exception as e:
        return jsonify({'error': f"Story generation failed: {str(e)}"}), 500

    return jsonify({'story': generated_story})



# @api_blueprint.route('/api/story', methods=['POST'])
# def generate_story_RAG():
#     try:
#         # Extract child input details from the request
#         data = request.get_json()
        
#         # Check if necessary fields are provided
#         required_fields = ['theme', 'characterType', 'characterCount', 'characters', 'storyLocation', 'storyMoral', 'otherThings']
#         if not all(field in data for field in required_fields):
#             return jsonify({'error': 'Invalid request format, missing data'}), 400

#         # Extract inputs from the request
#         theme = data['theme']
#         characterType = data['characterType']
#         characterCount = data['characterCount']
#         characters = data['characters']
#         storyLocation = data['storyLocation']
#         storyMoral = data['storyMoral']
#         otherThings = data['otherThings']

#         # Construct retrieval query based on the child's input
#         retrieval_prompt = f"A story with {characterType} about {characters} in a {storyLocation}. The story should have the main theme: {theme} with moral: {storyMoral} or additional elements: {otherThings}."
        
#         # Generate an embedding for the retrieval query (modify as per model's retrieval function if needed)
#         query_embedding = embedding_model.encode(retrieval_prompt)  # ALLAM embedding for retrieval prompt

#         # Retrieve relevant story chunks from ChromaDB
#         results = collection.query(
#             query_embeddings=[query_embedding],
#             n_results=3  # Retrieve top 3 similar story chunks
#         )

#         # Combine retrieved story chunks into a single context
#         retrieved_content = " ".join([doc for doc in results["documents"][0]])

#         # Define the structured prompt template
#         prompt_template = PromptTemplate(
#             input_variables=["retrieved_content", "theme", "characterType", "characterCount", "characters", "storyLocation", "storyMoral", "otherThings"],
#             template="""
#             Based on the following input details:
#             - Main theme: {theme}
#             - Character Type: {characterType}
#             - Number of characters: {characterCount}
#             - Name of Characters: {characters}
#             - Setting: {storyLocation}
#             - Main Theme: {storyMoral}
#             - More details: {otherThings}
#             - Retrieved Content: {retrieved_content}
            
#             Based on the input details provided, write a short Arabic story for children aged 8-11, emphasizing Arabic culture. Ensure it has a clear beginning, middle, and end, and conclude with a unique ending type.
#             """
#         )

#         # Format the final prompt using PromptTemplate
#         formatted_prompt = prompt_template.format(
#             retrieved_content=retrieved_content,
#             theme=theme,
#             characterType=characterType,
#             characterCount=characterCount,
#             characters=characters,
#             storyLocation=storyLocation,
#             storyMoral=storyMoral,
#             otherThings=otherThings
#         )

#         # Generate story using IBM ALLAM model
#         print("Submitting generation request to IBM ALLAM...")
#         story_response = allam_model.generate(formatted_prompt)  # Extract generated story text

#         # Assume `story_response` contains the generated story in a field called `generated_text`
#         generated_story = story_response['results'][0]['generated_text']
#         print(story_response)

#     except Exception as e:
#         return jsonify({'error': f"Story generation failed: {str(e)}"}), 500

#     return jsonify({'story': generated_story})


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
        prompt_text = f"Generate a concise, detailed prompt (1000 characters or less) to generate an image, without any writing, with a illustration appearance, that is appropriate for kids, based on the following description: {image_desc}"
        
        # Generate the prompt response using the model
        response = llm.invoke([{"role": "user", "content": prompt_text}])
        generated_prompt = response.content

        # Use the generated prompt with DALL-E API
        image_url = DallEAPIWrapper().run(generated_prompt)

        return jsonify({'image_url': image_url})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
