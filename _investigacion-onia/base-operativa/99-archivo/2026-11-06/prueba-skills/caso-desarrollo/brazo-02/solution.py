def select_latest(events):
    latest = None
    for event in events:
        if latest is None or event["seq"] >= latest["seq"]:
            latest = event
    return latest
