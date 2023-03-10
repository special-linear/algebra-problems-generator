import sys

from flask import Flask, render_template, request
from flask_sock import Sock
from os.path import abspath
from collections import defaultdict
import json
import asyncio
import threading
from multiprocessing import Process, Queue
from queue import Empty

import generator
from updates_handler import UpdatesHandler, ConsoleUpdatesHandler

templates_path = abspath('web')
static_path = abspath('web/static')
app = Flask(__name__, template_folder=templates_path, static_folder=static_path)
sock = Sock()
sock.init_app(app)


updates_handlers = defaultdict(ConsoleUpdatesHandler)


@app.route("/")
def index():
    return render_template('web.html', problem_types=generator.problem_types)


def generate_process(problem_types, variants, messages: Queue):
    def messages_to_queue(message):
        messages.put({'type': 'update', 'message': message})
    updates_handler = ConsoleUpdatesHandler()
    updates_handler.add_listener(messages_to_queue)
    problems = generator.construct_problems(problem_types, variants, updates_handler=updates_handler)
    messages.put({'type': 'output', 'message': generator.render_problems(problems, variants)})


@sock.route("/generator")
def generator_aaa(ws):
    finished = False
    proc = None
    messages = Queue()
    while not finished:
        input_message = ws.receive(0.1)
        if input_message is not None:
            data = json.loads(input_message)
            if data['request'] == 'generate':
                variants = data['variants']
                problem_types = [generator.problems_classes[ptn] for ptn in data['problems']]
                proc = Process(target=generate_process, args=(problem_types, variants, messages))
                proc.start()
            elif data['request'] == 'stop':
                if isinstance(proc, Process):
                    proc.terminate()
                    proc = None
                    finished = True
        if isinstance(proc, Process):
            while proc.is_alive():
                try:
                    message = messages.get(block=False, timeout=1)
                    ws.send(json.dumps(message))
                    if message['type'] == 'output':
                        finished = True
                        break
                except Empty:
                    break




@app.route("/generate", methods=['POST', 'GET'])
def generate():
    request_json = request.get_json()
    request_id = request_json['request_id']
    updates_handler = updates_handlers[request_id]
    variants = request_json['variants']
    problem_types = [generator.problems_classes[ptn] for ptn in request_json['problems']]
    problems = generator.construct_problems(problem_types, variants, updates_handler)
    del updates_handlers[request_id]
    return generator.render_problems(problems, variants)


@sock.route("/updates/<string:request_id>")
def updates(ws, request_id):
    updates_handlers[request_id].add_listener(ws.send)
    while True:
        data = ws.receive()
    # data = ws.receive()
    # ws.send(data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
