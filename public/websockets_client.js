// Connect to the WebSocket server
const socket = new WebSocket('ws://127.0.0.1:5005');

// Event listener for when the connection opens
socket.onopen = function(event) {
    console.log('WebSocket connected');
    // Send a message to the server
    socket.send('Connected');
};

// Event listener for incoming messages
socket.onmessage = function(event) {
    console.log('Message from server: ', event.data);
};

// Event listener for errors
socket.onerror = function(error) {
    console.error('WebSocket Error: ', error);
};

// Event listener for connection closes
socket.onclose = function(event) {
    console.log('WebSocket closed');
};
