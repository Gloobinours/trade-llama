from enum import Enum
from Player import Player
from Maze import Maze

class ActionState(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class GameLoop:
    def __init__(self, player: Player, maze: Maze) -> None:
        self.player: Player = player
        self.maze: Maze = maze
    
    def draw_maze(self):
        new_maze = []
        for x in range(self.maze.size):
            row = []
            for y in range(self.maze.size):
                if x == self.player.x and y == self.player.y:
                    row.append('#')
                else:
                    row.append(str(self.maze.grid[x][y].state.value))
            new_maze.append(row)
        
        for row in new_maze:
            print(' '.join(row))

    def loop(self):
        while True:
            self.draw_maze()
            action = input("take action $> ").upper()

            match action:
                case action if action in [ActionState.UP.value, 'UP']:
                    self.player.move_up()
                case action if action in [ActionState.RIGHT.value, 'RIGHT']:
                    self.player.move_right()
                case action if action in [ActionState.DOWN.value, 'DOWN']:
                    self.player.move_down()
                case action if action in [ActionState.LEFT.value, 'LEFT']:
                    self.player.move_left()
                case _:
                    print('Invalid action')
            print(f'move player to: ({self.player.x}, {self.player.y})')

            self.player.all_coins_collected()
            self.player.touching_coin()
            self.player.touching_bomb()


if __name__ == '__main__':
    maze: Maze = Maze(31, 1, 2)
    player: Player = Player(0, 0, maze)
    gameloop: GameLoop = GameLoop(player, maze)
    gameloop.loop()
