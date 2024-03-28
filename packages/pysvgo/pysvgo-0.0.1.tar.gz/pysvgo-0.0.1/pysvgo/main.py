# main.py
# Import the sys library
import sys
from core import PySvgO

if __name__ == "__main__": 
    # Initialize our app with the parameters received from CLI with the sys.argv 
    # Starts from the position one due to position 0 will be main.py
    app = PySvgO(sys.argv[1:])  # python main.py default addition multiplication
    # Run our application 
    app.run()
