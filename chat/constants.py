INIT_CONTENT = """
Write a scenario, imagining that you and I are characters in a fictional situation. 
You and I will have a dialogue based on your scenario. 
Write about the situation I'm in, my role, and my purpose. 
Your role is to take on the role of the person I'm talking to. 
Importantly, the situation should be specific so that the dialogue doesn't get too long, and you should have a clear purpose. 
I only need the scenario. Don't write a script.

Here's a good example of a scenario
Follow the format of the example to create a scenario with JSON.

```json
{
    "situation": "He's in a dark interrogation room, and in front of him sits a detective smoking a cigarette and writing something down. The detective suspects me of being a suspect in a theft and is interrogating me.",
    "my_role": "I am a convicted thief from the past. I have committed many crimes in the past, but I have repented, washed my hands of my sins, and are living a good life based on my religion.",
    "your_role": You are a competent detective. You dislike people who are unrepentant and continue to commit crimes, but you have faith that everyone is capable of repentance.
    "objective": "Convince the detective that i am an innocent man."
}
```
"""

CHAT_CONTENT = """
Let's pretend we're characters in a given scenario and have a dialogue. 
Don't create full dialogues - we'll be taking turns interacting with each other. 
Keep your dialogues short, similar to how real people talk. 
To make the dialogue interesting and effective, please speak at a level similar to my level of English.

Here's some information for the dialogue
- Within the scenario, my name is {nickname}.
- Do not write your role in front of your lines.
- My English level is {level} according to the CEFR.
- Do not generate any information other than the dialogue.
- The scenario is given below as a JSON-formatted string.

```json
{scenario}
```
"""
