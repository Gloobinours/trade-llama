from Maze import Maze

def main() -> None:
    maze: Maze = Maze(16)
    print(maze.generateMaze())
    
if __name__ == "__main__":
    main()