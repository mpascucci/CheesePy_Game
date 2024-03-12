from . import config

message_buffer = ''


def add(message, sep=' '):
    """Add message to the buffer"""
    global message_buffer
    message_buffer += sep + str(message)


def flush():
    """emty the buffer"""
    global message_buffer
    message_buffer = ''


def print_buffer():
    global message_buffer
    """Print and empty the buffer"""
    say(f">>> {message_buffer}")
    flush()


def say(message):
    """Print"""
    if config.verbose:
        global message_buffer
        print(f">>> {message}")
