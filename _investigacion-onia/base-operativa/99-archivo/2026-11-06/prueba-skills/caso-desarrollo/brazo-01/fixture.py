def select_latest(events):
    if not events:
        return None
    events.sort(key=lambda item: str(item["seq"]))
    return events[-1]

