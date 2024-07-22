from enum import Enum
from Player import Player
from Maze import Maze

class GameLoop:
    def __init__(self, player: Player, maze: Maze) -> None:
        """Constructor for GameLoop

        Args:
            player (Player): player playing the game
            maze (Maze): maze generated for the game
        """
        self.player: Player = player
        self.maze: Maze = maze
    
    def draw_maze(self) -> None:
        """Draws the player on the maze
        """
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

    def loop(self) -> None:
        """Main game loop function
        """
        while True:
            self.draw_maze()
            action = input("take action $> ").upper()

            if action =='UP':
                self.player.move_up()
            elif action == 'RIGHT':
                self.player.move_right()
            elif action =='DOWN':
                self.player.move_down()
            elif action =='LEFT':
                self.player.move_left()
            elif action =='BOMB':
                self.player.use_bomb()
            else:
                print('Invalid action')
            print(f'move player to: ({self.player.x}, {self.player.y})')

            self.player.touching_coin()

            if self.player.all_coins_collected():
                print("All coins collected")
                break


if __name__ == '__main__':
    maze: Maze = Maze(9, 1)
    player: Player = Player(0, 0, maze)
    gameloop: GameLoop = GameLoop(player, maze)
    gameloop.loop()
