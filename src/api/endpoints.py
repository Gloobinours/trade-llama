from flask_restful import Resource
from flask import request, jsonify
import json
import sys
sys.path.insert(0, '../')
from Maze import Maze

class MazeEndpoint(Resource):

    def get(self, maze_size):
        maze: Maze = Maze(maze_size, 3)
        mtx = maze.maze_mtx.tolist()
        return jsonify(matrix=mtx)