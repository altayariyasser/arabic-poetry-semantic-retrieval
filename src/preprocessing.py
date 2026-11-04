"""Expose the existing Arabic normalizer without modifying a corpus or index."""
import argparse
import sys

from .lexical import normalize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('text', nargs='?', help='Arabic text; omit to read stdin')
    parser.add_argument('--fold', action='store_true', help='Apply existing alef/ya folding')
    args = parser.parse_args()
    text = args.text if args.text is not None else sys.stdin.read()
    print(normalize(text, fold=args.fold))


if __name__ == '__main__':
    main()
