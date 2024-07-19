let mazeData = null;
let maze_size = 60;

// Function to fetch maze data from the server
function get_maze(size) {
    if (mazeData) {
        // If maze data is already fetched, return it directly
        return Promise.resolve(mazeData);
    }

    return fetch(`http://127.0.0.1:5000/maze/${size}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // Return the parsed JSON data
        })
        .then(data => {
            console.log('Fetched maze data:', data); // Log fetched data for debugging
            if (!data || !data.matrix || data.matrix.length === 0) {
                throw new Error('Fetched maze data is empty or invalid');
            }
            mazeData = data.matrix; // Save maze matrix array in mazeData variable
            return mazeData;
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            throw error; // Re-throw the error to propagate it
        });
}


// Function to draw the maze on the canvas
function drawMaze(mazeArray) {
    // Maze cell dimensions and colors
    const cellSize = 15; // Size of each cell in pixels
    const wallColor = '#333'; // Color for walls
    const pathColor = '#fff'; // Color for paths
    const coinColor = '#aa0'

    // Get the canvas element and its context
    const canvas = document.getElementById('mazeCanvas');
    const ctx = canvas.getContext('2d');

    // Calculate the canvas dimensions based on the maze size
    const mazeWidth = mazeArray[0].length;
    const mazeHeight = mazeArray.length;
    canvas.width = mazeWidth * cellSize;
    canvas.height = mazeHeight * cellSize;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Iterate through the mazeArray and draw walls and paths
    for (let y = 0; y < mazeHeight; y++) {
        for (let x = 0; x < mazeWidth; x++) {
            if (mazeArray[y][x] === 1) {
                // set color to wall
                ctx.fillStyle = wallColor;
            } else if(mazeArray[y][x] === 0){
                // set color to path
                ctx.fillStyle = pathColor;
            } else if(mazeArray[y][x] === 2) {
                // set color to coin
                ctx.fillStyle = coinColor;
            }
            // Draw cell
            ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
        }
    }
}
