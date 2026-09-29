"""地震监测站核心逻辑：传感器、巡检、数据和校准。"""

import json


def new_game():
    return {
        "sensors": {},
        "data": {},
        "storage_capacity": 100,
        "calibrated": {},
        "day": 1,
        "seq": ["calm", "aftershock", "quake"],
        "idx": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    return state


def calibrate(state, sensor_id):
    if state["calibrated"].get(sensor_id):
        return False
    state["sensors"][sensor_id] = True
    state["calibrated"][sensor_id] = True
    return True


def inspect(state, sensor_id, size):
    if state.get("storm"):
        return False
    state["data"][sensor_id] = size
    return True


def capacity(state):
    return sum(state["data"].values())


def cancel(state, sensor_id):
    state.setdefault("windows", {})[sensor_id] = "open"
    return True


def record(state, sensor_id, size):
    if state.get("fault"):
        return False
    state["data"][sensor_id] = size
    return True


def next_event(state):
    event = state["seq"][state["idx"] % len(state["seq"])]
    state["idx"] += 1
    return event


def main():
    print("地震监测站 - 命令: calibrate/inspect/capacity/cancel/record/event/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
