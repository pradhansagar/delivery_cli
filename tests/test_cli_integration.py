import unittest
import os
from io import StringIO
from unittest.mock import patch
from delivery.cli.app import run_app
from delivery.cli.input_providers import FileInputProvider

class TestCliIntegration(unittest.TestCase):
    def setUp(self):
        # Determine the path to the sample input file
        self.sample_file_path = os.path.join(os.path.dirname(__file__), '..', 'import', 'sample_input.txt')

    @patch('sys.stdout', new_callable=StringIO)
    def test_run_app_cost_mode_from_file_provider(self, mock_stdout):
        print("\n--- Test: CLI Integration - Cost Mode ---")
        lines = [
            "cost",
            "100 3",
            "PKG1 5 5 OFR001",
            "PKG2 15 5 OFR002",
            "PKG3 10 100 OFR003"
        ]
        provider = FileInputProvider(lines)
        run_app(provider)
        output = mock_stdout.getvalue()
        print("Output:\n", output)
        
        self.assertIn("Total cost for PKG1", output)
        self.assertIn("Total cost for PKG2", output)
        self.assertIn("Total cost for PKG3", output)
        print("Status: SUCCESS")

    @patch('sys.stdout', new_callable=StringIO)
    def test_run_app_delivery_mode_from_sample_file(self, mock_stdout):
        print("\n--- Test: CLI Integration - Delivery Mode (from Sample File) ---")
        
        # Use the static factory method directly
        provider = FileInputProvider.from_file(self.sample_file_path)
            
        run_app(provider)
        output = mock_stdout.getvalue()
        print("Output:\n", output)
        
        # Verify output format: PKG1 discount total_cost delivery_time
        self.assertIn("PKG1", output)
        self.assertIn("PKG2", output)
        self.assertIn("PKG3", output)
        print("Status: SUCCESS")

if __name__ == "__main__":
    unittest.main()
