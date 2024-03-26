from dataclasses import dataclass
import logging
import tempfile
from pathlib import Path
import typing as T
import re
import argparse


@dataclass
class Todo:
    file: Path
    line_number: int
    text: str


def find_todos(repository: Path, exclude: T.List[Path]) -> T.List[Todo]:
    from . import logger

    parse_cfg = {
        ".cpp": re.compile("^[ \t]*//[ ]*todo[: ]", flags=re.IGNORECASE),
        ".c": re.compile("^[ \t]*//[ ]*todo[: ]", flags=re.IGNORECASE),
        ".cc": re.compile("^[ \t]*//[ ]*todo[: ]", flags=re.IGNORECASE),
        ".cxx": re.compile("^[ \t]*//[ ]*todo[: ]", flags=re.IGNORECASE),
        ".hpp": re.compile("^[ \t]*//[ ]*todo[: ]", flags=re.IGNORECASE),
        ".h": re.compile("^[ \t]*//[ ]*todo[: ]", flags=re.IGNORECASE),
        ".py": re.compile("^[ \t]*#[ ]*todo[: ]", flags=re.IGNORECASE),
        ".i": re.compile("^[ \t]*#[ ]*todo[: ]", flags=re.IGNORECASE),
        ".ksy": re.compile("^[ \t]*#[ ]*todo[: ]", flags=re.IGNORECASE),
        ".sh": re.compile("^[ \t]*[#;][ ]*todo[: ]", flags=re.IGNORECASE),
    }

    enc_regex = re.compile(r"coding[=:]\s*([-\w.]+)")

    # TODO: Improve file parsing
    todo_list = list()
    for fp in repository.glob("./src/**/*"):
        if not fp.is_file():
            continue

        to_be_excluded = False
        for ex_path in exclude:
            if fp.resolve().is_relative_to(ex_path):
                to_be_excluded = True
                logger.debug(f"File {fp} excluded (matches {ex_path})")
                break

        if to_be_excluded:
            continue

        ext = fp.suffix

        com_regex = parse_cfg.get(ext, None)
        if com_regex is None:
            logger.debug(f"Skipping extension {ext} ({fp})")
            continue

        if fp.parts[0].startswith("."):
            continue

        line = ""
        enc = None
        for open_enc in [None, "ascii", "utf-8"]:
            try:
                if open_enc is not None:
                    kwds = {"mode": "r", "encoding": open_enc}
                else:
                    kwds = {"mode": "r"}

                # https://docs.python.org/3/reference/lexical_analysis.html#encoding-declarations
                with open(fp, **kwds) as f:
                    line = f.readline()
                    m = enc_regex.split(line)
                    if len(m) >= 2:
                        enc = m[1]

                    line = f.readline()
                    m = enc_regex.split(line)
                    if len(m) >= 2:
                        enc = m[1]
                    else:
                        enc = "utf-8"

            except Exception as e:
                pass

        if enc is None:
            logger.error(f"enc=={enc}")
            continue

        line = ""
        with open(fp, encoding=enc) as f:
            logger.debug(f"Analysing {fp} for TODO")
            for ln, line in enumerate(f.readlines()):
                m = com_regex.split(line, maxsplit=100)
                if len(m) >= 2:
                    t = Todo(fp, ln + 1, m[1].strip())
                    logger.debug(f"Found TODO: {t}")
                    todo_list.append(t)

    return todo_list


def build_and_render(repository: Path, output: Path, exclude: T.List[Path]):
    todo_list = find_todos(repository, exclude=exclude)

    # https://github.com/todotxt/todo.txt
    with open(output, mode="w", encoding="utf-8") as f:
        for t in todo_list:
            f.write(f"- [{t.file}#L{t.line_number}]({t.file}#L{t.line_number}): {t.text}\n")


def main(args: T.List[str] = None) -> int:
    """Check if TODO.md is up to date with the last commits/tags.
    If not, updates it and interrupts commit

    """
    from . import logger

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ignore", nargs="*", help="List of directory to exclude")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    opts = parser.parse_args(args=args)
    if opts.verbose:
        logger.setLevel(logging.DEBUG)
    if opts.ignore is None:
        exclude = []
    else:
        exclude = [
            Path(p).expanduser().resolve()
            for p in opts.ignore
            if Path(p).expanduser().resolve().exists()
        ]

    todo_path = Path("TODO.md")
    todo_path.touch(exist_ok=True)

    with open(todo_path) as f:
        old_todo = f.read()

    retval = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_file = Path(tmpdir) / todo_path.name

        with open(temp_file, "w") as fp:
            fp.write(old_todo)

        # Write todos to a temporary file
        build_and_render(repository=Path("."), output=temp_file, exclude=exclude)

        with open(temp_file, "r") as fp:
            new_todo = fp.read()

    if new_todo != old_todo:
        retval = 1
        with open(todo_path, "w") as f:
            f.write(new_todo)

    logger.debug(f"Returned {retval}")

    return retval


if __name__ == "__main__":
    main(["-i", "tests/**/*"])
