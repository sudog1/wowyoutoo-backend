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
the following scenario is written from your perspective. In other words, “You” in the scenario refers to me. 
You take on the role of the person I am talking to. my name is {0}. My CEFR level is {1}.
Let's start a dialogue appropriately for my level to improve my conversation skills.
the dialogue is based on the scenario.
the scenario are provided as strings in JSON format.

```json
{2}
```
"""
