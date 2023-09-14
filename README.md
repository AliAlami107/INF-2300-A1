################################################################
###### Simple HTTP Server with JSON Message Storage
###### Overview
################################################################
#
#This Python script serves as a feature-rich HTTP server, designed to handle HTTP GET, POST, PUT, and DELETE requests. The server stores messages in JSON format in a file named `messages.json`. It's implemented using Python's `socketserver` library.
#
### Features
#
#- HTTP GET, POST, PUT, and DELETE request handling
#- JSON message storage and retrieval
#- TCP Socket Handling
#- HTTP header parsing
#
### How It Works
#### Main Components
#
#- `MyTCPHandler`: The class responsible for handling incoming HTTP requests.
#- `socketserver.TCPServer`: A class from the Python standard library used to create the TCP server.
#
#### Handling HTTP Requests
#
#- **GET Requests**: When a GET request is made to the "/messages" endpoint, the server reads the `messages.json` file and returns its content as a JSON response.
#- **POST Requests**: When a POST request is made to the "/messages" endpoint, the server reads the incoming message from the request body, appends it to the existing messages in `messages.json`, and returns the newly added message.
#- **PUT Requests**: PUT requests allow updating existing messages in the `messages.json` file by specifying the message ID.
#- **DELETE Requests**: DELETE requests allow removing messages from `messages.json` by specifying the message ID.
#
### Prerequisites
#
#- Python 3.x
#- No additional libraries are needed.
#
### Usage
#
#- Clone the repository or download the script.
#- Open a terminal and navigate to the folder containing the script.
#- Run `python3 server.py`
#- You will see the message "Serving at: http://localhost:8080".
#- Use an HTTP client to send GET, POST, PUT, or DELETE requests to `http://localhost:8080/messages`.
#
### Methods
#
#Here's a brief description of the methods in the `MyTCPHandler` class:
#
#- `read_request_line()`: Reads the request line from the incoming HTTP request.
#- `read_headers()`: Reads the headers from the incoming HTTP request.
#- `parse_request_line(request_line)`: Parses the request line into its components (method, resource, HTTP version).
#- `is_directory_traversal(resource)`: Checks for directory traversal elements in the requested resource.
#- `messages_GET_request(http_version)`: Handles GET requests for "/messages".
#- `handle_post_messages(headers, http_version)`: Handles POST requests for "/messages".
#- `handle_put_messages(headers, http_version)`: Handles PUT requests for "/messages".
#- `handle_delete_messages(headers, http_version)`: Handles DELETE requests for "/messages".
#- `serve_json(content, http_version)`: Serves JSON content as the response.
#- `handle()`: The main method responsible for delegating the handling of incoming HTTP requests based on the method and resource.
#
### Security Considerations
#
#- The script currently checks for directory traversal attacks but lacks many other security features. Do not use it in a production environment.
#- No authentication or authorization is implemented.
#
### Limitations and Future Work
#
#- Error handling is minimal and needs to be extended.
#- Consider implementing more security features like input validation and logging.
#
#