# gcloud auth login
export CLAUDE_CODE_USE_VERTEX=1
export ANTHROPIC_VERTEX_PROJECT_ID="landing-zone-demo-341118"
export CLOUD_ML_REGION="global"
gcloud auth application-default login
npx @anthropic-ai/claude-code