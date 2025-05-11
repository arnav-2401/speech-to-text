import os
import sys

def startup():
    if sys.prefix == getattr(sys, 'base_prefix', sys.prefix):
        # Running in the main environment
        print("Running in the main environment\n" "Looking for virtual environment...\n")
        program_path = os.path.dirname(os.path.abspath(__file__))
        venv_cmd = os.path.join(program_path, "venv", "bin", "python")
        if not os.path.isfile(venv_cmd):
            sys.exit(f"No virtualenv found at {venv_cmd} – run:\n" f"   python3 -m venv venv")
        else:
            print(f"Found virtual environment at {venv_cmd}\n" "Starting it...\n")
        os.execv(venv_cmd, [venv_cmd] + sys.argv)

startup()
