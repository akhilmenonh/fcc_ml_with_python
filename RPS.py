# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

'''
def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)

    guess = "R"
    if len(opponent_history) > 2:
        guess = opponent_history[-2]

    return guess
'''

import itertools, random

def init_model(order=1):
    def gen_keys(n):
        keys = ['R', 'P', 'S']
        for _ in range(n * 2 - 1):
            keys = [''.join(k) for k in itertools.product(keys, 'RPS')]
        return keys

    keys = gen_keys(order)
    return {
        k: {m: {'p': 1/3, 'n': 0} for m in 'RPS'}
        for k in keys
    }

def update_model(model, key, move, decay=0.9):
    for m in model[key]:
        model[key][m]['n'] *= decay
    model[key][move]['n'] += 1
    total = sum(model[key][m]['n'] for m in 'RPS')
    for m in 'RPS':
        model[key][m]['p'] = model[key][m]['n'] / total

def predict_move(model, key):
    dist = model[key]
    probs = [dist[m]['p'] for m in 'RPS']
    if max(probs) == min(probs):
        return random.choice('RPS')
    return 'RPS'[probs.index(max(probs))]

counter = {'R': 'P', 'P': 'S', 'S': 'R'}
model = init_model()
last_seq, prev_seq = '', ''
ai_move = ''

def player(prev):
    global last_seq, prev_seq, ai_move, model
    if not prev:
        reset()
    prev_seq, last_seq = last_seq, ai_move + prev
    if prev_seq:
        update_model(model, prev_seq, prev)
        ai_move = counter[predict_move(model, last_seq)]
    else:
        ai_move = random.choice('RPS')
    return ai_move

def reset():
    global model, last_seq, prev_seq, ai_move
    model = init_model()
    last_seq = prev_seq = ai_move = ''
