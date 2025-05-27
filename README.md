# FAQ Search System

This project implements an FAQ Search System using RAG (Retrieval Augmented Generation) with a PostgreSQL database and pgvector for storing and querying vector embeddings.

The system allows users to search frequently asked questions using natural language and retrieves the most relevant answers based on semantic similarity. Search results include the question and answer, along with metadata such as category, creation date, and similarity score.

## Getting Started

Follow these steps to set up and run the FAQ Search System locally:

1.  **Clone your repository:**

    ```bash
    git clone https://github.com/seonokkim/rag-pgvector.git
    cd rag-pgvector
    ```

2.  **Set up environment variables:**

    Create a `.env.local` file in the root directory of the project. Copy the contents from `.env.example` (if it exists) and update the variables, especially the database connection string and any API keys (e.g., `OPENAI_API_KEY`).

    ```dotenv
    # Example variables (adjust as needed)
    DATABASE_URL="postgresql://user:password@localhost:5432/mydatabase"
    OPENAI_API_KEY="your_openai_api_key"
    ```

3.  **Start Docker containers:**

    Use Docker Compose to start the PostgreSQL database container.

    ```bash
    docker-compose up -d
    ```

    Wait a few moments for the database to initialize.

4.  **Install dependencies:**

    Install the project dependencies using npm.

    ```bash
    npm install
    ```

5.  **Set up the database schema and run migrations:**

    Apply the database schema and run any pending migrations using Prisma.

    ```bash
    npx prisma migrate dev
    ```

6.  **Ingest FAQ data:**

    Run the data ingestion script to load FAQ data into the database. This step might vary depending on where the ingestion script is located and how it's run.

    ```bash
    # Example: Assuming an ingest script in the 'scripts' directory
    npx ts-node scripts/ingest.ts
    ```
    *Note: The exact command for data ingestion might differ based on the project structure.*

7.  **Run the application:**

    Start the development server.

    ```bash
    npm run dev
    ```

    The application should now be running and accessible, likely at `http://localhost:3000` or similar. 


## Database Structure (TablePlus Example)

The project uses a PostgreSQL database with the `pgvector` extension to store vector embeddings for the FAQ data. Below is an example view of the `embeddings` table in TablePlus:

![TablePlus Embeddings Table](images/tableplus_embeddings.png)

## Streamlit Application

This project includes a user-friendly web interface built with Streamlit for the FAQ Search System. You can interact with the search functionality through this application.

![Streamlit App GUI](images/streamlit_app_gui.png)

## Acknowledgments
This project is based on the code from [daveebbelaar/pgvectorscale-rag-solution](https://github.com/daveebbelaar/pgvectorscale-rag-solution/tree/setup). 
