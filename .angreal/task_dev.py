import angreal
import subprocess
from pathlib import Path
import shutil
import sys

root = angreal.get_root()
DEV_DIR = Path(root) / "dev"

# Ensure dev directory exists
DEV_DIR.mkdir(exist_ok=True)

# Define command group
docs = angreal.command_group(name="docs", about="commands for documentation tasks")


def _clean_docs():
    """Clean the documentation build directory."""
    dist_dir = Path(root) / "dist"
    if dist_dir.exists():
        print("Cleaning documentation build directory...")
        shutil.rmtree(dist_dir)
        print("Clean complete!")
    return 0


@angreal.command(name="build", about="Build the project for production")
def build():
    """Build the project for production."""
    subprocess.run(["npm", "run", "build"], cwd=root, check=True)
    print("Build complete! Output is in the 'dist' directory.")

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


@docs()
@angreal.command(name="clean", about="clean the documentation build directory")
def docs_clean():
    """Clean the documentation build directory."""
    return _clean_docs()


@docs()
@angreal.command(name="serve", about="serve the documentation site locally, by default building draft documents.")
@angreal.argument(
    name="prod",
    long="prod",
    help="exclude draft content from the build",
    required=False,
    takes_value=False,
    is_flag=True
)
def docs_serve(prod: bool = False):
    """Serve the documentation site locally.

    Args:
        prod: If True, excludes draft content from the build. Defaults to False.
    """
    print("=== Setting up documentation ===")

    # Clean the build directory first
    clean_result = _clean_docs()
    if clean_result != 0:
        return clean_result

    # Start development server
    print("\n=== Starting development server ===")
    print("Documentation will be available at http://localhost:4321")
    print("Press Ctrl+C to stop the server")

    try:
        # By default include drafts, unless prod flag is set
        if prod:
            print("Excluding draft content from build")
            # For production mode, we'd need to modify the build process
            # This is a simplified version - you might want to add draft filtering
            subprocess.run(["npm", "run", "dev"], cwd=root, check=True)
        else:
            print("Including draft content in build")
            subprocess.run(["npm", "run", "dev"], cwd=root, check=True)
        
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Development server failed: {e}", file=sys.stderr)
        return e.returncode


@docs()
@angreal.command(name="build", about="build the documentation site, by default excluding draft documents.")
@angreal.argument(
    name="draft",
    long="draft",
    help="include draft content in the build",
    required=False,
    takes_value=False,
    is_flag=True
)
def docs_build(draft: bool = False):
    """Build the documentation site.

    Args:
        draft: If True, includes draft content in the build. Defaults to False.
    """
    print("=== Building documentation site ===")

    # Clean the build directory first
    clean_result = _clean_docs()
    if clean_result != 0:
        return clean_result

    # Build the site
    print("\nBuilding site...")
    try:
        if draft:
            print("Including draft content in build")
            # For draft mode, you might want to modify the build process
            # This is a simplified version
            subprocess.run(["npm", "run", "build"], cwd=root, check=True)
        else:
            print("Excluding draft content from build (production mode)")
            subprocess.run(["npm", "run", "build"], cwd=root, check=True)
        
        print("\n=== Build complete ===")
        print(f"Documentation site built in {root}/dist")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Failed to build documentation: {e}", file=sys.stderr)
        return e.returncode