import angreal
import subprocess
from pathlib import Path
import shutil

root = angreal.get_root()
DEV_DIR = Path(root) / "dev"

# Ensure dev directory exists
DEV_DIR.mkdir(exist_ok=True)

@angreal.command(name="setup", about="Install dependencies")
def setup():
    """Install all project dependencies."""
    subprocess.run(["npm", "install"], cwd=root, check=True)
    print("Dependencies installed.")

@angreal.command(name="dev", about="Start the development server")
def dev():
    """Start the development server."""
    subprocess.run(["npm", "run", "dev"], cwd=root, check=True)

@angreal.command(name="build", about="Build the project for production")
def build():
    """Build the project for production."""
    subprocess.run(["npm", "run", "build"], cwd=root, check=True)
    print("Build complete! Output is in the 'dist' directory.")

@angreal.command(name="lint", about="Run the linter")
def lint():
    """Run the linter on the codebase."""
    subprocess.run(["npm", "run", "lint"], cwd=root, check=True)

@angreal.command(name="clean", about="Clean build caches and node_modules")
def clean():
    """Remove build artifacts and node_modules."""
    targets = [
        Path(root) / "dist",
        Path(root) / ".astro",
        Path(root) / "node_modules",
        DEV_DIR,
    ]
    for target in targets:
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
                print(f"Removed directory: {target}")
            else:
                target.unlink()
                print(f"Removed file: {target}")
    DEV_DIR.mkdir(exist_ok=True)
    print("Clean complete!")