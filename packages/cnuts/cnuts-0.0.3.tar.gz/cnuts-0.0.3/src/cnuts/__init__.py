import subprocess
import os

def nuts():
    print(os.path.dirname(__file__))
    subprocess.run(["streamlit", "run", f"{os.path.dirname(__file__)}/juice.py"])
