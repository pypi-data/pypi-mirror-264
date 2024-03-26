import tempfile
from pathlib import Path
from typing import List
from argparse import Action

from git_changelog.cli import build_and_render, get_parser


def create_empty_changelog(changelog_path: Path):
    txt = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->

    """
    with open(changelog_path, "w") as f:
        f.write(txt)


def main(args: List[str] = None) -> int:
    """Check if CHANGELOG.md is up to dat with the last commits/tags.
    If not, updates it and interrupts commit

    """
    parser = get_parser()
    parser.add_argument("filenames", nargs="*")
    to_remove: List[Action] = []
    name_to_remove = ["repository", "output", "version", "help"]
    for action in parser._actions:
        if action.dest in name_to_remove:
            to_remove.append(action)

    for action in to_remove:
        parser._remove_action(action)
        for option_string in action.option_strings:
            parser._option_string_actions.pop(option_string, None)

    parser.add_argument("filenames", nargs="*")

    opts = parser.parse_args(args=args)

    changelog_path = Path("CHANGELOG.md")
    if not Path(changelog_path).exists():
        create_empty_changelog(changelog_path)

    with open(changelog_path) as f:
        old_changelog = f.read()

    retval = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_file = Path(tmpdir) / changelog_path.name

        with open(temp_file, "w") as fp:
            fp.write(old_changelog)

        # Write changelog to a temporary file
        build_and_render(
            repository=".",
            template=opts.template,
            convention=opts.convention,
            parse_refs=opts.parse_refs,
            parse_trailers=opts.parse_trailers,
            sections=opts.sections,
            in_place=opts.in_place,
            output=str(temp_file),
            version_regex=opts.version_regex,
            marker_line=opts.marker_line,
            bump_latest=opts.bump_latest,
        )

        with open(temp_file, "r") as fp:
            new_changelog = fp.read()

    if new_changelog != old_changelog:
        retval = 1
        with open(changelog_path, "w") as f:
            f.write(new_changelog)

    return retval
