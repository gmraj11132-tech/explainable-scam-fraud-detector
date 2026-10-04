import sys
import os

# Add parent directory to sys.path so app and its modules are imported cleanly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
