from flask_restful import Resource
from flask import jsonify
import sys
sys.path.insert(0, '../')
from Maze import Maze
import shared_context

class MazeEndpoint(Resource):

    def get(self, maze_size):
        shared_context.create_game_loop(maze_size)

        maze = shared_context.game_loop_instance.maze
        mtx = []
        for x in range(maze_size):
            mtx.append([])
            for y in range(maze_size):
                mtx[x].append(maze.grid[x][y].state.value)

        return jsonify(matrix=mtx)