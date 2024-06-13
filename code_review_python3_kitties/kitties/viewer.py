"""This module provides functionality for viewing kitties in rows based on
    specified page width and row height.
"""

import argparse
import logging
import pprint

from kitties import images

parser = argparse.ArgumentParser(description="View Kitties")
parser.add_argument("--page_width", type=int, default=80)
parser.add_argument("--row_height", type=int, default=10)


def make_into_rows(image_list, page_width, row_height):
    """Take a list of dictionary of images and split them into rows.

        Input:
            image_list (list): List of image dictionaries with 'width', 'height', and 'src' keys.
            page_width (int): The width of the display page.
            row_height (int): The height of each row in pixels.

        Returns:
            list of rows: A 2D list representing the rows of images, where each sublist contains
                    dictionaries with 'width', 'height', and 'src' keys for each image.
    """

    rows_list = [[]] #list of rows of lists of image dictionaries
    cur_row = 0
    cur_width = 0

    # if list is NOT empty
    if image_list:
        for image in image_list:
            new_width = image["width"] * row_height / image["height"]
            total_width = cur_width + new_width
            if total_width > page_width:
                # Start a new row.
                rows_list.append([])
                cur_row += 1
                cur_width = 0
            rows_list[cur_row].append({"width": new_width, "height": row_height, "src": image["src"]})
            cur_width += new_width
        return rows_list
    else:
        logging.error("Empty image list")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO) # init logging

    args = parser.parse_args()
    try:
        as_rows = make_into_rows(images.six_kitties, args.page_width, args.row_height)
        printer = pprint.PrettyPrinter(compact=True)
        printer.pprint(as_rows)
        exit(0)
    except AttributeError as e:
        logging.error(e)
