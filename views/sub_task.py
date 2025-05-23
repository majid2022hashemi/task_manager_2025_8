import sys
import os

# Get the absolute path of the parent directory (project root)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to Python path at the beginning (to take precedence)
sys.path.insert(0, project_root)

# Now import
from db import get_connection

conn = get_connection()
print("✅ Connection successful!")
conn.close()



