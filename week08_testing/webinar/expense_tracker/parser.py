def parse_command(text):
    parts = text.split()
    command = parts[0]
    if command == "add":
        return command, float(parts[1]), parts[2]
    if command in ("total", "stats", "quit"):
        return command, None, None
    raise ValueError("unknown command")
