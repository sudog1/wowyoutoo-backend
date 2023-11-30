CONTENT = """
I want to test my reading comprehension skills.
Follow these steps to create a reading comprehension quiz.
My CEFR level is {0}. Please create it appropriately for my level.

Step 1. Choose a random topic
Choose a random topic from a variety of fields. For example, here are some possible topics, but there are others as well. You need to generate the topics randomly.

- Scientific Facts: A brief explanation about a recent scientific discovery or phenomenon.
- Historical Events: A short description of a significant historical event or figure.
- Cultural Issues: A concise introduction to a cultural aspect like art, music, or cinema.
- Social Problems: A brief overview of a societal issue that impacts mainstream culture.
- Natural Phenomena: A simple explanation of an intriguing natural occurrence.

Step 2. Write a title and paragraph
Write a short paragraph based on the topic you've chosen. You'll also need to write a suitable title for your paragraph.

Step 3. Design question and multiple choice options
Create comprehension question and multiple choice options based on the content of the passage. You should include one choice that matches the content and three distractors to test comprehension. The four options must be in order in the list.

Step 4. Write solution and explanation
Indicate which of the choices is the solution with a 0-based index. You'll need to write a explanation about it. 

The results should be generated in JSON format. Here's a good example

```json
{
    "title": "The Discovery of Exoplanets",
    "paragraph": "In recent decades, advancements in technology have revolutionized our understanding of the universe. One of the most significant breakthroughs has been the discovery of exoplanets. Exoplanets, or extrasolar planets, are planets that orbit stars outside our solar system. The methods employed to detect these distant worlds include the transit method, radial velocity, and direct imaging. The identification of exoplanets has expanded our comprehension of planetary systems and the potential for extraterrestrial life.",
    "question": "How are exoplanets discovered?",
    "options": ["A) By studying the atmosphere of neighboring planets.", "B) Through the observation of gravitational waves.", "C) Via methods like the transit method, radial velocity, and direct imaging.", "D) By analyzing the surface composition of distant celestial bodies."],
    "solution": 2,
    "explanation": "Exoplanets are discovered through various methods like the transit method, which observes a planet passing in front of its star, causing a slight dimming of the star's light; radial velocity, which detects the gravitational tug of an orbiting planet on its star; and direct imaging, capturing actual images of the exoplanets. Options A and D are incorrect as they describe methods that are not primarily used for discovering exoplanets. Option B refers to a different phenomenon unrelated to exoplanet detection."
}
```
"""

READING_QUIZ_COUNT = 10

CORRECT_WORDS_COUNT = 10
WRONG_WORDS_PER_QUIZ = 3
