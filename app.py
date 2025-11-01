import streamlit as st
from initialization import safety_settings
from placeholders import GENERATE_IMAGES
from utils import (
    get_project_id,
    get_llm_client,
    display_result,
    create_make_prompt,
    create_refine_prompt,
    create_improved_prompt,
    create_system_prompt,
    create_agent_prompt,
    create_meta_prompt,
    json_prompter,
    banana_json_prompter,
    run_prompt,
    zero_to_few_prompt,
    chain_of_thought_prompt,
    dare_it,
    create_dare_artifacts,
    run_trim,
    GenerateImagePrompt,
    GenerateImageNew,
    display_images_new,
    create_video_prompt,
    MODEL_NAMES,
    REGIONS,
    metaprompt,
)
from google.genai.types import (GenerateContentConfig,)


# https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
st.set_page_config(
    page_title="The Prompt Playground",
    page_icon="icons/vertexai.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://github.com/UriKatsirPrivate/vertex-prompt-palyground',
        'About': "#### Created by [Uri Katsir](https://www.linkedin.com/in/uri-katsir/)"
    }
)

st.warning("Starting November 2025, this service will migrate to https://myprompt.online/")

project_id=get_project_id()
# st.sidebar.write("Project ID: ",f"{project_id}")
region=REGIONS[0]
# st.sidebar.write("Region: ",f"{region}")

# ==============================================================================
# region=st.sidebar.selectbox("Region",REGIONS,label_visibility="collapsed")
st.sidebar.title("Model Configuration")
model_name = st.sidebar.selectbox('Model Name', MODEL_NAMES, label_visibility="collapsed")

# with st.sidebar.expander("Advanced Settings"):
#     max_tokens = st.slider('Output Token Limit',min_value=1,max_value=65535,step=100,value=65535)
#     temperature = st.slider('Temperature',min_value=0.0,max_value=2.0,step=0.1,value=1.0)
#     top_p = st.slider('Top-P',min_value=0.0,max_value=1.0,step=0.1,value=0.8)
#     st.caption("Thinking Mode: Auto")

tool_categories = {
    "Prompt Engineering": [
        "Fine-Tune Prompt",
        "System Prompt",
        "Json Prompt",
        "Nano Banana Json Prompt",
        "Images",
        "Veo Prompt",
        "Run Prompt",
        "Meta Prompt",
        "Agent Prompt",
        "Zero to Few",
        "Chain of Thought",
        "D.A.R.E Prompting",
        "Compress Prompt",
    ],
}
st.sidebar.caption("Thinking Mode: Auto")
st.sidebar.title("Tools")



# Create a single list of all tools for the selectbox
all_tools = [tool for tools in tool_categories.values() for tool in tools]

# Use a single selectbox for page navigation
page = st.sidebar.selectbox("Select a tool", all_tools)

with st.sidebar.expander("Advanced Settings"):
    max_tokens = st.slider('Output Token Limit',min_value=1,max_value=65535,step=100,value=65535)
    temperature = st.slider('Temperature',min_value=0.0,max_value=2.0,step=0.1,value=1.0)
    top_p = st.slider('Top-P',min_value=0.0,max_value=1.0,step=0.1,value=0.8)
    # st.caption("Thinking Mode: Auto")

# Initialize client once and cache it
client = get_llm_client(project_id, region)

# Create generation config on each run, as it depends on sliders. This is fast.
generation_config = GenerateContentConfig(
    temperature=temperature,
    top_p=top_p,
    max_output_tokens=max_tokens,
    safety_settings=safety_settings,
)

if page == "Fine-Tune Prompt":
    st.header("Fine-Tune Prompt")
    with st.form(key='fine-tune',clear_on_submit=False):
        desc="Write your prompt below, the service will optimize your prompt:"
        prompt = st.text_area(desc,height=200, key=33,placeholder="tweet about Israel")
        
        if st.form_submit_button('Fine-Tune Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating prompts...'):
                    col1, col2= st.columns(2,gap="medium")
                    with col1:
                        execution_result = create_make_prompt(client, project_id, region, model_name, generation_config, 1, prompt)
                        st.code(execution_result, language=None)

                        execution_result = create_make_prompt(client, project_id, region, model_name, generation_config, 2, prompt)
                        st.code(execution_result, language=None)
                    
                    with col2:
                      execution_result = create_refine_prompt(client, project_id, region, model_name, generation_config, prompt)
                      st.code(execution_result, language=None)
                      execution_result = create_improved_prompt(client, project_id, region, model_name, generation_config, prompt)
                      st.code(execution_result, language=None)
            else:
                st.warning('Please enter a prompt before executing.')

elif page == "System Prompt":
    st.header("System Prompt")
    with st.form(key='system-prompt',clear_on_submit=False):
    #Get the prompt from the user
        desc="Write your prompt below, the service will generate a corresponding system prompt:"
        prompt = st.text_area(desc,height=200, key=9,placeholder="")
        
        if st.form_submit_button('System Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating system prompt...'):
                    execution_result = create_system_prompt(client, project_id, region, model_name, generation_config, prompt)
                display_result(execution_result, "system_prompt")
            else:
                st.warning('Please enter a prompt before executing.')

elif page == "Agent Prompt":
    st.header("Agent Prompt")
    with st.form(key='agent-prompt',clear_on_submit=False):
    #Get the prompt from the user
        desc="Write your prompt below, the service will generate a corresponding agentic prompt:"
        prompt = st.text_area(desc,height=200, key=3,placeholder="")
        
        if st.form_submit_button('Agent Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating agent prompt...'):
                    execution_result = create_agent_prompt(client, project_id, region, model_name, generation_config, prompt)
                display_result(execution_result, "agent_prompt")
            else:
                st.warning('Please enter a prompt before executing.')

elif page == "Meta Prompt":
    st.header("Meta Prompt")
    with st.form(key='metaprompt',clear_on_submit=False):
    #Get the prompt from the user
        link="https://meta-prompting.github.io/"
        desc="Write your prompt below, the service will generate a corresponding meta prompt: (See the help icon for more info)"
        prompt = st.text_area(desc,height=200, key=4,help=link)
        
        if st.form_submit_button('Meta-Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                TASK=prompt
                with st.spinner('Generating meta-prompt...'):
                    prompt = metaprompt.replace("{{TASK}}", TASK)
                    execution_result = create_meta_prompt(client, project_id, region, model_name, generation_config, prompt)
                display_result(execution_result, "meta_prompt")
            else:
                st.warning('Please enter a prompt before executing.')     

elif page == "Json Prompt":
    st.header("Json Prompt")
    with st.form(key='json-prompt',clear_on_submit=False):
    #Get the prompt from the user
        desc="Write your prompt below, the service will generate a corresponding Json prompt"
        prompt = st.text_area(desc,height=200, key=55,placeholder="")
        
        if st.form_submit_button('Json Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating Json prompt...'):
                    execution_result = json_prompter(client, project_id, region, model_name, generation_config, prompt)
                display_result(execution_result, "json_prompt")
            else:
                st.warning('Please enter a prompt before executing.')                                                                   
elif page == "Nano Banana Json Prompt":
    st.header("Nano Banana Prompt")
    with st.form(key='banana-json-prompt',clear_on_submit=False):
    #Get the prompt from the user
        desc="Write your prompt below, the service will generate a corresponding Nano Banana Json prompt"
        prompt = st.text_area(desc,height=200, key=55,placeholder="")
        
        if st.form_submit_button('Nano Banana Json Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating Json prompt...'):
                    execution_result = banana_json_prompter(client, project_id, region, model_name, generation_config, prompt)
                display_result(execution_result, "json_prompt")
            else:
                st.warning('Please enter a prompt before executing.')                                                                   
elif page == "Run Prompt":
    st.header("Run Prompt")

    with st.form(key='run-prompt',clear_on_submit=False):
    #Get the prompt from the user
        prompt = st.text_area('Enter your prompt:',height=200, key=1,placeholder="")
        
        if st.form_submit_button('Run Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Running prompt...'):
                    execution_result = run_prompt(client, project_id, region, model_name, generation_config, prompt)
                display_result(execution_result, "run_prompt")
            else:
                st.warning('Please enter a prompt before executing.')                

elif page == "Zero to Few":
    st.header("Zero to Few")
    with st.form(key='zero-to-few',clear_on_submit=False):
    #Get the prompt from the user
        link="https://www.promptingguide.ai/techniques/fewshot"
        desc="Write your prompt below, the service will generate a corresponding few shots prompt: (See the help icon for more info)"
        prompt = st.text_area(desc,height=200, key=5,help=link)
        
        if st.form_submit_button('Zero to few',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating prompt with shots...'):
                    execution_result = zero_to_few_prompt(client, project_id, region, model_name, generation_config, prompt)
                display_result(execution_result, "zero_to_few")
            else:
                st.warning('Please enter a prompt before executing.')

elif page == "Chain of Thought":
    st.header("Chain of Thought")
    with st.form(key='chain-of-thought',clear_on_submit=False):
    #Get the prompt from the user
        link="https://www.promptingguide.ai/techniques/cot"
        desc="Write your prompt below, the service will generate a corresponding chain of thought prompt: (See the help icon for more info)"
        prompt = st.text_area(desc,height=200, key=6,help=link)
        
        if st.form_submit_button('Chain of thought',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating Chain of thought prompt...'):
                    execution_result = chain_of_thought_prompt(client, project_id, region, model_name, generation_config, prompt)
                display_result(execution_result, "cot")
            else:
                st.warning('Please enter a prompt before executing.')

elif page == "D.A.R.E Prompting":
    st.header("D.A.R.E Prompting")
    with st.form(key='dare',clear_on_submit=False):
        link="https://www.linkedin.com/posts/ram-seshadri-nyc-nj_how-do-you-reduce-hallucinations-ensure-activity-7085123540177285121-THrK/"
        vision_help="Enter your vision: See help icon for more information about the DARE prompting technique:"
        vision=st.text_input(vision_help ,placeholder="Marketing assistant",help=link)
        mission=st.text_input("Enter your mission:", placeholder="Help people plan marketing events",help="")
        context=st.text_area("Enter your context:",height=68, placeholder="You are a marketing assistant. Be as elaborate as makes sense",help="")
        prompt=st.text_area("Enter your prompt:",height=68, placeholder="Plan cloud run marketing workshop",help="")
    
        if st.form_submit_button('D.A.R.E',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('working on it...'):
                    dare_result = dare_it(client, project_id, region, model_name, generation_config, prompt, vision, mission, context)
                st.code(dare_result, language=None)
            else:
                st.markdown("Please enter a prompt.")   
    help_me=st.checkbox("Help Me Create D.A.R.E Artifacts")
    with st.form(key='dareassist',clear_on_submit=False):
            
            if help_me:
                # st.write('Enter your prompt below and click the button')
                user_input=st.text_input("Enter your prompt below and click the button:")
                if st.form_submit_button(' D.A.R.E Artifacts',disabled=not (project_id)  or project_id=="Your Project ID"):
                    if user_input:
                            with st.spinner('working on it...'):
                                dare_artifacts_result = create_dare_artifacts(client, project_id, region, model_name, temperature, top_p, max_tokens, safety_settings, user_input)
                            st.code(dare_artifacts_result, language=None)
                    else:
                        st.markdown("Please enter a prompt.")

elif page == "Compress Prompt":
    st.header("Compress Prompt")
    with st.form(key='compressprompt'):
        desc="Write your prompt below, the service will compress it:"
        prompt = st.text_area(desc,height=200,placeholder="")
        submit_button = st.form_submit_button(label='Submit Prompt',disabled=not (project_id)  or project_id=="Your Project ID")
        
        if submit_button:
            with st.spinner('Working on it...'):
                trimmed_text = run_trim(prompt)
                # trimmed_text = "trim(prompt)"
                    
            # Display the trimmed prompt
            if prompt is not None and len(str(trimmed_text)) > 0:
                st.code(trimmed_text, language=None)
                st.text("Original Prompt Length: " + str(len(prompt)))
                st.text("Compressed Prompt Length: " + str(len(trimmed_text)))
                st.text("Reduction %: " + "%.2f" % ((len(prompt) - len(trimmed_text)) / len(prompt) * 100))
            else:
                st.text("Please enter a prompt")

elif page == "Images":
    st.header("Images")
    with st.form(key='prompt_magic10',clear_on_submit=False):
        link="https://cloud.google.com/vertex-ai/docs/generative-ai/image/img-gen-prompt-guide"
        desc="Write your prompt below, See help icon for a prompt guide: (Images will be generated using Imagen4)"
        description = st.text_area(desc,height=200,key=110,placeholder=GENERATE_IMAGES,help=link)
                
        col1, col2 = st.columns(2,gap="large")
        with col1:
        # with st.form(key='prompt_magic10',clear_on_submit=False):
            num_of_prompts=st.number_input("How many prompts to generate",min_value=2,max_value=2,value=2)
            if st.form_submit_button('Generate Prompt(s)',disabled=not (project_id)  or project_id=="Your Project ID"):
                if description:
                    with st.spinner('Generating Prompt(s)...'):
                        improved_prompt = GenerateImagePrompt(client, project_id, region, model_name, temperature, top_p, max_tokens, safety_settings, description)
                    st.markdown(improved_prompt, unsafe_allow_html=False)
                else:
                    st.markdown("No prompts generated. Please enter a valid prompt.")        
    with st.form(key='prompt_magic1',clear_on_submit=False):
        with col2:
        # with st.form(key='prompt_magic1',clear_on_submit=False):                
        
            num_of_images=st.number_input("How many images to generate",min_value=2,max_value=2,value=2)
            if st.form_submit_button('Generate Image(s)',disabled=not (project_id)  or project_id=="Your Project ID"):
                if description:
                    with st.spinner('Generating Image(s)...'):
                        images = GenerateImageNew(client, description,num_of_images)
                        if images:
                            display_images_new(images)
                        else:
                           st.markdown("No images generated. The prompt may have been blocked by safety filters.")
                else:
                    st.markdown("No images generated. Please enter a valid prompt.")

elif page == "Veo Prompt":
    st.header("Veo Prompt")
    with st.form(key='video-prompt',clear_on_submit=False):
        desc="Write your prompt below, the service will generate a corresponding veo prompt"
        prompt = st.text_area(desc,height=200, key=551,placeholder="")
        
        if st.form_submit_button('Veo Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating optimized veo prompt...'):
                    execution_result = create_video_prompt(client, project_id, region, model_name, generation_config, prompt)
                display_result(execution_result, "veo_prompt")
            else:
                st.warning('Please enter a prompt before executing.')