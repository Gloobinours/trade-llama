from flask import Flask
from flask_restful import Resource, Api
from api.endpoints import *
from flask_cors import CORS
from shared_context import create_game_loop, game_loop_instance

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(MazeEndpoint, '/maze/<int:maze_size>')

if __name__ == "__name__":
    app.run(debug=True)