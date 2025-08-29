# FILE: utils.py
def seconds_to_minsec(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f"{m}:{s:02d}"
