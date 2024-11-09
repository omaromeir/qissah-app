# Qissah App

Qissah App is an innovative platform designed to generate and share Arabic children's stories. Leveraging **ALLAM** for story generation and **DALL-E** for image creation, it offers a unique storytelling experience that emphasizes Arabic culture and values.

---

## Features

- **Story Generation**: Utilizes IBM WatsonX's ALLAM to craft engaging stories tailored for children aged 8-11.
- **Image Generation**: Integrates DALL-E to create complementary images for stories.
- **Arabic Cultural Emphasis**: Ensures narratives and visuals are rich in Arabic traditions and morals.
- **User-Friendly Interface**: Provides an intuitive platform for users to generate and read stories.
- **Customization**: Allows users to input specific characters, settings, and themes for personalized stories.

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Few-Shot Learning](#few-shot-learning)
5. [Docker Deployment](#docker-deployment)
6. [Technologies Used](#technologies-used)
7. [Contributing](#contributing)
8. [License](#license)

---

## Installation

### Prerequisites

- **Python 3.10+**
- **Node.js** (for frontend development)
- **Firebase Account**: For database and authentication services.
- **IBM WatsonX API Key**: For AI model integration.
- **OpenAI API Key**: For DALL-E image generation.
- **ChromaDB**: For vector database management and semantic search.

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/omaromeir/qissah-app.git
   cd qissah-app
   ```

2. **Backend Setup**:
   - Create a virtual environment and activate it:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Set up environment variables for Firebase, IBM WatsonX, and OpenAI:
     ```bash
     export FIREBASE_CREDENTIALS="path/to/firebase_credentials.json"
     export IBM_WATSONX_API_KEY="your_ibm_watsonx_api_key"
     export OPENAI_API_KEY="your_openai_api_key"
     ```
   - Run the backend server:
     ```bash
     flask run
     ```

3. **Frontend Setup**:
   - Navigate to the frontend directory:
     ```bash
     cd frontend
     ```
   - Install the necessary Node.js packages:
     ```bash
     npm install
     ```
   - Start the development server:
     ```bash
     npm start
     ```

---

## Usage

### Run the Application

To start the backend:
```bash
flask run
```

Access the application at `http://localhost:3000`.

### Key Features

- **Story Generation**: Input characters, settings, and themes to generate a story with ALLAM.
- **Image Creation**: Use DALL-E to generate images that match the story.
- **Few-Shot Learning Notebook**: Explore `FewShotLearning Notebook.ipynb` for examples of model fine-tuning.

---

## Few-Shot Learning with Prompt Engineering and RAG

The repository includes a Jupyter Notebook for models with Few-Shot Learning using Prompt Engineering and RAG:
- File: `Integrated_RAG_ALLAM_Story_Generation_with_Prompt.ipynb`
- Purpose: Generate stories through ALLAM using Prompt Engineering and RAG.

To run the notebook:
   ```bash
   jupyter notebook "Integrated_RAG_ALLAM_Story_Generation_with_Prompt.ipynb"
   ```

---

## Docker Deployment

To containerize and deploy the application:

1. Build the Docker image:
   ```bash
   docker build -t flask-app .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 flask-app
   ```

3. Access the app at `http://localhost:5000`.

---

## Technologies Used

- **Backend**: Flask, Python
- **ML Integration**: LangChain, IBM WatsonX ALLAM, OpenAI DALL-E
- **Vector Database**: ChromaDB
- **Frontend (Optional)**: Svelte
- **Containerization**: Docker
- **Notebook**: Jupyter Notebook for Few-Shot Learning with Prompt Engineering and RAG

---

## Contributing

Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add my new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/my-new-feature
   ```
5. Submit a pull request.

---

## License

This project is licensed under Sdaia

---

## Contact

For inquiries or support, contact:
- **GitHub**: [omaromeir](https://github.com/omaromeir)
