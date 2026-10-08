#!/usr/bin/env python3
"""Basic static quality checks for the AI Dev App landing page."""
import re
import sys
from html.parser import HTMLParser

HTML_FILE = "index.html"
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img",
    "input", "link", "meta", "param", "source", "track", "wbr",
}


class TagBalanceChecker(HTMLParser):
    """Detects stray or unclosed non-void tags."""

    def __init__(self):
        super().__init__()
        self.stack = []
        self.problems = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.problems.append(f"stray closing tag </{tag}>")
        elif self.stack[-1] != tag:
            self.problems.append(f"expected </{self.stack[-1]}> but found </{tag}>")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()


def check(html):
    errors = []

    for tag in ["<!doctype html>", "<html", "<head", "<body", "</html>"]:
        if tag not in html.lower():
            errors.append(f"missing required tag: {tag}")

    if 'name="viewport"' not in html:
        errors.append("missing viewport meta tag for responsiveness")

    if not re.search(r"<title>.*?</title>", html, re.S | re.I):
        errors.append("missing <title> element")

    if "<form" not in html:
        errors.append("no <form> element found")
    for field in ['id="name"', 'id="email"', 'id="message"']:
        if field not in html:
            errors.append(f"contact form missing field: {field}")

    parser = TagBalanceChecker()
    parser.feed(html)
    for tag in parser.stack:
        parser.problems.append(f"unclosed tag <{tag}>")
    errors.extend(parser.problems)

    for number, line in enumerate(html.splitlines(), 1):
        if len(line) > 200:
            errors.append(f"line {number} is longer than 200 characters")
        if line != line.rstrip():
            errors.append(f"line {number} has trailing whitespace")

    if "\t" in html:
        errors.append("file contains tab characters (use spaces)")

    return errors


def main():
    try:
        with open(HTML_FILE, encoding="utf-8") as handle:
            html = handle.read()
    except FileNotFoundError:
        print(f"FAIL: {HTML_FILE} not found")
        return 1

    print(f"Checking {HTML_FILE} ({len(html)} characters)")
    errors = check(html)

    if errors:
        print("\nFAIL: code quality issues found:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("\nPASS: all code quality checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
