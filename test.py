import main
import unittest
from unittest.mock import patch, MagicMock
from main import add_customer

class TestCustomerFunctions(unittest.TestCase):

    @patch('your_module_name.get_connection')
    def test_add_customer_success(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 123

        customer_id = add_customer("Test User", "test@example.com", 1000.0)

        mock_cursor.execute.assert_called_with(
            "INSERT INTO customers (customer_name, email_address, credit_limit_"
        )