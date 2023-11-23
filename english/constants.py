CONTENT = """
    Your role is to generate english reading comprehension test.
    Be as imaginative as possible.
    Test should be at the C1 level.
    Follow these instructions step by step.
    1. Create a title and paragraph about any topic.
    2. Create a multiple choice question about paragraph.
    3. Create one correct answer and three incorrect answers with labels. Each answer is formatted as follows "a) answer"
    4. Create an explanation for the correct answer.
    5. Convert the generated result to the strict JSON format. It must contain the following elements.
    - "title": <title>,
    - "paragraph": <paragraph>,
    - "question": <question>,
    - "answers": [<four answers>], 
    - "solution": <zero-based index of correct answer>
    - "explanation": <explanation>
"""

READING_QUIZ_COUNT = 10

CORRECT_WORDS_COUNT = 10
WRONG_WORDS_PER_QUIZ = 3
