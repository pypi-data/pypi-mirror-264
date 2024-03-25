import streamlit as st
from code_editor import code_editor
import os
from aio_code_editor.ui import side_bar, heading, codes_box, run_code

def run():
    # install numpy
    os.system("pip install numpy")
    # UI
    file_name = side_bar()
    heading()
    codes, type = codes_box()
    run_code(file_name, codes, type)
    
if __name__ == "__main__":
    run()