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
    if state.get("calibrated", {}).get(sensor_id):
        return False
    state["calibrated"][sensor_id] = True
    return True


def inspect(state, sensor_id, size):
    if state.get("storm"):
        return False
    state["data"][sensor_id] = size
    return True


def capacity(state):
    return sum(state.get("data", {}).values())


def cancel(state, sensor_id):
    windows = state.setdefault("windows", {})
    windows[sensor_id] = "open"
    return True


def record(state, sensor_id, size):
    if state.get("fault"):
        return False
    state["data"][sensor_id] = size
    return True


def next_event(state):
    event = state["seq"][state["idx"]]
    state["idx"] = (state["idx"] + 1) % len(state["seq"])
    return event


def main():
    print("地震监测站 - 命令: calibrate/inspect/capacity/cancel/record/event/quit")
    state = new_game()
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        parts = raw.split()
        command, args = parts[0], parts[1:]
        if command == "calibrate" and len(args) == 1:
            print(calibrate(state, args[0]))
        elif command == "inspect" and len(args) == 2:
            print(inspect(state, args[0], int(args[1])))
        elif command == "capacity":
            print(capacity(state))
        elif command == "cancel" and len(args) == 1:
            print(cancel(state, args[0]))
        elif command == "record" and len(args) == 2:
            print(record(state, args[0], int(args[1])))
        elif command == "event":
            print(next_event(state))
        else:
            print("unknown command")


if __name__ == "__main__":
    main()
