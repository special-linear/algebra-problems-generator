import sys


class UpdatesHandler:
    def __init__(self):
        self.listeners = []

    def add_listener(self, message_handler):
        self.listeners.append(message_handler)

    def push(self, message):
        for message_handler in self.listeners:
            message_handler(message)


class ConsoleUpdatesHandler(UpdatesHandler):
    def __init__(self):
        super().__init__()

        def console_updates_print(message):
            sys.stdout.write('\r{}'.format(message))
            sys.stdout.flush()

        self.add_listener(console_updates_print)
