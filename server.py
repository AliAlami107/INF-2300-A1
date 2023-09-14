#!/usr/bin/env python3
import socketserver
import json

# File path to store messages
MESSAGE_FILE_PATH = "messages.json"


class MyTCPHandler(socketserver.StreamRequestHandler):
    """Class for handling TCP requests."""

    # ========================
    # Methods for Parsing and Reading Requests
    # ========================
    
    def read_request_line(self):
        """Read the request line from the incoming HTTP request."""
        return self.rfile.readline().decode('utf-8').strip()

    def read_headers(self):
        """Read HTTP headers from the incoming HTTP request."""
        headers = []
        while True:
            line = self.rfile.readline().decode('utf-8').strip()
            if not line:
                break
            headers.append(line)
        return headers

    def parse_request_line(self, request_line):
        """Parse the request line into HTTP method, resource, and HTTP version."""
        return request_line.split(" ")

    def is_directory_traversal(self, resource):
        """Check if the resource path contains directory traversal elements."""
        return ".." in resource
    

    # ========================
    # Endpoint Handling for /messages
    # ========================

    def messages_GET_request(self, http_version):
        """Handle GET requests for the /messages endpoint."""

        try:
            with open(MESSAGE_FILE_PATH, "r") as f:
                content = json.load(f)
            self.serve_json(content, http_version)
        except FileNotFoundError:
            self.send_error(404, "Not Found", http_version)


    # Utility methods for /messages endpoint
    def serve_json(self, content, http_version):
        content_str = json.dumps(content)
        content_bytes = content_str.encode('utf-8')
        content_length = len(content_bytes)
        headers = f"{http_version} 200 OK\r\nContent-Type: application/json\r\nContent-Length: {content_length}\r\n\r\n"
        self.wfile.write(headers.encode('utf-8'))
        self.wfile.write(content_bytes)



    def handle_post_messages(self, headers, http_version):
        """Handle POST requests for the /messages endpoint."""
        try:
            content_length = int(self.get_header_value(headers, "Content-Length"))
            body = self.rfile.read(content_length).decode('utf-8')
            new_message = json.loads(body)

            try:
                with open(MESSAGE_FILE_PATH, 'r') as f:
                    messages = json.load(f)
            except FileNotFoundError:
                messages = []

            new_id = len(messages) + 1

            
            # Create a new dictionary with 'id' field first, then 'text'
            ordered_message = {"id": new_id, "text": new_message.get("text", "")}
            messages.append(ordered_message)

            with open(MESSAGE_FILE_PATH, 'w') as f:
                json.dump(messages, f)

            self.serve_json_with_status(new_message, http_version, 201, "Created")
        except Exception as e:
            self.send_error(400, "Bad Request", http_version)


        """Send a JSON response with a custom status code and message."""
    def serve_json_with_status(self, content, http_version, status_code, status_message):
        content_str = json.dumps(content)
        content_bytes = content_str.encode('utf-8')
        content_length = len(content_bytes)
        headers = f"{http_version} {status_code} {status_message}\r\nContent-Type: application/json\r\nContent-Length: {content_length}\r\n\r\n"
        self.wfile.write(headers.encode('utf-8'))
        self.wfile.write(content_bytes)

    ### PUT to /messages 
    def handle_put_messages(self, headers, http_version):
        """Handle PUT requests for the /messages endpoint."""
        try:
            # Step 1: Get the Content-Length from headers
            content_length = int(self.get_header_value(headers, "Content-Length"))

            # Step 2: Read the request body
            body = self.rfile.read(content_length).decode('utf-8')

            # Step 3: Parse the request body as JSON
            updated_message = json.loads(body)

            # Step 4: Load existing messages from the file
            try:
                with open(MESSAGE_FILE_PATH, 'r') as f:
                    messages = json.load(f)
            except FileNotFoundError:
                self.send_error(404, "Not Found", http_version)
                return

            # Step 5: Find the message with the given ID and update its text
            message_id = updated_message.get('id')
            if message_id is None:
                self.send_error(400, "Bad Request: Missing ID", http_version)
                return

            found = False
            for message in messages:
                if message['id'] == message_id:
                    message['text'] = updated_message.get('text', "")
                    found = True
                    break

            if not found:
                self.send_error(404, "Not Found", http_version)
                return

            # Step 6: Save updated messages back to the file
            with open(MESSAGE_FILE_PATH, 'w') as f:
                json.dump(messages, f)

            # Step 7: Send response
            self.serve_json_with_status({"message": "Updated successfully"}, http_version, 200, "OK")

        except Exception as e:
            self.send_error(400, "Bad Request", http_version)

    
    ### DELETE to /messages 
    def handle_delete_messages(self, headers, http_version):
        """Handle DELETE requests for the /messages endpoint."""
        try:
            # Step 1: Get the Content-Length from headers
            content_length = int(self.get_header_value(headers, "Content-Length"))

            # Step 2: Read the request body
            body = self.rfile.read(content_length).decode('utf-8')

            # Step 3: Parse the request body as JSON
            message_to_delete = json.loads(body)

            # Step 4: Load existing messages from the file
            try:
                with open(MESSAGE_FILE_PATH, 'r') as f:
                    messages = json.load(f)
            except FileNotFoundError:
                self.send_error(404, "Not Found", http_version)
                return

            # Step 5: Find the message with the given ID and remove it
            message_id = message_to_delete.get('id')
            if message_id is None:
                self.send_error(400, "Bad Request: Missing ID", http_version)
                return

            found = False
            for i, message in enumerate(messages):
                if message['id'] == message_id:
                    del messages[i]
                    found = True
                    break

            if not found:
                self.send_error(404, "Not Found", http_version)
                return

            # Step 6: Save updated messages back to the file
            with open(MESSAGE_FILE_PATH, 'w') as f:
                json.dump(messages, f)

            # Step 7: Send response
            self.serve_json_with_status({"message": "Deleted successfully"}, http_version, 200, "OK")

        except Exception as e:
            self.send_error(400, "Bad Request", http_version)




    ########################################################
    ### First endpoint / & /index.html ###
    ########################################################

    def handle_get_request(self, resource, http_version):
        """Handle GET requests for general endpoints like / and /index.html."""
        if resource in ["/", "/index.html"]:
            self.serve_file("index.html", "text/html", http_version)
        elif resource in ["/server.py", "server.py"]:
            self.send_error(403, "Forbidden", http_version)
        else:
            self.send_error(404, "Not Found", http_version)


    def handle_post_request(self, resource, headers, http_version):
        """Handle POST requests for general endpoints."""
        content_length = int(self.get_header_value(headers, "Content-Length"))
        body = self.rfile.read(content_length)
        with open(resource.lstrip('/'), "ab") as f:
            f.write(body)
        self.serve_file(resource.lstrip('/'), "text/plain", http_version)


    def serve_file(self, file_path, content_type, http_version):
        """Serve a file from the disk."""
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            content_length = len(content)
            headers = f"{http_version} 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {content_length}\r\n\r\n"
            self.wfile.write(headers.encode('utf-8'))
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "Not Found", http_version)

    def send_error(self, status_code, message, http_version):
        """Send an HTTP error response."""
        body = message.encode('utf-8')
        headers = f"{http_version} {status_code} {message}\r\nContent-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n"
        self.wfile.write(headers.encode('utf-8'))
        self.wfile.write(body)

    def get_header_value(self, headers, key):
        """Retrieve the value of a specific header."""
        for header in headers:
            k, v = header.split(": ", 1)   
            if k.lower() == key.lower():
                return v
        return None

    # ========================
    # Main Entry Point
    # ========================
    def handle(self):
        """Main method to handle incoming HTTP requests."""

        request_line = self.read_request_line()
        headers = self.read_headers()
        print(f"Received request: {request_line}")


        method, resource, http_version = self.parse_request_line(request_line)


        if self.is_directory_traversal(resource):
            self.send_error(403, "Forbidden", http_version)
            return

        # Handling /messages resource
        if resource == "/messages":
            if method == "GET":
                self.messages_GET_request(http_version)
            elif method == "POST":
                self.handle_post_messages(headers, http_version)
            elif method == "PUT":
                self.handle_put_messages(headers, http_version)
            elif method == "DELETE":
                self.handle_delete_messages(headers, http_version)  
        else:
            if method == "GET":
                self.handle_get_request(resource, http_version)
            elif method == "POST":
                self.handle_post_request(resource, headers, http_version)




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"Serving at: http://{HOST}:{PORT}")
        server.serve_forever()

"""
    This class is responsible for handling a request. The whole class is
    handed over as a parameter to the server instance so that it is capable
    of processing request. The server will use the handle-method to do this.
    It is instantiated once for each request!
    Since it inherits from the StreamRequestHandler class, it has two very
    usefull attributes you can use:

    rfile - This is the whole content of the request, displayed as a python
    file-like object. This means we can do readline(), readlines() on it!

    wfile - This is a file-like object which represents the response. We can
    write to it with write(). When we do wfile.close(), the response is
    automatically sent.

    The class has three important methods:
    handle() - is called to handle each request.
    setup() - Does nothing by default, but can be used to do any initial
    tasks before handling a request. Is automatically called before handle().
    finish() - Does nothing by default, but is called after handle() to do any
    necessary clean up after a request is handled.

        This method is responsible for handling an http-request. You can, and should(!),
        make additional methods to organize the flow with which a request is handled by
        this method. But it all starts here!
        """
