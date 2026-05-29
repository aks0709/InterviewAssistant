"""Auto-installer for project dependencies."""
import subprocess
import sys

def install_dependencies():
    """Install all required packages from requirements.txt."""
    print("Installing dependencies from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✓ All dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_dependencies()
