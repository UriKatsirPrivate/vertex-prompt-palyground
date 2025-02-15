# vertex-prompt-playground
 
Powered by Vertex AI Gemini models & Streamlit. Hosted on Cloud Run.

### See the code in action [here](https://thepromptplayground.xyz/).

### Usage
* In app.py, modify get_project_id function to return your project number
* Deploy to Cloud Run
    * Modify deploy.sh:
        * Replace SERVICE_ACCOUNT_EMAIL with your own service account. 
            * The service account should have _Cloud Run Invoker_ and _Vertex AI User_ permissions.
        * Replace ARTIFACT_REGISTRY_NAME with your own. (The repository should already exist.)
        * Replace GOOGLE_CLOUD_PROJECT with your own.
        * Note the allow-unauthenticated and ingress settings.
    * Execute deploy.sh to deploy the code to Cloud Run.