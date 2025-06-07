"""
run_streamlit.py – Entry Point for B5W2 Streamlit UI
----------------------------------------------------

This script acts as the launch wrapper for the Streamlit interface defined
in `ui/app_streamlit.py`. It imports the modular launch_app() function and
executes it when run as a standalone program.

To run:
    streamlit run scripts/run_streamlit.py

Author: Nabil Mohamed
"""

# ------------------------------------------------------------------------------
# 🛠 Ensure Script Runs from Project Root (for src/ imports to work)
# ------------------------------------------------------------------------------

import os
import sys

# If running from /notebooks/, move up to project root
if os.path.basename(os.getcwd()) == "notebooks":
    os.chdir("..")
    print("📂 Changed working directory to project root")

# Add project root to sys.path so `src/` modules can be imported
project_root = os.getcwd()
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"✅ Added to sys.path: {project_root}")

# Confirm expected output path
expected_path = "data/cleaned"
print(
    "📁 Output path ready"
    if os.path.exists(expected_path)
    else f"⚠️ Output path not found: {expected_path}"
)


from ui.app_streamlit import launch_app


# ------------------------------------------------------------------------------
# 🚀 Launch Streamlit App – Main Execution Trigger
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Launch the app (controlled via ui/app_streamlit.py)
    launch_app()
