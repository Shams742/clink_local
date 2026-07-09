import os
import sys

# Add the 'code' directory to the path so we can import 'app'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'code'))

from app import create_app

app = create_app()
