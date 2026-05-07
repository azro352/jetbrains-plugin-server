import re
from importlib.metadata import PackageNotFoundError, metadata

import markdown

HTML_PREFIX = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Jetbrains Plugin Server</title>
</head>
<body>
"""

HTML_SUFFIX = """
</body>
</html>
"""


def get_homepage() -> str:
    md = "# Jetbrains plugin server"
    try:
        mdt = metadata("jetbrains-plugin-server")
        md += " v" + mdt["version"] + "\n\n"
        md += mdt["description"]
        md = re.sub(r"- `(/[^`]*)`", r"- [`\1`](\1)", md)
    except PackageNotFoundError:
        pass

    return HTML_PREFIX + markdown.markdown(md) + HTML_SUFFIX


def get_favicon() -> str:
    return """
    <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g clip-path="url(#clip0_8802_42984)">
        <path d="M20.34 3.66L3.66 20.34C1.32 22.68 0 25.86 0 29.18V59C0 61.76 2.24 64 5 64H34.82C38.14 64 41.31 62.68 43.66 60.34L60.34 43.66C62.68 41.32 64 38.14 64 34.82V5C64 2.24 61.76 0 59 0H29.18C25.86 0 22.69 1.32 20.34 3.66Z"
              fill="url(#paint0_linear_8802_42984)"/>
        <path d="M48 16H8V56H48V16Z" fill="black"/>
        <path d="M30 47H13V51H30V47Z" fill="white"/>
    </g>
    <defs>
        <linearGradient id="paint0_linear_8802_42984" x1="0.850001" y1="62.72" x2="62.62" y2="1.81"
                        gradientUnits="userSpaceOnUse">
            <stop stop-color="#FF9419"/>
            <stop offset="0.43" stop-color="#FF021D"/>
            <stop offset="0.99" stop-color="#E600FF"/>
        </linearGradient>
        <clipPath id="clip0_8802_42984">
            <rect width="64" height="64" fill="white"/>
        </clipPath>
    </defs>
</svg>
"""
