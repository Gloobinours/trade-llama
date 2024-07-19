// Connect to the WebSocket server
const socket = new WebSocket('ws://127.0.0.1:5005');

// Event listener for when the connection opens
socket.onopen = function(event) {
    console.log('WebSocket connected');
    // Send a message to the server
    socket.send('WebSocket client connected');
};

// Event listener for incoming messages
socket.onmessage = function(event) {
    try {
        console.log(event.data);
        const mazeData = JSON.parse(event.data);
        console.log('Message from server: ', mazeData);
    } catch(error) {
        console.error('Error parsing JSON:', error);
    }
};

// Event listener for errors
socket.onerror = function(error) {
    console.error('WebSocket Error: ', error);
};

// Event listener for connection closes
socket.onclose = function(event) {
    console.log('WebSocket closed');
};
