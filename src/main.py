from editor import init_editor
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


if sys.version_info[:3] != (3, 11, 0):
    sys.exit("This project requires Python 3.11.0")

def main():
    init_editor.init_editor()

if __name__ == "__main__":
    main()


