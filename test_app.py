import unittest
from unittest.mock import patch
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.connections.Connection')  # Mock the database connection
    def test_home_route(self, mock_db_conn):
        # Set up the mocked connection
        mock_conn = mock_db_conn.return_value
        mock_cursor = mock_conn.cursor.return_value

        # Define the behavior of the mock cursor
        mock_cursor.fetchone.return_value = (1, 'John', 'Doe', 'Python', 'New York')

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the App', response.data)

    # Add more test cases here

if __name__ == '__main__':
    unittest.main()
