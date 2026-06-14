supercharge_prompt="""
Write a writing prompt that if followed will lead to this: {goal}.
Here is their original (lazy) writing prompt: {prompt}.
You must improve the writing prompt to make it fit the goal.
Here are general tips on writing great instructions that create writing prompts:
Be specific and descriptive about the desired tone, context, format, persona, examples, task. Go into detail about the requirements
Task: The main action you want to be executed. Includes verb or action word. ex: write an x, summarize this y.
Persona: The voice or character you want the model to assume. ex: anime villain, 5 year old. 
Format: The visual layout or presentation or medium of the desired output. ex: email, monologue, report, article, use tables. 
Tone: The tone or mood in which the response should be delivered. ex: 'use a formal and friendly tone', 'use suggestive language'
Exemplars: Specific elements the user wants to include. Overview of contents. 
Context: Informational Context about the task - often substring of task. 
dedicate a sentence at least to each of these.
Writing Prompt:
"""

refine_prompt="""
Your goal is to improve the prompt given below for {task} :
--------------------

Prompt: {lazy_prompt}

--------------------

Here are several tips on writing great prompts:

-------

Start the prompt by stating that it is an expert in the subject.

Put instructions at the beginning of the prompt and use ### or to separate the instruction and context 

Be specific, descriptive and as detailed as possible about the desired context, outcome, length, format, style, etc 

---------

Here's an example of a great prompt:

As a master YouTube content creator, develop an engaging script that revolves around the theme of "Exploring Ancient Ruins."

Your script should encompass exciting discoveries, historical insights, and a sense of adventure.

Include a mix of on-screen narration, engaging visuals, and possibly interactions with co-hosts or experts.

The script should ideally result in a video of around 10-15 minutes, providing viewers with a captivating journey through the secrets of the past.

Example:

"Welcome back, fellow history enthusiasts, to our channel! Today, we embark on a thrilling expedition..."

-----

Now, improve the prompt.

IMPROVED PROMPT:
"""

make_prompt="""
Your goal is to improve the prompt given below for {task} :
--------------------

Prompt: {lazy_prompt}

--------------------

Here are several tips on writing great prompts:

-------

Start the prompt by stating that it is an expert in the subject.

Put instructions at the beginning of the prompt and use ### or to separate the instruction and context 

Be specific, descriptive and as detailed as possible about the desired context, outcome, length, format, style, etc 

---------

Here's an example of a great prompt:

As a master YouTube content creator, develop an engaging script that revolves around the theme of "Exploring Ancient Ruins."

Your script should encompass exciting discoveries, historical insights, and a sense of adventure.

Include a mix of on-screen narration, engaging visuals, and possibly interactions with co-hosts or experts.

The script should ideally result in a video of around 10-15 minutes, providing viewers with a captivating journey through the secrets of the past.

Example:

"Welcome back, fellow history enthusiasts, to our channel! Today, we embark on a thrilling expedition..."

-----

Now, improve the prompt.

IMPROVED PROMPT:
"""

make_prompt_v2="""
Your goal is to improve the prompt given below for {task} :
--------------------

Prompt: {lazy_prompt}

--------------------

Here are several tips on writing great prompts:

-------

Start the prompt by stating that it is an expert in the subject.

Put instructions at the beginning of the prompt and use ### or to separate the instruction and context 

Be specific, descriptive and as detailed as possible about the desired context, outcome, length, format, style, etc 

---------

Here's an example of a great prompt:

As a master YouTube content creator, develop an engaging script that revolves around the theme of "Exploring Ancient Ruins."

Your script should encompass exciting discoveries, historical insights, and a sense of adventure.

Include a mix of on-screen narration, engaging visuals, and possibly interactions with co-hosts or experts.

The script should ideally result in a video of around 10-15 minutes, providing viewers with a captivating journey through the secrets of the past.

Example:

"Welcome back, fellow history enthusiasts, to our channel! Today, we embark on a thrilling expedition..."

-----

Now, improve the prompt.

IMPROVED PROMPT:

"""

prompt_improver = """
You are an expert Prompt Writer for Large Language Models.

Your goal is to improve the prompt given below:
--------------------

{text}

--------------------

Here are several tips on writing great prompts:

-------

Start the prompt by stating that it is an expert in the subject.

Put instructions at the beginning of the prompt and use ### or to separate the instruction and context 

Be specific, descriptive and as detailed as possible about the desired context, outcome, length, format, style, etc 
---------
Here's an example of a great prompt:

As a certified nutritionist, create a 7-day meal plan for a vegan athlete. 

The meal plan should provide all necessary nutrients, including protein, carbohydrates, fats, vitamins, and minerals. 

Each day should include breakfast, lunch, dinner, and two snacks. 

Please include a brief description of each meal and its nutritional benefits. 

The output should be in a daily format, with each meal detailed. 

Example:

Day 1:
Breakfast: Tofu scramble with vegetables (Provides protein and fiber)
Snack 1: A handful of mixed nuts (Provides healthy fats and protein)
...


Now, improve the prompt below:

IMPROVE PROMPT:

"""