import json
import os
import random
import bottle

from app.api import ping_response, start_response, move_response, end_response
from app.model import Game


@bottle.route("/")
def index():
    return """
    Snecko!
    """


@bottle.route("/static/<path:path>")
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.
    """
    return bottle.static_file(path, root="static/")


@bottle.post("/ping")
def ping():
    """
    A keep-alive endpoint.
    """
    return ping_response()


@bottle.post("/start")
def start():
    data = bottle.request.json
    print(json.dumps(data))
    color = "#AA2288"

    return start_response(color)


@bottle.post("/move")
def move():
    data = bottle.request.json
    game = Game(data)
    return move_response(game.naive_move())


@bottle.post("/end")
def end():
    data = bottle.request.json
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )
