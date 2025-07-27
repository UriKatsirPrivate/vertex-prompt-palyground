import os
import streamlit as st
# import vertexai
from initialization import initialize_llm_vertex
# from vertexai.preview.vision_models import Image, ImageGenerationModel
from gptrim import trim
from system_prompts import *
from system_prompts import *
from placeholders import *
from system_prompts import *
from meta_prompt import *
from google.genai import types
from fine_tune_prompt import *
from agent_prompt import *
from google.genai.types import (GenerateContentConfig,)
from dare_prompts import *
from system_prompts import *
from image_prompts import *
from video_prompt import *
from google import genai


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

# REGIONS=["us-central1"]
REGIONS=["global"]
MODEL_NAMES=['gemini-2.5-flash','gemini-2.5-pro']

def get_project_id():
    return "landing-zone-demo-341118"

project_id=get_project_id()
# st.sidebar.write("Project ID: ",f"{project_id}")
region=REGIONS[0]
# st.sidebar.write("Region: ",f"{region}")

# region=st.sidebar.selectbox("Region",REGIONS,label_visibility="collapsed")
model_name = st.sidebar.selectbox('Model Name',MODEL_NAMES)
thinking_mode=st.sidebar.text("Thinking Mode: Auto")
max_tokens = st.sidebar.slider('Output Token Limit',min_value=1,max_value=65535,step=100,value=65535)
temperature = st.sidebar.slider('Temperature',min_value=0.0,max_value=2.0,step=0.1,value=1.0)
top_p = st.sidebar.slider('Top-P',min_value=0.0,max_value=1.0,step=0.1,value=0.8)

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.15rem;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7,tab8,tab9, tab10, tab11,tab12 = st.tabs(["Fine-Tune Prompt / ",
                                             "System Prompt / ",
                                             "Agent Prompt / ",
                                             "Meta Prompt / ",
                                             "Json Prompt / ",
                                             "Run Prompt / ",
                                             "Zero to Few / ",
                                             "Chain of Thought / ",
                                             "D.A.R.E Prompting / ",
                                             "Compress Prompt / ",
                                             "Images / ",
                                             "Veo Prompt / "
                                             ])

client, safety_settings,generation_config = initialize_llm_vertex(project_id,region,model_name,max_tokens,temperature,top_p)

with tab1:
    
    # def create_supercharge_prompt(user_input):
        
    #     prompt= supercharge_prompt
        
    #     goal="improve the prompt"
        
    #     formatted_prompt = prompt.format(goal=goal,prompt=user_input)

    #     response = client.models.generate_content(
    #         model=model_name,
    #         contents=formatted_prompt,
    #         config=generation_config,
    #         )
    #     return(response.text)
    def create_refine_prompt(user_input):
        
        prompt= refine_prompt
        
        goal="improve the prompt"
        
        formatted_prompt = prompt.format(task=goal,lazy_prompt=user_input)

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)
    def create_improved_prompt(user_input):
        
        prompt= prompt_improver
        
              
        formatted_prompt = prompt.format(text=user_input)

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)
    def create_make_prompt(prompt_version,user_input):
        
        if prompt_version==1:
            prompt= make_prompt
        else:
            prompt=make_prompt_v2

      
        goal="improve the prompt"
        
        formatted_prompt = prompt.format(task=goal,lazy_prompt=user_input)

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)

    with st.form(key='fine-tune',clear_on_submit=False):
    #Get the prompt from the user
        desc="Write your prompt below, the service will optimize your prompt:"
        prompt = st.text_area(desc,height=200, key=33,placeholder="tweet about Israel")
        
        if st.form_submit_button('Fine-Tune Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating prompts...'):
                    col1, col2= st.columns(2,gap="medium")
                    with col1:
                        # execution_result = create_supercharge_prompt(prompt)
                        # st.text_area(label="Supercharged prompt:",value=execution_result,height=400, key=100)

                        execution_result = create_make_prompt(1,prompt)
                        st.text_area(label="Prompt-1:",value=execution_result,height=400, key=101)

                        execution_result = create_make_prompt(1,prompt)
                        st.text_area(label="Prompt-2:",value=execution_result,height=400, key=102)
                    
                    with col2:
                      execution_result = create_refine_prompt(prompt)
                      st.text_area(label="Prompt-3:",value=execution_result,height=400, key=103)

                      execution_result = create_improved_prompt(prompt)
                      st.text_area(label="Prompt-4:",value=execution_result,height=400, key=104)
            else:
                st.warning('Please enter a prompt before executing.')
with tab6:
    
    def run_prompt(prompt):
        response = client.models.generate_content(model=model_name, contents=prompt)
        return response.text 


    def display_result(execution_result):
        if execution_result != "":
            st.text_area(label="Execution Result:",value=execution_result,height=400, key=50)
        else:
            st.warning('No result to display.')    

    with st.form(key='run-prompt',clear_on_submit=False):
    #Get the prompt from the user
        prompt = st.text_area('Enter your prompt:',height=200, key=1,placeholder="")
        
        if st.form_submit_button('Run Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Running prompt...'):
                    execution_result = run_prompt(prompt)
                display_result(execution_result)
            else:
                st.warning('Please enter a prompt before executing.')                
with tab3:
    
    def create_agent_prompt(user_input):
        
        prompt= agent_prompt
        
        # goal="improve the prompt"
        
        formatted_prompt = prompt.format(prompt=user_input)

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)
    
    def display_result(execution_result):
        if execution_result != "":
            st.text_area(label="Execution Result:",value=execution_result,height=400, key=50)
        else:
            st.warning('No result to display.')    

    with st.form(key='agent-prompt',clear_on_submit=False):
    #Get the prompt from the user
        desc="Write your prompt below, the service will generate a corresponding agentic prompt:"
        prompt = st.text_area(desc,height=200, key=3,placeholder="")
        
        if st.form_submit_button('Agent Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating agent prompt...'):
                    execution_result = create_agent_prompt(prompt)
                display_result(execution_result)
            else:
                st.warning('Please enter a prompt before executing.')
with tab4:
    def create_meta_prompt(user_input):
        response = client.models.generate_content(
            model=model_name,
            contents=user_input,
            config=generation_config,
            )
        return(response.text)
    
    def display_result(execution_result):
        if execution_result != "":
            st.text_area(label="Execution Result:",value=execution_result,height=400, key=50)
        else:
            st.warning('No result to display.')    

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
                    assistant_partial = "<Inputs>"
                    execution_result = create_meta_prompt(prompt)
                display_result(execution_result)
            else:
                st.warning('Please enter a prompt before executing.')     
with tab7:
    
    def zero_to_few_prompt(user_input):
        system_prompt ="""
                        You are an assistant designed to convert a zero-shot prompt into a few-shot prompt.
        """


        prompt= """The zero-shot prompt is: '{zero_shot_prompt}'. Please convert it into a few-shot prompt.
                   Be as elaborate as possible. Make sure to include at least 3 examples.
                """
        
        formatted_prompt = prompt.format(zero_shot_prompt=user_input)

        generation_config = GenerateContentConfig(temperature=temperature,
                                          top_p=top_p,
                                          max_output_tokens=max_tokens,
                                          system_instruction=system_prompt,
                                          response_modalities = ["TEXT"],
                                          safety_settings=safety_settings,
                                    )

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)
    
    def display_result(execution_result):
        if execution_result != "":
            st.text_area(label="Execution Result:",value=execution_result,height=400, key=50)
        else:
            st.warning('No result to display.')    

    with st.form(key='zero-to-few',clear_on_submit=False):
    #Get the prompt from the user
        link="https://www.promptingguide.ai/techniques/fewshot"
        desc="Write your prompt below, the service will generate a corresponding few shots prompt: (See the help icon for more info)"
        prompt = st.text_area(desc,height=200, key=5,help=link)
        
        if st.form_submit_button('Zero to few',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating prompt with shots...'):
                    execution_result = zero_to_few_prompt(prompt)
                display_result(execution_result)
            else:
                st.warning('Please enter a prompt before executing.')
with tab8:
    
    def chain_of_thought_prompt(user_input):
        system_prompt ="""
                        You are an assistant designed to convert a prompt into a chain of thought prompt.
        """


        prompt= """The prompt is: '{prompt}'. Please convert it into a chain of thought prompt.
                    Always append 'Let's think step by step.' to the prompt.
                """
        
        formatted_prompt = prompt.format(prompt=user_input)

        generation_config = GenerateContentConfig(temperature=temperature,
                                          top_p=top_p,
                                          max_output_tokens=max_tokens,
                                          system_instruction=system_prompt,
                                          response_modalities = ["TEXT"],
                                          safety_settings=safety_settings,
                                    )

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)
    
    def display_result(execution_result):
        if execution_result != "":
            st.text_area(label="Execution Result:",value=execution_result,height=400, key=50)
        else:
            st.warning('No result to display.')    

    with st.form(key='chain-of-thought',clear_on_submit=False):
    #Get the prompt from the user
        link="https://www.promptingguide.ai/techniques/cot"
        desc="Write your prompt below, the service will generate a corresponding chain of thought prompt: (See the help icon for more info)"
        prompt = st.text_area(desc,height=200, key=6,help=link)
        
        if st.form_submit_button('Chain of thought',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating Chain of thought prompt...'):
                    execution_result = chain_of_thought_prompt(prompt)
                display_result(execution_result)
            else:
                st.warning('Please enter a prompt before executing.')
with tab9:
    
    def dare_it(query,vision,mission,context):
        
        template_prompt= dare_prompt
        
        formatted_prompt = template_prompt.format(vision=vision,mission=mission,context=context,prompt=query)

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)
    
    def create_dare_artifacts(user_input):
        system_prompt ="""
                        You are a GenAI expert capable of generating solid prompts.
                        Context: D.A.R.E prompting works by asking the chatbot to remember its mission and vision before answering a question.
                        This helps to keep the chatbot grounded in reality and prevents it from generating responses that are irrelevant or nonsensical.
                        D.A.R.E uses vision and mission statements to check if the response complies with them
        """
        template_prompt= dare_artifacts_generator
        formatted_prompt = template_prompt.format(user_input=user_input)

        generation_config = GenerateContentConfig(temperature=temperature,
                                          top_p=top_p,
                                          max_output_tokens=max_tokens,
                                          system_instruction=system_prompt,
                                          response_modalities = ["TEXT"],
                                          safety_settings=safety_settings,
                                    )
        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)
    
    def display_result(execution_result):
        if execution_result != "":
            st.text_area(label="Execution Result:",value=execution_result,height=400, key=50)
        else:
            st.warning('No result to display.')    

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
                    dare_result = dare_it(prompt,vision,mission,context)
                st.text_area('Result', dare_result, height=250, max_chars=None, key=None)
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
                                dare_artifacts_result = create_dare_artifacts(user_input)
                            st.text_area('D.A.R.E Artifacts', dare_artifacts_result, height=250, max_chars=None, key=None)
                    else:
                        st.markdown("Please enter a prompt.")   
with tab10:
    
    with st.form(key='compressprompt'):
        desc="Write your prompt below, the service will compress it:"
        prompt = st.text_area(desc,height=200,placeholder="")
        submit_button = st.form_submit_button(label='Submit Prompt',disabled=not (project_id)  or project_id=="Your Project ID")
        
        if submit_button:
            with st.spinner('Working on it...'):
                trimmed_text = trim(prompt)
                # trimmed_text = "trim(prompt)"
                    
            # Display the trimmed prompt
            if prompt is not None and len(str(trimmed_text)) > 0:
                st.text_area(label="Compressed Prompt",value=trimmed_text, height=250, max_chars=None, key=None)
                st.text("Original Prompt Length: " + str(len(prompt)))
                st.text("Compressed Prompt Length: " + str(len(trimmed_text)))
                st.text("Reduction %: " + "%.2f" % ((len(prompt) - len(trimmed_text)) / len(prompt) * 100))
            else:
                st.text("Please enter a prompt")            
with tab2:
    
    def create_system_prompt(user_input):
        
        prompt= SYSTEM_PROMPT
        
        formatted_prompt = prompt.format(user_input=user_input)

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)
    
    def display_result(execution_result):
        if execution_result != "":
            st.text_area(label="Execution Result:",value=execution_result,height=400, key=50)
        else:
            st.warning('No result to display.')    

    with st.form(key='system-prompt',clear_on_submit=False):
    #Get the prompt from the user
        desc="Write your prompt below, the service will generate a corresponding system prompt:"
        prompt = st.text_area(desc,height=200, key=9,placeholder="")
        
        if st.form_submit_button('System Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating system prompt...'):
                    execution_result = create_system_prompt(prompt)
                display_result(execution_result)
            else:
                st.warning('Please enter a prompt before executing.')
with tab11:
    def GenerateImagePrompt(user_input):
        system_prompt = GenerateImageSystemPrompt


        prompt= """Please generate 2 prompt(s) about: {description}
                """
        
        formatted_prompt = prompt.format(description=user_input)

        generation_config = GenerateContentConfig(temperature=temperature,
                                          top_p=top_p,
                                          max_output_tokens=max_tokens,
                                          system_instruction=system_prompt,
                                          response_modalities = ["TEXT"],
                                          safety_settings=safety_settings,
                                    )

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)
    
    def GenerateImageNew(description,num_of_images):
        client = genai.Client(vertexai=True, project=project_id, location=region)
        images = client.models.generate_images(
            prompt=description,
            model="imagen-3.0-generate-002",
            config=types.GenerateImagesConfig(
                number_of_images=num_of_images,
                # include_rai_reason=True,
                output_mime_type='image/jpeg',
                # add_watermark=True,
                safety_filter_level="BLOCK_ONLY_HIGH",
                person_generation="allow_adult",
                aspect_ratio="9:16",  # "1:1" "16:9" "4:3" "3:4"
                ),
            )
        return images

    def display_images_new(images):
        # for image in images:
        #     st.image(images.generated_images[1].image._pil_image, use_container_width="auto")
        st.image(images.generated_images[0].image._pil_image, use_container_width="auto")
        st.image(images.generated_images[1].image._pil_image, use_container_width="auto")
    
    with st.form(key='prompt_magic10',clear_on_submit=False):
        link="https://cloud.google.com/vertex-ai/docs/generative-ai/image/img-gen-prompt-guide"
        desc="Write your prompt below, See help icon for a prompt guide: (Images will be generated using the Imagen3 model)"
        description = st.text_area(desc,height=200,key=110,placeholder=GENERATE_IMAGES,help=link)
                
        col1, col2 = st.columns(2,gap="large")
        with col1:
        # with st.form(key='prompt_magic10',clear_on_submit=False):
            num_of_prompts=st.number_input("How many prompts to generate",min_value=2,max_value=2,value=2)
            if st.form_submit_button('Generate Prompt(s)',disabled=not (project_id)  or project_id=="Your Project ID"):
                if description:
                    with st.spinner('Generating Prompt(s)...'):
                        improved_prompt = GenerateImagePrompt(description)
                    st.markdown(improved_prompt)
                else:
                    st.markdown("No prompts generated. Please enter a valid prompt.")        
    with st.form(key='prompt_magic1',clear_on_submit=False):
        with col2:
        # with st.form(key='prompt_magic1',clear_on_submit=False):                
        
            num_of_images=st.number_input("How many images to generate",min_value=2,max_value=2,value=2)
            if st.form_submit_button('Generate Image(s)',disabled=not (project_id)  or project_id=="Your Project ID"):
                if description:
                    with st.spinner('Generating Image(s)...'):
                        # images = GenerateImage(description,num_of_images)
                        images = GenerateImageNew(description,num_of_images)
                        if images:
                            display_images_new(images)
                        else:
                           st.markdown("No images generated. Prompt was blocked.")     
                else:
                    st.markdown("No images generated. Please enter a valid prompt.") 
with tab5:
    def json_prompter(user_input):
        
        json_prompt = JSON_PROMPT
        
        formatted_prompt = json_prompt.format(user_input=user_input)
        
        generation_config = GenerateContentConfig(temperature=temperature,
                                          top_p=top_p,
                                          max_output_tokens=max_tokens,
                                        #   system_instruction=system_prompt,
                                          response_modalities = ["TEXT"],
                                          safety_settings=safety_settings,
                                    )

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)
    
    def display_result(execution_result):
        if execution_result != "":
            st.text_area(label="Execution Result:",value=execution_result,height=400, key=50)
        else:
            st.warning('No result to display.')    

    with st.form(key='json-prompt',clear_on_submit=False):
    #Get the prompt from the user
        # link="https://cloud.google.com/vertex-ai/generative-ai/docs/thinking"
        desc="Write your prompt below, the service will generate a corresponding Json prompt"
        prompt = st.text_area(desc,height=200, key=55,placeholder="")
        
        if st.form_submit_button('Json Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating Json prompt...'):
                    execution_result = json_prompter(prompt)
                display_result(execution_result)
            else:
                st.warning('Please enter a prompt before executing.')                                                                   

with tab12:
    def create_video_prompt(user_input):
        
        prompt= video_prompt
                      
        formatted_prompt = prompt.format(user_idea=user_input)

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_prompt,
            config=generation_config,
            )
        return(response.text)
    
    with st.form(key='video-prompt',clear_on_submit=False):
    #Get the prompt from the user
        # link="https://cloud.google.com/vertex-ai/generative-ai/docs/thinking"
        desc="Write your prompt below, the service will generate a corresponding veo prompt"
        prompt = st.text_area(desc,height=200, key=551,placeholder="")
        
        if st.form_submit_button('Veo Prompt',disabled=not (project_id)  or project_id=="Your Project ID"):
            if prompt:
                with st.spinner('Generating optimized veo prompt...'):
                    execution_result = create_video_prompt(prompt)
                display_result(execution_result)
            else:
                st.warning('Please enter a prompt before executing.')