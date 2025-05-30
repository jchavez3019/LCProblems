"""
This program creates a new Jupyter notebook for a LeetCode problem, better automating the process. In order to comply
with the Terms of Service of LeetCode, this program does not programmatically open the LeetCode problem webpage.
Instead, you must first open a debugging session in Chrome using the command:

google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug-profile

and navigate to the LeetCode problem's webpage. Thereafter, you can run this program with the following command:

python create_lc_template.py <name_of_new_directory>

Once invoked, this script will scape the problem description, create a new notebook in the specified directory,
and paste this problem description into the notebook as the first Markdown cell. It will also paste boilerplate code
into the notebook as a code cell.

TODO:
    Extend this program to scrape the default code given in the problem and inject this into the boilerplate code.
    Additionally, it would be nice to scrape the default test-cases and inject this into the boilerplate code.
"""
import os, nbformat, argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

## BEGIN PROGRAM ARGUMENTS ##
parser = argparse.ArgumentParser()
# Build arguments
parser.add_argument("new_directory", type=str,
                    help="Name of the new directory in the LeetCode repo.")
parser.add_argument("--div_class", type=str, default="elfjS",
                    help="The HTML to scrape. The LC problem description typically has 'elfjS' as its class name.")
parser.add_argument("--subdirectory", type=str, default="python_helper",
                    help="Inside the new LC, I like to place Python programs in its own subdirectory in case I want "
                         "to revisit the LC problem in a different language.")
parser.add_argument("--notebook_name", type=str, default="python_main.ipynb",
                    help="The name of the newly created Jupyter notebook.")
parser.add_argument("--localhost", type=str, default="localhost:9222",
                    help="The local host address for the Chrome debugger.")
parser.add_argument("--boilerplate_code", type=str,
help="This is an example of boilerplate code that I typically like to use when I tackle LeetCode problems locally.",
default=r"""
class Solution:

def main():
    test_cases = {
        "1": {
            "nums": [1,0,1],
            "queries": [[0,2]],
            "expected": True,
        },
        "2": {
            "nums": [4,3,2,1],
            "queries": [[1,3],[0,2]],
            "expected": False,
        },
    }

    solution = Solution()

    for tk, targs in test_cases.items():
        expected = targs.pop("expected", None)
        ret = solution.isZeroArray(**targs, verbose=True)
        if expected is not None:
            passed = ret == expected
        else:
            passed = None
        print(f"test case {tk}: {targs}\nReturned: {ret}, Expected: {expected}\nPassed:{passed}\n")


main()
""")
# Parse arguments
args = parser.parse_args()
args_dict = vars(args)
## END PROGRAM ARGUMENTS

def extract_div_html(class_name: str, driver: webdriver.Chrome) -> str:
    """Find the first div with the given class name and return its outer HTML."""
    div = driver.find_element(By.CLASS_NAME, class_name)
    return div.get_attribute("outerHTML")

def create_notebook(html_text: str, output_path: str, boilerplate_code: str = "# Your code goes here"):
    """Create a Jupyter notebook with the HTML as a Markdown cell and boilerplate code as a code cell."""
    nb = nbformat.v4.new_notebook()

    # Add Markdown cell
    md_cell = nbformat.v4.new_markdown_cell(f"\n{html_text}\n")
    nb.cells.append(md_cell)

    # Add code cell that imports typing
    import_cell = nbformat.v4.new_code_cell("from typing import *")
    nb.cells.append(import_cell)

    # Add boilerplate code cell
    code_cell = nbformat.v4.new_code_cell(boilerplate_code)
    nb.cells.append(code_cell)

    # Write notebook (this also creates the new subdirectories)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    print(f"Notebook saved to: {output_path}")

def run_scraper(div_class: str, driver: webdriver.Chrome, relative_path: str, boilerplate_code: str):
    """The main program action which will extract the html and create the notebook."""
    html = extract_div_html(div_class, driver)
    create_notebook(html, relative_path, boilerplate_code=boilerplate_code)

def main():

    # gets the relevant arguments
    div_class = args_dict.get("div_class")
    new_directory = args_dict.get("new_directory")
    subdirectory = args_dict.get("subdirectory")
    notebook_name = args_dict.get("notebook_name")
    localhost = args_dict.get("localhost")
    boilerplate_code = args_dict.get("boilerplate_code")

    # create the relative path to the new notebook
    if subdirectory is not None:
        relative_path = os.path.join(new_directory, subdirectory, notebook_name)
    else:
        relative_path = os.path.join(new_directory, notebook_name)

    # Initialize options for the Chrome driver
    chrome_options = Options()
    chrome_options.debugger_address = localhost

    # Ensure the chromedriver matches the browser version
    driver = webdriver.Chrome(options=chrome_options)

    try:
        run_scraper(div_class, driver, relative_path, boilerplate_code)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
