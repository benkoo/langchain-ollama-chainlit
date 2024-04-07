import json
import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider

async def load_settings_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data['settings']

@cl.on_chat_start
async def start():
    settings_config = await load_settings_from_file('src/settings.json')
    settings_objects = []
    for item in settings_config:
        item_type = item['type'].lower()  # Ensure type is in lowercase
        if item_type == 'select':
            settings_objects.append(Select(**item))
        elif item_type == 'switch':
            settings_objects.append(Switch(**item))
        elif item_type == 'slider':
            settings_objects.append(Slider(**item))
    settings = await cl.ChatSettings(settings_objects).send()

@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)