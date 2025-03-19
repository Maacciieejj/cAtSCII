import json
import os

def get_switch_state():
    try:
        with open('switch_state.json', 'r') as f:
            return json.load(f)['przelacznik1']
    except:
        return False

def set_switch_state(state):
    with open('switch_state.json', 'w') as f:
        json.dump({'przelacznik1': state}, f)

# Inicjalizacja stanu
if not os.path.exists('switch_state.json'):
    set_switch_state(False)

przelacznik1 = get_switch_state()