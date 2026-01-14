# uuid.py
import argparse
import random
import uuid


def _randomize_case(value: str, upper_ratio: float) -> str:
    chars = []
    for char in value:
        if char.isalpha() and random.random() < upper_ratio:
            chars.append(char.upper())
        else:
            chars.append(char)
    return "".join(chars)


def _randomize_case_by_block(value: str, upper_ratio: float) -> str:
    parts = value.split("-")
    randomized = []
    for part in parts:
        if random.random() < upper_ratio:
            randomized.append(part.upper())
        else:
            randomized.append(part.lower())
    return "-".join(randomized)


def _positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("count must be an integer") from exc
    if number <= 0:
        raise argparse.ArgumentTypeError("count must be positive")
    return number


def _ratio(value: str) -> float:
    try:
        ratio = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("upper-ratio must be a float") from exc
    if ratio < 0 or ratio > 1:
        raise argparse.ArgumentTypeError("upper-ratio must be between 0 and 1")
    return ratio


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate UUIDs with randomized uppercase letters.")
    parser.add_argument("-n", "--count", type=_positive_int, default=20, help="Number of UUIDs to generate.")
    parser.add_argument(
        "--upper-ratio",
        type=_ratio,
        default=0.3,
        help="Probability that each hex letter is uppercased (0 to 1).",
    )
    parser.add_argument(
        "--not-block-case",
        action="store_false",
        help="Randomize case per dash-separated block instead of per letter.",
    )

    args = parser.parse_args()

    for _ in range(args.count):
        value = str(uuid.uuid4())
        if args.not_block_case:
            print(_randomize_case_by_block(value, args.upper_ratio))
        else:
            print(_randomize_case(value, args.upper_ratio))

    return 0
