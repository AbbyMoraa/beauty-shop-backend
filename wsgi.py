import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import application
app = application.app

if __name__ == "__main__":
    app.run()
