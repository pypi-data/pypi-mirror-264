"""__main__.py file"""
import sys
from prusalinkapi import PrusaLink

def main():
    """Main Function"""
    args = sys.argv[1:]  # Exclude the script name

    printer = PrusaLink(args[0], args[1], args[2])

    try:
        return getattr(printer, args[3])
    except AttributeError as exc:
        raise AttributeError from exc

if __name__ == "__main__":
    main()
