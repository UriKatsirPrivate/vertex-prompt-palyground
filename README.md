# vertex-prompt-playground
 
Powered by Vertex AI Gemini models & Streamlit. Hosted on Cloud Run.

### See the code in action [here](https://myprompt.online/).

### Usage
* In app.py, modify get_project_id function to return your project ID.
* Deploy to Cloud Run
    * Modify deploy.sh:
        * Modify all values under the "Configuration Variables" section with your own
            * The service account should have _Cloud Run Invoker_ and _Vertex AI User_ permissions.
    * Execute deploy.sh to deploy the code to Cloud Run.