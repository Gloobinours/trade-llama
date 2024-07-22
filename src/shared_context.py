from Maze import Maze
from Player import Player
from Game import GameLoop

game_loop_instance = None

def create_game_loop(maze_size=21):
    global game_loop_instance

    maze = Maze(maze_size, 1)
    player = Player(0, 0, maze)
    game_loop_instance = GameLoop(player, maze)
