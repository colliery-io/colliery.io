import angreal
import subprocess
from pathlib import Path

@angreal.command(name="build", about="Build the project for production")
def build():
    """
    Build the project for production deployment.
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    print("Building project for production...")
    subprocess.run(["pnpm", "run", "build"], cwd=project_root, check=True)
    
    print("Build complete! Output is in the 'dist' directory.") 