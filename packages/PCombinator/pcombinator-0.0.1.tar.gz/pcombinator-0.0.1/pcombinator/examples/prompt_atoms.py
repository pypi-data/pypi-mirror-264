from pcombinator.combinators.one_of_combinator import OneOfCombinator

# TODO:
# 1. Switch to FixedStringCombinator in all cases
# 2. Separate the single items from the combinator to allow reuse
# 3. Consider how to persist and load for reuse - libraries of combinators?

# TODO:
# Format for storing combinations in a user editable way.
# Need to store type, ID and children, where children can be strings or references to other combinators.
# On load, take the strings into FixedStringCombinator such that there's an id for each string.
# Load into combinators; Save from combinators tree.
# Registry module.
# Ability to load the combinators or print the file from actual combinations of IdTree.
# Consider - ability to adjust probabilities following feedback (need to replace combinators in this case)

role = OneOfCombinator(
    id="default_role",
    children=[
        "You're an expert on the subject.",
        "You're an enthusiastic expert on the subject."
        "You're a friendly advisor on the subject.",
        "You're an AI assistant that considers the problem carefully and gives a thoughtful answer. Be forthcoming about any uncertaity or unknowns.",
        "You're name is Bob.",
    ],
)

# TODO: Separate the role as well into level, domain, approach, etc.


audience = OneOfCombinator(
    id="default_audience",
    children=[
        "Your audience is a beginner.",
        "Your answer should assume a beginner level user.",
        "Explain on the level of a beginner level user.",
    ],
)

tip = OneOfCombinator(
    id="default_tip",
    children=[
        "I'll tip you $5 if you do a good job.",
        "I'll tip you $10 if you do a good job.",
        "I'll tip you $20000 if you do a good job.",
    ],
)

task = OneOfCombinator(
    id="default_task",
    children=[
        "Your task is to give an overview of the subject and answer the question with the relevant context."
        "Your task is to explain the subject in a way that is easy to understand.",
    ],
)

cot = OneOfCombinator(
    id="default_cot",
    children=[
        "Think step by step and first make a list of steps.",
        "First print all the assumptions you're taking and only then give the answer.",
        "List your assumptions, provide the answer and then explain why you think the answer is correct.",
        "List your assumptions, reasoning steps, and finally an answer consistent with those.",
    ],
)

primers = OneOfCombinator(
    id="default_primers",
    children=[
        "First, let's go through some basic concepts."
        "Sure! Let's start with some basic concepts.",
        "Let me rephrase what you're asking to make sure I understand.",
        "Gladly!",
    ],
)

instructions = OneOfCombinator(
    id="default_instructions",
    children=[
        "First, go through some basic concepts. Then, describe the problem and your approach to solving it. Finally, give the answer.",
        "For each assumption, quote the text from the user prompt that supports it.",
        "Do not assume any prior knowledge on the part of the user.",
        "Keep the answer short",
        "Make sure the answer is exhaustive.",
    ],
)

output_format = OneOfCombinator(
    id="default_output_format",
    children=[
        "The output should be a single paragraph.",
        "Use only JSON in the output, do not include any other text before or after."
        "Use only JSON in the output, do not include any other text before or after. The following JSON schema describes the desired output:",
    ],
)

shape_of_good_answer = OneOfCombinator(
    id="default_shape_of_good_answer",
    children=[
        "A good answer is one that is easy to understand and is correct.",
        "A good answer is one that is easy to understand and is correct. It should also be exhaustive.",
    ],
)

tone = OneOfCombinator(
    id="default_tone",
    children=[
        "Be friendly and professional.",
        "Be concise and supportive.",
    ],
)

few_shot = OneOfCombinator(
    id="default_few_shot",
    children=[],
)

template = jinja2.Template(
    """
{{role}}
{{audience}}
{{tip}}
"""
)
