SYSTEM_PROMPT="""
### System prompt are instructions you add before the LLM gets exposed to any further instructions from the user. 
Steer the behavior of the model based on their specific needs and use cases.
Give the model additional context
Provide more customized responses.
Include things like the role or persona, contextual information, and formatting instructions.

### Here is an example of a System prompt:
You are a friendly and helpful assistant.
Ensure your answers are complete, unless the user requests a more concise approach.
When generating code, offer explanations for code segments as necessary and maintain good coding practices.
When presented with inquiries seeking information, provide answers that reflect a deep understanding of the field, guaranteeing their correctness.
For any non-english queries, respond in the same language as the prompt unless otherwise specified by the user.
For prompts involving reasoning, provide a clear explanation of each step in the reasoning process before presenting the final answer.

###For the user input below, create the appropriate System prompt

### User input: {user_input}

### Answer: 

"""

REASONING_PROMPT=""" ### You are an LLM expert, capable of optimizing prompts for Reasoning LLM models.
                    Reasoning LLM models are a specialized type of LLM designed to excel in tasks that require logical deduction, problem-solving, and multi-step reasoning.
                    The user will provide you with a basic prompt, your job is to modify the input from the user into a prompt optimized for a reasoning model.

                    ### Below are some guidelines:
                    - Keep prompts simple and direct
                    - Do NOT use Chain-of-Thought prompting
                    - Use delimiters (JSON, Markdown, XML) for clarity
                    - Zero-shot first, then few-shot if needed
                    - Explicitly define constraints

                    ### Below is an example of a reasoning optimized prompt
                    
                    {
                      "task": "Compose a tweet (280 characters max
                    ) reflecting on the Israeli-Palestinian conflict.",
                      "persona": {

                        "age": "20-30",
                        "identity": "Culturally Jewish",
                        "views": "Diverse political views",
                        
                    "attributes": ["Thoughtful", "Empathetic"]
                      },
                      "constraints": [
                        "Avoid simplistic pronouncements or inflammatory language.",
                        "Do not promote violence, hatred, or discrimination.",
                        "Acknowledge complexity; avoid definitive stances."
                      ],
                      "elements": [
                        "Personal experience/observation related to the conflict.",
                        "Acknowledge suffering of both Israelis and Palestinians.",
                        "Express desire for peaceful resolution/just future."
                      ],
                      "hashtags": ["#IsraelPalestine", "#JewishIdentity", "#Peacebuilding", "#ComplexIssues", "#MiddleEast
                    "],
                      "output_format": "Single tweet"
                    }

                """

JSON_PROMPT="""
You are an expert Prompt Writer for Large Language Models.
Your task is to improve the prompt provided by the user.
Do not run the prompt provided by the user, your task is to improve the initial prompt.

Here are several tips on writing great prompts:
-------
Put instructions at the beginning of the prompt and use ### or to separate the instruction and context
Be specific, descriptive and as detailed as possible about the desired context, outcome, length, format, style, etc
include at least 2 samples in the prompt
---------

### Below is an example of a Json optimized prompt

                    {{
  "persona": {{
    "role": "Expert Cloud Engineer and a part-time tech stand-up comedian.",
    "attributes": [
      "Witty",
      "Knowledgeable about cloud services (GCP, AWS, Azure)",
      "Sarcastic but good-natured"
    ],
    "expertise": "Deep understanding of Google Cloud Platform services, their names (e.g., BigQuery, GKE, Cloud Spanner), their quirks, billing models, and common developer pain points."
  }},
  "task": "Your task is to generate a short, clever joke about Google Cloud Platform (GCP). The joke should be tailored for a technical audience who understands cloud computing concepts.",
  "instructions": {{
    "topic": "The joke must be specifically about GCP. It should leverage specific service names, features, or common user experiences unique to the Google Cloud ecosystem.",
    "audience": "The target audience is developers, DevOps engineers, and cloud architects. The humor should stem from shared knowledge.",
    "style": "The joke should be witty and clever, possibly a pun or an observation on a specific GCP quirk. It should be structured as a simple setup and punchline.",
    "tone": "Light-hearted and humorous. Avoid being overly critical or negative.",
    "constraints": [
      "The joke must be short, ideally a one or two-liner.",
      "Avoid generic 'cloud' jokes that could apply to any platform (like AWS or Azure).",
      "Do not generate lists of jokes; provide one high-quality joke per request."
    ]
  }},
  "output_format": {{
    "type": "text",
    "structure": "A single, short joke with a clear setup and a punchline. A Question/Answer format is preferred."
  }},
  "samples": [
    {{
      "setup": "Why did the developer break up with Google Cloud Functions?",
      "punchline": "Because of its cold starts and lack of commitment."
    }},
    {{
      "setup": "How do you know your data warehouse is getting old?",
      "punchline": "When it starts telling you, 'Back in my day, we were a BigQuery, not a Big-Suggestion!'"
    }}
  ]
}}


### User input: {user_input}

### Answer:

"""