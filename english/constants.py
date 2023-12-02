CONTENT = """
I want to test my reading comprehension skills.
Follow these steps to create a reading comprehension quiz.
My CEFR level is B1. Please create it appropriately for my level.

Step 1. Choose a random topic
Choose a random topic from a variety of fields. You need to generate the topics randomly.
For example, there are the following topics In addition to these, please create appropriate topics.

- The Evolution of Wearable Health Devices
- The Intersection of Psychology and Architecture
- The Psychological Impact of Color in Marketing
- Sustainable Tourism Initiatives in Developing Countries
- The Role of Robotics in Agricultural Sustainability
- The Ethical Dimensions of Genetic Editing in Livestock
- Virtual Reality's Influence on Memory Retention
- The Rise of Emotional Intelligence Apps
- The Socioeconomic Impact of AI Automation in Manufacturing
- The Future of Renewable Energy in Aviation
- The Intersection of Neuroscience and Marketing Strategies
- Sustainable Innovations in Urban Transportation
- The Impact of Biophilic Design on Workplace Productivity
- AI-Powered Tutoring Systems in Education
- The Ethics of Personal Data Monetization
- Cognitive Effects of Bilingualism on the Brain
- The Role of Blockchain in Supply Chain Transparency
- The Psychological Effects of Environmental Destruction
- Sustainable Innovations in Textile Recycling
- The Ethics of AI in Personalized Advertising
- The Influence of Cultural Heritage on Technological Innovations
- The Intersection of Sociology and AI Ethics
- The Role of Gaming in Social Skills Development
- The Psychological Impact of Space Exploration Ambitions
- Sustainable Agriculture Practices in Arid Regions
- AI Applications in Wildlife Migration Tracking
- The Ethics of Brain-Computer Interfaces in Gaming
- The Societal Impact of Renewable Energy Job Creation
- The Psychological Benefits of Nature-Inspired Architecture
- The Role of AI in Humanitarian Aid Distribution
- The Impact of Big Data on Healthcare Accessibility
- Sustainable Innovations in Marine Conservation
- The Ethics of AI-Powered Drug Discovery
- The Psychological Effects of Long-Term Space Travel
- The Intersection of Indigenous Wisdom and Modern Technology
- The Role of Virtual Reality in Environmental Education
- The Impact of Social Media Algorithms on Information Bias
- Sustainable Practices in Urban Waste Management
- The Ethical Implications of AI in Sentencing Systems
- The Psychological Influence of Soundscapes in Urban Planning
- AI Solutions for Mental Health Crisis Intervention
- The Evolution of Ethical Considerations in Robotics
- The Socioeconomic Impact of AI-Based Job Displacement
- The Psychological Impact of Smart Home Technology
- Sustainable Innovations in Forestry and Timber Production
- The Ethical Considerations of AI-Powered Content Creation
- The Societal Impact of Renewable Energy Accessibility
- The Psychological Impact of Climate Change Displacement
- Sustainable Urban Water Management Strategies
- The Intersection of AI and Environmental Conservation

Step 2. Write a title and paragraph
Write a short paragraph based on the topic you've chosen. You'll also need to write a suitable title for your paragraph.
 
Step 3. Design question and multiple choice options
Create comprehension question and multiple choice options based on the content of the passage. You should include one choice that matches the content and three distractors to test comprehension. The four options must be in order in the list.

Step 4. Write solution and explanation
Indicate which of the choices is the solution with a 0-based index. You'll need to write a explanation about it. 

Here's a good example
```
- "title": "The Discovery of Exoplanets",
- "paragraph": "In recent decades, advancements in technology have revolutionized our understanding of the universe. One of the most significant breakthroughs has been the discovery of exoplanets. Exoplanets, or extrasolar planets, are planets that orbit stars outside our solar system. The methods employed to detect these distant worlds include the transit method, radial velocity, and direct imaging. The identification of exoplanets has expanded our comprehension of planetary systems and the potential for extraterrestrial life.",
- "question": "How are exoplanets discovered?",
- "options": ["A) By studying the atmosphere of neighboring planets.", "B) Through the observation of gravitational waves.", "C) Via methods like the transit method, radial velocity, and direct imaging.", "D) By analyzing the surface composition of distant celestial bodies."],
- "solution": 2,
- "explanation": "Exoplanets are discovered through various methods like the transit method, which observes a planet passing in front of its star, causing a slight dimming of the star's light; radial velocity, which detects the gravitational tug of an orbiting planet on its star; and direct imaging, capturing actual images of the exoplanets. Options A and D are incorrect as they describe methods that are not primarily used for discovering exoplanets. Option B refers to a different phenomenon unrelated to exoplanet detection."
```
The results should be generated in JSON format. 
"""

READING_QUIZ_COUNT = 10

CORRECT_WORDS_COUNT = 10
WRONG_WORDS_PER_QUIZ = 3

READING_COST = 1
