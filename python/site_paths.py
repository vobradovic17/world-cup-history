"""Convert generated root-relative links for pages one folder below root."""

import re


ATTRIBUTE = re.compile(r'((?:href|src|data-src)=")([^"]+)(")')


def for_subdirectory_page(markup: str) -> str:
    def relocate(match: re.Match[str]) -> str:
        prefix, value, suffix = match.groups()
        if value.startswith("assets/"):
            value = "../" + value
        elif value.startswith(("index.html", "teams.html", "players.html")):
            value = "../" + value
        elif value.endswith(".css") and "/" not in value:
            value = "../css/" + value
        elif value.endswith(".js") and "/" not in value:
            value = "../js/" + value
        return prefix + value + suffix

    return ATTRIBUTE.sub(relocate, markup)
