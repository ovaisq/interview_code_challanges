import unittest
from unittest.mock import patch

from kitties import images
from kitties import viewer


class TestViewer(unittest.TestCase):
    """Test cases for the viewer module in the kitties package.
    """

    def test_make_into_rows(self):
        """Test the make_into_rows function with a predefined set of images.

            This test checks if the function correctly arranges a list of image
            dictionaries into rows based on given width and height constraints.
        """

        output = viewer.make_into_rows(images.six_kitties, 220, 40)

        expected_output = [
            [
                {"width": 50,  "height": 40, "src": "kitty1.jpg"},
                {"width": 20,  "height": 40, "src": "kitty2.jpg"},
                {"width": 100, "height": 40, "src": "kitty3.jpg"}
            ], [
                {"width": 80,  "height": 40, "src": "kitty4.jpg"},
                {"width": 80,  "height": 40, "src": "kitty5.jpg"},
                {"width": 60,  "height": 40, "src": "kitty6.jpg"}
            ]
        ]

        self.assertEqual(expected_output, output)

    def test_make_into_rows_empty_list(self):
        """Test the make_into_rows function with an empty list of images.

            This test checks if the function returns None when given an empty list of
            images, ensuring that it handles edge cases gracefully.
        """

        output = viewer.make_into_rows([], 220, 40)

        expected_output = None

        self.assertEqual(expected_output, output)

    @patch('logging.error')
    def test_make_into_rows_empty_list_logging(self, mock_logging):
        """Test logging error for empty image list.
        """
        
        viewer.make_into_rows([], 80, 40)
        mock_logging.assert_called_once_with("Empty image list")
        
    def test_make_into_rows_multiple_images_exceed_page_width(self):
        """Test with multiple images that exceed the page width.
        """

        images = [
            {"width": 40, "height": 10, "src": "kitty1.jpg"},
            {"width": 50, "height": 10, "src": "kitty2.jpg"},
            {"width": 40, "height": 10, "src": "kitty3.jpg"}
        ]

        output = viewer.make_into_rows(images, 220, 40)

        expected_output = [
            [{"width": 160, "height": 40, "src": "kitty1.jpg"}],
            [{"width": 200, "height": 40, "src": "kitty2.jpg"}],
            [{"width": 160, "height": 40, "src": "kitty3.jpg"}]
        ]

        self.assertEqual(output, expected_output)
    
    def test_make_into_rows_single_image_exceeds_page_width(self):
        """Test with a single image that exceeds the page width.
        """
    
        images = [{"width": 100, "height": 10, "src": "kitty1.jpg"}]
    
        output = viewer.make_into_rows(images, 80, 10)
    
        expected_output = [[],[{"width": 100, "height": 10, "src": "kitty1.jpg"}]]
    
        self.assertEqual(output, expected_output)
