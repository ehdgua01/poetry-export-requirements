import argparse
import difflib
import subprocess
from distutils.util import strtobool
from typing import Optional, Sequence

REQUIREMENTS_TXT = "requirements.txt"
DEV_REQUIREMENTS_TXT = "requirements-dev.txt"
RETURN_MSG = "Generated new requirements file"
PASS = 0
FAIL = 1


def check_diff(new: bytes, old: bytes) -> bool:
    return (
        True if difflib.SequenceMatcher(a=old, b=new).quick_ratio() < 1 else False
    )


def poetry_export_requirements(
        output: str = None, dev: bool = False, extras: str = "",
        without_hashes: bool = False, with_credentials: bool = False,
) -> int:
    if not output:
        output = REQUIREMENTS_TXT if not dev else DEV_REQUIREMENTS_TXT

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
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.strip()
    except subprocess.CalledProcessError as e:
        print(e)
        return FAIL

    try:
        old_requirements_txt = open(output, "rb+")
    except OSError:
        with open(output, "wb") as f:
            f.write(new_requirements)
        print(RETURN_MSG)
        return FAIL

    try:
        if check_diff(new_requirements, old_requirements_txt.read().strip()):
            old_requirements_txt.seek(0)
            old_requirements_txt.write(new_requirements)
            old_requirements_txt.truncate()
            print(RETURN_MSG)
            return FAIL
    finally:
        old_requirements_txt.close()

    return PASS


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", "-o", nargs="?", const=REQUIREMENTS_TXT, default=None,
        help="The name of the output file.",
    )
    parser.add_argument(
        "--dev", "-D", nargs="?", type=strtobool, const=True, default=False,
        help="Include development dependencies.",
    )
    parser.add_argument(
        "--extras", "-E", nargs="?", default=None,
        help="Extra sets of dependencies to include.",
    )
    parser.add_argument(
        "--without-hashes", nargs="?", type=strtobool, const=True, default=False,
        help="Exclude hashes from the exported file.",
    )
    parser.add_argument(
        "--with-credentials", nargs="?", type=strtobool, const=True, default=False,
        help="Include credentials for extra indices.",
    )
    args = parser.parse_args(argv)
    return poetry_export_requirements(
        output=args.output,
        dev=args.dev,
        extras=args.extras,
        without_hashes=args.without_hashes,
        with_credentials=args.with_credentials,
    )


if __name__ == "__main__":
    exit(main())
