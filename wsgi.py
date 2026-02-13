import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import app as app_module
app = app_module.app

if __name__ == "__main__":
    app.run()
