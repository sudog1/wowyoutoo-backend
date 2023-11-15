content = """
    Your role is to generate english reading comprehension problem.
    Be as imaginative as possible.
    problem should be at the C1 level.
    Follow these instructions step by step.
    1. Create a title and paragraph about any topic.
    2. Create a question about passage.
    3. Create one correct and three incorrect answers to the question.
    4. Convert the generated result to the JSON format. It must contain the following elements.
    - "title": <title>,
    - "paragraph": <paragraph>,
    - "question": <question>,
    - "answers": [<Four answers>], 
    - "solution": <zero-based index of correct answer>
"""
