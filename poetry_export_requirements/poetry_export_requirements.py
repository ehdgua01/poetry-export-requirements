import argparse
import difflib
import subprocess
from typing import Tuple

REQUIREMENTS_TXT = "requirements.txt"
DEV_REQUIREMENTS_TXT = "requirements-dev.txt"
RETURN_MSG = "Generated new requirements file"
PASS = 0
FAIL = 1


def is_diff(new: str, old: str) -> bool:
    return (
        True
        if difflib.SequenceMatcher(a=old, b=new).quick_ratio() < 1
        else False
    )


def poetry_export_requirements(
    output: str,
    dev: bool = False,
    extras: str = "",
    without_hashes: bool = False,
    with_credentials: bool = False,
) -> Tuple[int, bool]:
    """
    :return: Return result code, flag of Created requirements file
    """
    cmd = ["poetry", "export", "-f", REQUIREMENTS_TXT]
    if dev:
        cmd.append("--dev")

    if extras:
        cmd.extend(["--extras", extras])

    if without_hashes:
        cmd.append("--without-hashes")

    if with_credentials:
        cmd.append("--with-credentials")

    try:
        new_requirements = subprocess.run(
            cmd, stdout=subprocess.PIPE, universal_newlines=True, check=True,
        ).stdout.strip()

        if not len(new_requirements):
            return PASS, False
    except subprocess.CalledProcessError as e:
        print(f"ERROR[{e.returncode}]: {e.stderr or e.stdout}")
        return FAIL, False

    try:
        old_requirements_txt = open(output, "r+")
    except OSError:
        with open(output, "w") as f:
            f.write(new_requirements)
        print(RETURN_MSG)
        return FAIL, True

    try:
        if is_diff(new_requirements, old_requirements_txt.read().strip()):
            old_requirements_txt.seek(0)
            old_requirements_txt.write(new_requirements)
            old_requirements_txt.truncate()
            print(RETURN_MSG)
            return FAIL, True
    finally:
        old_requirements_txt.close()

    return PASS, True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    parser.add_argument(
        "--dev",
        "-D",
        action="store_true",
        help="Include development dependencies.",
    )
    parser.add_argument(
        "--without-hashes",
        action="store_true",
        help="Exclude hashes from the exported file.",
    )
    parser.add_argument(
        "--with-credentials",
        action="store_true",
        help="Include credentials for extra indices.",
    )
    parser.add_argument(
        "--without-output",
        action="store_true",
        help="Allow commit without requirements output.",
    )
    parser.add_argument(
        "--output",
        "-o",
        nargs="?",
        const=REQUIREMENTS_TXT,
        default=None,
        help="The name of the output file.",
    )
    parser.add_argument(
        "--extras",
        "-E",
        nargs="?",
        default=None,
        help="Extra sets of dependencies to include.",
    )
    args = parser.parse_args()

    if not args.output:
        args.output = REQUIREMENTS_TXT if not args.dev else DEV_REQUIREMENTS_TXT

    ret, created = poetry_export_requirements(
        output=args.output,
        dev=args.dev,
        extras=args.extras,
        without_hashes=args.without_hashes,
        with_credentials=args.with_credentials,
    )

    if ret is FAIL:
        return FAIL

    if (
        created
        and args.output not in args.filenames
        and args.without_output is False
    ):
        print(f"{args.output} not staged for commit")
        return FAIL

    return PASS


if __name__ == "__main__":
    exit(main())
