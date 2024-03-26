import sys
from .main import loo

def main():
    if len(sys.argv) < 2:
        print("Usage: python laeplooth <text>")
        sys.exit(1)
    text = sys.argv[1]
    try:
        loo(text)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
