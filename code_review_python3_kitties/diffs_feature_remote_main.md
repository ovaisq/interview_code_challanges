## GIT LOG SUMMARY

```shell
> git log --pretty=format:"%h %s" --author=ovais --name-status

ed07333 added new tests
M       tests/test_viewer.py

4339276 clarified docstring
M       kitties/viewer.py

12ddb47 added git diffs, run and test output files
A       commits.txt
A       diffs_feature_remote_main.md
A       run.md

59c1924 clarified total width test
M       kitties/viewer.py

50e68f5 Added test case details to the tests
M       tests/test_viewer.py

9a6078f Added empty list test
M       tests/test_viewer.py

99f29f3 viewer.py: clarified docstring, added empty list exception handaling, added logging, clarified list of rows variable name
M       kitties/viewer.py

8dd47ea pylint: removed duplicated argparse import, clarified variable scope by renaming images variable to images_list
M       kitties/viewer.py

ee33a5f pylint: added docstring to images.py
M       kitties/images.py

d0c4784 pylint: snake_case variables, add docstrings
M       kitties/viewer.py

24da7bd Fixed typo verson to version
M       README.md
```


## GIT DIFF

```shell
> git diff ovais-quraishi-pr..origin/main

diff --git a/README.md b/README.md
index ea05720..4ac8fdb 100644
--- a/README.md
+++ b/README.md
@@ -7,7 +7,7 @@ This utility code takes images of kitties and arranges them in nice rows.

 ### Setup

-Ensure you're using python 3.10. If you use `pyenv` to manage python environments, run `pyenv version` to check. Run `pyenv global 3.10.0` to set 3.10.0 as the global version.
+Ensure you're using python 3.10. If you use `pyenv` to manage python environments, run `pyenv verson` to check. Run `pyenv global 3.10.0` to set 3.10.0 as the global version.

 Create the virtual env so you have all the right versions of all the right packages. We'll use pipenv which integrations virtualenv and pip nicely.

diff --git a/commits.txt b/commits.txt
deleted file mode 100644
index b32481f..0000000
--- a/commits.txt
+++ /dev/null
@@ -1,21 +0,0 @@
-git log --pretty=format:"%h %s" --author=ovais --name-status
-50e68f5 Added test case details to the tests
-M       tests/test_viewer.py
-
-9a6078f Added empty list test
-M       tests/test_viewer.py
-
-99f29f3 viewer.py: clarified docstring, added empty list exception handaling, added logging, clarified list of rows variable name
-M       kitties/viewer.py
-
-8dd47ea pylint: removed duplicated argparse import, clarified variable scope by renaming images variable to images_list
-M       kitties/viewer.py
-
-ee33a5f pylint: added docstring to images.py
-M       kitties/images.py
-
-d0c4784 pylint: snake_case variables, add docstrings
-M       kitties/viewer.py
-
-24da7bd Fixed typo verson to version
-M       README.md
diff --git a/diffs_feature_remote_main.md b/diffs_feature_remote_main.md
deleted file mode 100644
index 8f07260..0000000
--- a/diffs_feature_remote_main.md
+++ /dev/null
@@ -1,147 +0,0 @@
-diff --git a/README.md b/README.md
-index ea05720..4ac8fdb 100644
---- a/README.md
-+++ b/README.md
-@@ -7,7 +7,7 @@ This utility code takes images of kitties and arranges them in nice rows.
-
- ### Setup
-
--Ensure you're using python 3.10. If you use `pyenv` to manage python environments, run `pyenv version` to check. Run `pyenv global 3.10.0` to set 3.10.0 as the global version.
-+Ensure you're using python 3.10. If you use `pyenv` to manage python environments, run `pyenv verson` to check. Run `pyenv global 3.10.0` to set 3.10.0 as the global version.
-
- Create the virtual env so you have all the right versions of all the right packages. We'll use pipenv which integrations virtualenv and pip nicely.
-
-diff --git a/kitties/images.py b/kitties/images.py
-index c434ad6..bf69ae0 100644
---- a/kitties/images.py
-+++ b/kitties/images.py
-@@ -1,10 +1,3 @@
--"""A list of dictionaries representing information about six kitties.
--    Each dictionary contains three keys:
--    - "width": The width of the kitty image in pixels.
--    - "height": The height of the kitty image in pixels.
--    - "src": The filename of the kitty image.
--"""
--
- six_kitties = [
-     {"width": 100, "height": 80, "src": "kitty1.jpg"},
-     {"width": 10,  "height": 20, "src": "kitty2.jpg"},
-diff --git a/kitties/viewer.py b/kitties/viewer.py
-index b2410b9..a6f6222 100644
---- a/kitties/viewer.py
-+++ b/kitties/viewer.py
-@@ -1,9 +1,4 @@
--"""This module provides functionality for viewing kitties in rows based on
--    specified page width and row height.
--"""
--
- import argparse
--import logging
- import pprint
-
- from kitties import images
-@@ -13,47 +8,25 @@ parser.add_argument("--page_width", type=int, default=80)
- parser.add_argument("--row_height", type=int, default=10)
-
-
--def make_into_rows(image_list, page_width, row_height):
--    """Take a list of dictionary of images and split them into rows.
--
--        Args:
--            images (list): List of image dictionaries with 'width', 'height', and 'src' keys.
--            page_width (int): The width of the display page.
--            row_height (int): The height of each row in pixels.
--
--        Returns:
--            list of rows: A 2D list representing the rows of images, where each sublist contains
--                    dictionaries with 'width', 'height', and 'src' keys for each image.
--    """
--
--    rows_list = [[]] #list of rows of lists of image dictionaries
--    cur_row = 0
--    cur_width = 0
--
--    # if list is NOT empty
--    if image_list:
--        for image in image_list:
--            new_width = image["width"] * row_height / image["height"]
--            if cur_width + new_width > page_width:
--                # Start a new row.
--                rows_list.append([])
--                cur_row += 1
--                cur_width = 0
--            rows_list[cur_row].append({"width": new_width, "height": row_height, "src": image["src"]})
--            cur_width += new_width
--        return rows_list
--    else:
--        logging.error("Empty image list")
-+def make_into_rows(images, pageWidth, rowHeight):
-+    ret = [[]]
-+    curRow = 0
-+    curWidth = 0
-+    for image in images:
-+        newWidth = image["width"] * rowHeight / image["height"]
-+        if curWidth + newWidth > pageWidth:
-+            # Start a new row.
-+            ret.append([])
-+            curRow += 1
-+            curWidth = 0
-+        ret[curRow].append({"width": newWidth, "height": rowHeight, "src": image["src"]})
-+        curWidth += newWidth
-+    return ret
-
-
- if __name__ == "__main__":
--    logging.basicConfig(level=logging.INFO) # init logging
--
-     args = parser.parse_args()
--    try:
--        as_rows = make_into_rows(images.six_kitties, args.page_width, args.row_height)
--        printer = pprint.PrettyPrinter(compact=True)
--        printer.pprint(as_rows)
--        exit(0)
--    except AttributeError as e:
--        logging.error(e)
-+    as_rows = make_into_rows(images.six_kitties, args.page_width, args.row_height)
-+    printer = pprint.PrettyPrinter(compact=True)
-+    printer.pprint(as_rows)
-+    exit(0)
-diff --git a/tests/test_viewer.py b/tests/test_viewer.py
-index ef896fb..1176e1d 100644
---- a/tests/test_viewer.py
-+++ b/tests/test_viewer.py
-@@ -5,16 +5,8 @@ from kitties import viewer
-
-
- class TestViewer(unittest.TestCase):
--    """Test cases for the viewer module in the kitties package.
--    """
-
-     def test_make_into_rows(self):
--        """Test the make_into_rows function with a predefined set of images.
--
--            This test checks if the function correctly arranges a list of image
--            dictionaries into rows based on given width and height constraints.
--        """
--
-         output = viewer.make_into_rows(images.six_kitties, 220, 40)
-
-         expected_output = [
-@@ -30,16 +22,3 @@ class TestViewer(unittest.TestCase):
-         ]
-
-         self.assertEqual(expected_output, output)
--
--    def test_make_into_rows_empty_list(self):
--        """Test the make_into_rows function with an empty list of images.
--
--            This test checks if the function returns None when given an empty list of
--            images, ensuring that it handles edge cases gracefully.
--        """
--
--        output = viewer.make_into_rows([], 220, 40)
--
--        expected_output = None
--
--        self.assertEqual(expected_output, output)
-\ No newline at end of file
diff --git a/kitties/images.py b/kitties/images.py
index c434ad6..bf69ae0 100644
--- a/kitties/images.py
+++ b/kitties/images.py
@@ -1,10 +1,3 @@
-"""A list of dictionaries representing information about six kitties.
-    Each dictionary contains three keys:
-    - "width": The width of the kitty image in pixels.
-    - "height": The height of the kitty image in pixels.
-    - "src": The filename of the kitty image.
-"""
-
 six_kitties = [
     {"width": 100, "height": 80, "src": "kitty1.jpg"},
     {"width": 10,  "height": 20, "src": "kitty2.jpg"},
diff --git a/kitties/viewer.py b/kitties/viewer.py
index 3613d44..a6f6222 100644
--- a/kitties/viewer.py
+++ b/kitties/viewer.py
@@ -1,9 +1,4 @@
-"""This module provides functionality for viewing kitties in rows based on
-    specified page width and row height.
-"""
-
 import argparse
-import logging
 import pprint

 from kitties import images
@@ -13,48 +8,25 @@ parser.add_argument("--page_width", type=int, default=80)
 parser.add_argument("--row_height", type=int, default=10)


-def make_into_rows(image_list, page_width, row_height):
-    """Take a list of dictionary of images and split them into rows.
-
-        Args:
-            images (list): List of image dictionaries with 'width', 'height', and 'src' keys.
-            page_width (int): The width of the display page.
-            row_height (int): The height of each row in pixels.
-
-        Returns:
-            list of rows: A 2D list representing the rows of images, where each sublist contains
-                    dictionaries with 'width', 'height', and 'src' keys for each image.
-    """
-
-    rows_list = [[]] #list of rows of lists of image dictionaries
-    cur_row = 0
-    cur_width = 0
-
-    # if list is NOT empty
-    if image_list:
-        for image in image_list:
-            new_width = image["width"] * row_height / image["height"]
-            total_width = cur_width + new_width
-            if total_width > page_width:
-                # Start a new row.
-                rows_list.append([])
-                cur_row += 1
-                cur_width = 0
-            rows_list[cur_row].append({"width": new_width, "height": row_height, "src": image["src"]})
-            cur_width += new_width
-        return rows_list
-    else:
-        logging.error("Empty image list")
+def make_into_rows(images, pageWidth, rowHeight):
+    ret = [[]]
+    curRow = 0
+    curWidth = 0
+    for image in images:
+        newWidth = image["width"] * rowHeight / image["height"]
+        if curWidth + newWidth > pageWidth:
+            # Start a new row.
+            ret.append([])
+            curRow += 1
+            curWidth = 0
+        ret[curRow].append({"width": newWidth, "height": rowHeight, "src": image["src"]})
+        curWidth += newWidth
+    return ret


 if __name__ == "__main__":
-    logging.basicConfig(level=logging.INFO) # init logging
-
     args = parser.parse_args()
-    try:
-        as_rows = make_into_rows(images.six_kitties, args.page_width, args.row_height)
-        printer = pprint.PrettyPrinter(compact=True)
-        printer.pprint(as_rows)
-        exit(0)
-    except AttributeError as e:
-        logging.error(e)
+    as_rows = make_into_rows(images.six_kitties, args.page_width, args.row_height)
+    printer = pprint.PrettyPrinter(compact=True)
+    printer.pprint(as_rows)
+    exit(0)
diff --git a/run.md b/run.md
deleted file mode 100644
index c22ac46..0000000
--- a/run.md
+++ /dev/null
@@ -1,49 +0,0 @@
-## RUN OUTPUT
-
-```shell
-> make run
-
-pipenv run python -m kitties.viewer
-[[{'height': 10, 'src': 'kitty1.jpg', 'width': 12.5},
-  {'height': 10, 'src': 'kitty2.jpg', 'width': 5.0},
-  {'height': 10, 'src': 'kitty3.jpg', 'width': 25.0},
-  {'height': 10, 'src': 'kitty4.jpg', 'width': 20.0}],
- [{'height': 10, 'src': 'kitty5.jpg', 'width': 20.0},
-  {'height': 10, 'src': 'kitty6.jpg', 'width': 15.0}]]
-```
-```shell
-> make run flags="--page_width=80 --row_height=200"
-
-pipenv run python -m kitties.viewer --page_width=80 --row_height=200
-[[], [{'height': 200, 'src': 'kitty1.jpg', 'width': 250.0}],
- [{'height': 200, 'src': 'kitty2.jpg', 'width': 100.0}],
- [{'height': 200, 'src': 'kitty3.jpg', 'width': 500.0}],
- [{'height': 200, 'src': 'kitty4.jpg', 'width': 400.0}],
- [{'height': 200, 'src': 'kitty5.jpg', 'width': 400.0}],
- [{'height': 200, 'src': 'kitty6.jpg', 'width': 300.0}]]
-```
-```shell
->  make run flags="--page_width=0 --row_height=0"
-
-pipenv run python -m kitties.viewer --page_width=0 --row_height=0
-[[{'height': 0, 'src': 'kitty1.jpg', 'width': 0.0},
-  {'height': 0, 'src': 'kitty2.jpg', 'width': 0.0},
-  {'height': 0, 'src': 'kitty3.jpg', 'width': 0.0},
-  {'height': 0, 'src': 'kitty4.jpg', 'width': 0.0},
-  {'height': 0, 'src': 'kitty5.jpg', 'width': 0.0},
-  {'height': 0, 'src': 'kitty6.jpg', 'width': 0.0}]]
-```
-
-## Tests
-
-```shell
-> make test
-
-pipenv run python -m unittest
-.ERROR:root:Empty image list
-.
-----------------------------------------------------------------------
-Ran 2 tests in 0.000s
-
-OK
-```
\ No newline at end of file
diff --git a/tests/test_viewer.py b/tests/test_viewer.py
index ef896fb..1176e1d 100644
--- a/tests/test_viewer.py
+++ b/tests/test_viewer.py
@@ -5,16 +5,8 @@ from kitties import viewer


 class TestViewer(unittest.TestCase):
-    """Test cases for the viewer module in the kitties package.
-    """

     def test_make_into_rows(self):
-        """Test the make_into_rows function with a predefined set of images.
-
-            This test checks if the function correctly arranges a list of image
-            dictionaries into rows based on given width and height constraints.
-        """
-
         output = viewer.make_into_rows(images.six_kitties, 220, 40)

         expected_output = [
@@ -30,16 +22,3 @@ class TestViewer(unittest.TestCase):
         ]

         self.assertEqual(expected_output, output)
-
-    def test_make_into_rows_empty_list(self):
-        """Test the make_into_rows function with an empty list of images.
-
-            This test checks if the function returns None when given an empty list of
-            images, ensuring that it handles edge cases gracefully.
-        """
-
-        output = viewer.make_into_rows([], 220, 40)
-
-        expected_output = None
-
-        self.assertEqual(expected_output, output)
\ No newline at end of file
```
