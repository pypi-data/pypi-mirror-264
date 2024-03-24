"""pixie16-binary-browser for *.bin files.

Usage:
  pixie16-binary-browser [<filename>]

"""

from docopt import docopt

commands = docopt(__doc__)


def main():
    from pathlib import Path
    import sys

    from pixie16.ui import BinaryApp, QApplication

    filename = commands["<filename>"]
    filename = Path(filename) if filename else None
    if filename and not filename.exists():
        print(f"[Error] Cannot find file {filename}")
        sys.exit(1)

    app = QApplication([])
    ex = BinaryApp(app)
    if filename:
        ex.open_file(filename)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
