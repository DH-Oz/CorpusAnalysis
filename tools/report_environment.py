"""Print the environment a CI leg actually got, and optionally assert it.

A matrix label is a claim. `sotu`'s CI advertised a matrix over Python 3.10 to 3.14
while running CPython 3.10 on every leg for five releases, and nothing about the green
badge distinguished nine legs from one leg repeated nine times. It surfaced only when
an unrelated change made one combination fail to resolve.

So every leg here states its platform, interpreter and text encoding, and fails if the
platform is not the one the matrix said it would be. The encoding line matters on its
own: the course reads a German dictionary whose terms carry umlauts, and a machine that
decodes it as anything other than UTF-8 loses those terms silently.

    uv run python tools/report_environment.py
    uv run python tools/report_environment.py --expect-system Windows
"""

import argparse
import locale
import platform
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--expect-system",
        help="Fail unless platform.system() matches, e.g. Linux, Darwin, Windows.",
    )
    arguments = parser.parse_args()

    system = platform.system()
    print(f"  platform.system():     {system}")
    print(f"  platform.machine():    {platform.machine()}")
    print(f"  platform.release():    {platform.release()}")
    print(f"  python:                {sys.version.split()[0]}")
    print(f"  sys.flags.utf8_mode:   {sys.flags.utf8_mode}")
    print(f"  locale.getencoding():  {locale.getencoding()}")
    print(f"  sys.getdefaultencoding(): {sys.getdefaultencoding()}")

    # The number that actually decides whether the German dictionary survives.
    dictionary = Path(__file__).resolve().parent.parent / "dictionaries" / "nietzsche.dic"
    if dictionary.exists():
        with open(dictionary) as handle:
            print(f"  a bare open() chooses:  {handle.encoding}")

    try:
        import pandas
        print(f"  pandas:                {pandas.__version__}")
    except ImportError:
        print("  pandas:                not installed")

    if arguments.expect_system and system != arguments.expect_system:
        print(f"\nThis leg claimed to be {arguments.expect_system} and is {system}.")
        return 1

    if arguments.expect_system:
        print(f"\nConfirmed: this leg really is {arguments.expect_system}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
