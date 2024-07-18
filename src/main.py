from Maze import Maze

def main() -> None:
    maze: Maze = Maze(20, 2)
    print(maze.generate_matrix())
    
if __name__ == "__main__":
    main()