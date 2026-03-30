import json
import os

Q_PATH = "data/q_table.json"


def load_q():
    if os.path.exists(Q_PATH):
        with open(Q_PATH, "r") as f:
            return json.load(f)
    return {}


def save_q(q):
    with open(Q_PATH, "w") as f:
        json.dump(q, f)


def update_q(state, reward):

    q = load_q()

    if state not in q:
        q[state] = 0

    # 🔥 簡單強化學習
    q[state] = q[state] + 0.1 * (reward - q[state])

    save_q(q)

    return q[state]
