
   # Baldwin-AI

   Welcome to Baldwin-AI! This project provides a web-based AI assistant using a Retrieval-Augmented Generation (RAG) model to enhance interactions and provide contextual responses based on uploaded documents.

   ## Features

   - **PDF Uploads**: Upload multiple PDF documents for processing.
   - **Index Creation**: Create and manage an index for your documents.
   - **AI Chatbot**: Interact with an AI chatbot that uses RAG to provide contextually relevant responses based on the uploaded documents.
   - **Document Processing**: Process and index documents using Elasticsearch and sentence transformers.

   ## Getting Started

   ### Prerequisites

   - Python 3.7+
   - Streamlit
   - Sentence Transformers
   - Elasticsearch
   - LangChain

   ### Installation

1. **Clone the Chatbot project only:**

      ```bash
         git clone --no-checkout https://github.com/usernamerepository.git my-repo
         cd my-repo
         git config core.sparseCheckout true
         echo "rag-chatbot/" >> .git/info/sparse-checkout
         git checkout main
      ```

2. **Set up the Conda environment and install required packages:**

      ```bash
      source conda_setup_env.sh
      ```

3. **Launch Docker containers for kibanna and elastic search:**
     
    ```bash
    docker compose up
    ```

     

4. **Test Elasticsearch:**

      - Ensure Elasticsearch is installed and running on `http://localhost:9200`. 

5. **Configure API keys (required for openai):**

      - You may need to configure API keys for OpenAI or other services. Add them to your `.env` file or directly in the Streamlit sidebar.

## Usage

   1. **Run the Streamlit app:**

      ```bash
      streamlit run app.py
      ```

      This will open the Baldwin-AI web application in your default web browser.

   2. **Upload PDFs and interact with the AI assistant:**

      - Use the sidebar to upload PDF files.
      - Create an index for your documents.
      - Start chatting with the AI assistant to get contextually relevant responses based on the uploaded documents.

   ## Project Structure

   - `streamlit.py`: Main Streamlit application file.
   - `parse_lama.py`: Module for processing PDF files.
   - `embed.py`: Module for indexing data into Elasticsearch.
   - `rag_chatbot.py`: Module for setting up and interacting with the RAG model.

   ## Contributing

   Contributions are welcome! Please follow these steps to contribute:

   1. Fork the repository.
   2. Create a new branch (`git checkout -b feature/your-feature`).
   3. Commit your changes (`git commit -am 'Add new feature'`).
   4. Push to the branch (`git push origin feature/your-feature`).
   5. Create a new Pull Request.

   ## License

   This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

   ## Acknowledgments

   - Thanks to the creators of the [Sentence Transformers](https://www.sbert.net/) and [LangChain](https://github.com/langchain/langchain) libraries for their powerful tools.
   - Special thanks to the [Elasticsearch](https://www.elastic.co/what-is/elasticsearch) team for their robust search engine.
   
## Versioning

- **Version 1**: Supports GPT-based models for generating responses.
- **Version 2 (Planned)**: Will include support for LLaMA 70B models.
