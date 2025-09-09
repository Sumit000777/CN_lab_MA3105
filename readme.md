This project implements a simple TCP client-server communication in Python for the CN (Computer Networks) Lab assignment.

📌 Features

Client

Connects to the server (IP + port).

Sends its name and an integer (input from keyboard).

Receives server’s name and integer.

Displays both integers, both names, and their sum.



Server

Listens on a port (>5000).

Accepts connections from clients.

Prints client’s name, server’s name, both integers, and their sum.

If the client sends an integer outside 1–100, the server terminates.