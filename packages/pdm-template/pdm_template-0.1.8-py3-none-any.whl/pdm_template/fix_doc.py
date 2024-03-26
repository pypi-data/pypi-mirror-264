# -*- coding: utf-8 -*-
from pathlib import Path
import shutil
import typing as T
import argparse
import re
import os.path

# from . import logger


def find_doc_index(doc_root: Path) -> Path:
    index_pth = None
    for p in doc_root.rglob("index.html"):
        if index_pth is None:
            index_pth = p.parent
        if "coverage" not in str(p) and len(str(p.parent)) < len(str(index_pth)):
            index_pth = p.parent
    return index_pth


def copy_resource(dst: Path):
    import inspect
    import pdm_template

    index_pth = find_doc_index(dst)

    pdm_copier_root = Path(inspect.getfile(pdm_template)).resolve().parent
    shutil.copytree(pdm_copier_root / "resource", index_pth, dirs_exist_ok=True)

    # logger.info(f"Scripts and styles copied to '{index_pth}'")


def fix_integrity(doc_root: Path, p: Path) -> int:
    """Remove the integrity attribute of html tags
    Example:
    <link rel="preload stylesheet" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/10up-sanitize.css/11.0.1/sanitize.min.css"
      integrity="sha256-PK9q560IAAa6WVRRh76LtCaI8pjTJ2z11v0miyNNjrs=" crossorigin>

    Becomes:
    <link rel="preload stylesheet" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/10up-sanitize.css/11.0.1/sanitize.min.css"
      crossorigin>

    Args:
        p: Path to a html file

    """
    rel_pth = os.path.relpath(doc_root, p.parent)
    src = p.read_text().split("\n")
    modified = 0
    style_list = [
        "github.min.css",
        "normalize.min.css",
        "sanitize.min.css",
        "typography.min.css",
        "bootstrap.min.css",
    ]
    script_list = ["highlight.min.js", "latest.js"]
    with open(p, "w") as dst:
        for raw_line in src:
            while "><" in raw_line:
                raw_line = raw_line.replace("><", ">\n<").replace("\r", "")
            for line in raw_line.strip().split("\n"):
                line = line.strip()
                new_line = line[:]

                if 'integrity="' in line:
                    i = line.index('integrity="')
                    j = line.index('"', i + 13)
                    new_line = line[:i] + line[j + 1 :]

                for s in style_list:
                    if f"/{s}" in new_line:
                        new_line = re.sub(f"""https://.*\/{s}""", f"{rel_pth}/style/{s}", new_line)

                for s in script_list:
                    if f"/{s}" in new_line:
                        new_line = re.sub(
                            f"""https://.*\/{s}(\?config=TeX-AMS_CHTML)*""",
                            f"{rel_pth}/script/{s}",
                            new_line,
                        )

                if new_line != line:
                    modified += 1

                dst.write(new_line + "\n")

    return modified


def main(args: T.List[str] = None) -> int:
    """Fix doc html files integrity info"""
    parser = argparse.ArgumentParser(
        prog="fix-doc", description="Fix doc html files integrity info"
    )
    parser.add_argument("files", type=Path, nargs="*", help="an integer for the accumulator")
    parser.add_argument(
        "--ret", action="store_true", help="If activated, returns the number of lines modified"
    )
    opts = parser.parse_args(args=args)

    dst = Path("htmldoc")
    index_pth = find_doc_index(dst)

    copy_resource(dst)

    modified = 0
    for p in dst.rglob("**/*"):
        if p.is_file() and p.suffix in [".html", ".htm"]:
            modified += fix_integrity(index_pth, p)

    if opts.ret:
        return modified
    else:
        return 0


if __name__ == "__main__":
    main()
