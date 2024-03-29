import unittest
from unittest.mock import patch, MagicMock
import socket
import threading
import ssl
import configparser
from server import handle_client, start_server 

class TestServer(unittest.TestCase):

    @patch('socket.socket')
    @patch('threading.Thread')
    def test_start_server(self, mock_thread, mock_socket):
        # Mock the socket and threading modules
        mock_socket.return_value.bind.return_value = None
        mock_socket.return_value.listen.return_value = None
        mock_socket.return_value.accept.return_value = (MagicMock(), ('127.0.0.1', 12345))

        # Call the start_server function
        start_server('192.168.96.1', 8086)

        # Assert that the socket was bound and listened
        mock_socket.return_value.bind.assert_called_once()
        mock_socket.return_value.listen.assert_called_once()

    @patch('socket.socket')
    def test_handle_client(self, mock_socket):
        # Mock the socket module
        mock_socket.return_value.recv.return_value = b'test\x00'
        mock_socket.return_value.send.return_value = None
        mock_socket.return_value.close.return_value = None

        # Call the handle_client function
        handle_client(mock_socket.return_value)

        # Assert that the client received the correct response
        mock_socket.return_value.send.assert_called_with(b'STRING EXISTS\n')

    @patch('socket.socket')
    def test_handle_client_string_not_found(self, mock_socket):
        # Mock the socket module
        mock_socket.return_value.recv.return_value = b'nonexistent\x00'
        mock_socket.return_value.send.return_value = None
        mock_socket.return_value.close.return_value = None

        # Call the handle_client function
        handle_client(mock_socket.return_value)

        # Assert that the client received the correct response
        mock_socket.return_value.send.assert_called_with(b'STRING NOT FOUND\n')

if __name__ == '__main__':
    unittest.main()
