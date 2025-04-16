import angreal
import subprocess
from pathlib import Path
import shutil
import os
import signal
import time
import platform
import sys

# Create a command group for dev-related commands
dev = angreal.command_group(name="dev", about="Development environment commands")

root = angreal.get_root()
DEV_DIR = Path(root) / "dev"
PID_FILE = DEV_DIR / "dev_server.pid"

# Ensure dev directory exists
DEV_DIR.mkdir(exist_ok=True)

def get_process_output_file(pid):
    """Get the output file for a process in a cross-platform way."""
    system = platform.system().lower()
    
    if system == 'windows':
        # On Windows, we'll use PowerShell to get the process output
        return None
    else:
        # On Unix-like systems (Linux, macOS), use lsof
        try:
            result = subprocess.run(
                ["lsof", "-p", str(pid), "-a", "-d", "1"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                # Parse lsof output to get the file descriptor
                for line in result.stdout.splitlines():
                    if "REG" in line:  # Regular file
                        parts = line.split()
                        if len(parts) > 8:
                            return parts[8]  # The file path
        except Exception:
            pass
    return None

@dev()
@angreal.command(name="setup", about="Setup the development environment")
def setup():
    """
    Setup the development environment by installing dependencies and configuring the project.
    """
    # Get the project root directory
    project_root = Path(root).parent
    
    # Install dependencies using pnpm
    print("Installing dependencies...")
    subprocess.run(["npm", "install"], cwd=project_root, check=True)
        
    print("Development environment setup complete!")

def is_server_running():
    """Check if the dev server is running by checking the PID file and process."""
    if not PID_FILE.exists():
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        # Check if process exists
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        # Process doesn't exist or PID file is invalid
        if PID_FILE.exists():
            PID_FILE.unlink()
        return False

@dev()
@angreal.command(name="run", about="Start the development server")
def run():
    """
    Start the development server with hot reloading enabled.
    """
    project_root = Path(root).parent
    print("Starting development server...")
    subprocess.run(["npm", "run", "dev"], cwd=project_root, check=True)

@dev()
@angreal.command(name="stop", about="Stop the development server")
def stop():
    """Stop the running development server."""
    if not is_server_running():
        print("No development server is running.")
        return
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        # Kill the process group
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        
        # Wait for process to terminate
        for _ in range(10):  # 10 attempts
            try:
                os.kill(pid, 0)
                time.sleep(0.5)
            except OSError:
                break
        else:
            # If process is still running, force kill it
            os.killpg(os.getpgid(pid), signal.SIGKILL)
        
        PID_FILE.unlink()
        print("Development server stopped.")
    except Exception as e:
        print(f"Error stopping server: {e}")
        if PID_FILE.exists():
            PID_FILE.unlink()

@dev()
@angreal.command(name="status", about="Check development server status")
def status():
    """Check if the development server is running."""
    if is_server_running():
        with open(PID_FILE, 'r') as f:
            pid = f.read().strip()
        print(f"Development server is running with PID: {pid}")
    else:
        print("Development server is not running.")

@dev()
@angreal.command(name="logs", about="View development server logs")
def logs():
    """View the development server logs by attaching to the process output."""
    if not is_server_running():
        print("No development server is running.")
        return
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        system = platform.system().lower()
        
        if system == 'windows':
            # On Windows, use PowerShell to get process output
            print("Attaching to server output (press Ctrl+C to stop)...")
            try:
                subprocess.run([
                    "powershell",
                    "-Command",
                    f"Get-Process -Id {pid} | Select-Object -ExpandProperty StandardOutput"
                ])
            except KeyboardInterrupt:
                print("\nDetached from server output.")
        else:
            # On Unix-like systems, try to get the output file
            output_file = get_process_output_file(pid)
            if output_file:
                print("Attaching to server output (press Ctrl+C to stop)...")
                try:
                    subprocess.run(["tail", "-f", output_file])
                except KeyboardInterrupt:
                    print("\nDetached from server output.")
            else:
                print("Could not attach to process output. The process may not have a visible output stream.")
                print("Try running the server without background mode to see its output.")
    
    except Exception as e:
        print(f"Error attaching to process: {e}")

@dev()
@angreal.command(name="clean", about="Clean build caches and temporary files")
def clean():
    """
    Clean up build caches, temporary files, and other generated artifacts.
    """
    project_root = Path(root).parent
    
    # Directories and files to clean
    clean_targets = [
        project_root / "dist",
        project_root / ".astro",
        project_root / "node_modules",
        project_root / ".turbo",
        project_root / ".next",
        project_root / ".svelte-kit",
        DEV_DIR,  # Clean the dev directory
    ]
    
    print("Cleaning build caches and temporary files...")
    for target in clean_targets:
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
                print(f"Removed directory: {target}")
            else:
                target.unlink()
                print(f"Removed file: {target}")
    
    # Recreate the dev directory
    DEV_DIR.mkdir(exist_ok=True)
    
    print("Clean complete!") 