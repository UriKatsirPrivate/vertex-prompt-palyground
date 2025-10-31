# The Prompt Playground

A comprehensive service designed as a playground for various prompt engineering techniques, powered by Google's Vertex AI Gemini models and hosted on Google Cloud Run.

### ✨ [See the code in action here](https://myprompt.online/) ✨

---

## Features

- **Prompt Engineering Tools:** A wide array of tools for fine-tuning, creating system prompts, agent prompts, meta prompts, and more.
- **Advanced Techniques:** Explore techniques like Zero-to-Few-Shot, Chain of Thought, and D.A.R.E. prompting.
- **Format Generation:** Specialized tools for generating JSON, Nano Banana JSON, and Veo prompts.
- **Image Generation:** Integrated with Imagen3 to generate images from text descriptions.
- **Real-time Configuration:** Interactively adjust model parameters like temperature, top-p, and token limits.

## Prerequisites

Before you begin, ensure you have the following:
- A Google Cloud Project.
- The Vertex AI API enabled in your Google Cloud project.
- `gcloud` CLI installed and authenticated.

## 🚀 Setup and Deployment

### 1. Configure Your Project ID
For security, this application is designed to use Streamlit's secrets management.

1.  Create a secrets file: `.streamlit/secrets.toml`
2.  Add your Google Cloud Project ID to the file:
    ```toml
    GCP_PROJECT_ID = "your-gcp-project-id"
    ```

### 2. Deploy to Cloud Run
The `deploy.sh` script is configured to deploy the application to Google Cloud Run.

1.  **Modify `deploy.sh`:** Update the configuration variables at the top of the script with your project-specific values (e.g., `PROJECT_ID`, `SERVICE_NAME`, `REGION`).
2.  **Service Account Permissions:** Ensure the service account you use for the Cloud Run service has the following IAM roles:
    - `Vertex AI User`: To allow access to Gemini models.
    - `Cloud Run Invoker`: To allow public access to the service if desired.
3.  **Execute the script:**
    ```bash
    ./deploy.sh
    ```

## Usage

Once deployed, navigate to the provided Cloud Run URL. Use the sidebar to select a tool and configure the model parameters. Enter your prompt and see the results.

## 🛠️ Technology Stack

- **Backend:** Python
- **Framework:** Streamlit
- **AI/ML:** Google Vertex AI (Gemini, Imagen)
- **Deployment:** Google Cloud Run, Docker