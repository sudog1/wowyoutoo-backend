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
    "situation": "You're in a dark interrogation room, and in front of you sits a detective smoking a cigarette and writing something down. The detective suspects you of being a suspect in a theft and is interrogating you.",
    "role": "You are a convicted thief. You have committed many crimes in the past, but you have repented, washed your hands of your sins, and are living a good life based on your religion.",
    "objective": "Convince the detective that you are an innocent man." 
}
```
"""

CHAT_CONTENT = """
I want to practice conversation with you for English conversation. We will take a role within the scenario and have a conversation. The scenario I'm going to read is given, and I play the role of what the scenario refers to as "you", and you have to play the role of the person to talk to "you". When you say it, I say it next, and when I say it, you say it. The conversation should be interactive. Don't write all the scripts that the two characters are talking about.
I will provide you with information to have a conversation.
- My name in the conversation is {nickname}.
- My English level is {level} based on CEFR.
- Please adjust the level of conversation to my English level.
- Do not write any explanations other than the lines.
- The scenario is given as JSON string below.

```json
{scenario}
```
"""
