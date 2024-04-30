import unittest
from unittest.mock import MagicMock

class TestOrganizeWindows(unittest.TestCase):
    def test_organize_windows(self):
        # Mocking the getWindowsWithTitle function
        gw = MagicMock()
        gw.getWindowsWithTitle.return_value = [
            MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
        ]

        # Call the function
        organize_windows(gw)

        # Assert that the windows are minimized and maximized
        for window in gw.getWindowsWithTitle.return_value:
            window.minimize.assert_called_once()
            window.maximize.assert_called_once()

        # Assert the window positions and sizes
        expected_positions = [
            (0, 0), (440, 0), (880, 0), (1320, 0), (1760, 0)
        ]
        expected_size = (450, 240)

        for i, window in enumerate(gw.getWindowsWithTitle.return_value):
            window.resizeTo.assert_called_once_with(*expected_size)
            window.moveTo.assert_called_once_with(*expected_positions[i])

if __name__ == '__main__':
    unittest.main()