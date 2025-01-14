const socket = new WebSocket('ws://' + window.location.host + '/ws/posts/');  // Open WebSocket connection to the server

// When the WebSocket connection opens
socket.onopen = function(e) {
    console.log("WebSocket connection established.");
};

// When the WebSocket receives a message
socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('Message from server:', data.message);
    // You can update the page with the received data here
};

// When the WebSocket connection closes
socket.onclose = function(e) {
    console.log('WebSocket connection closed.');
};

// To send a message over the WebSocket connection
function sendMessage() {
    const message = {
        'message': 'Hello, Server!'
    };
    socket.send(JSON.stringify(message));
}

// Example of sending a message when a button is clicked
document.getElementById('sendButton').addEventListener('click', sendMessage);
