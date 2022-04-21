from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Iterable

from .schema import LetterSchema


DPI = 96
MARGIN_BOTTOM = 25
MARGIN_TOP = 25
MARGIN_LEFT = 15
MARGIN_RIGHT = 15
BASE_CMD = (
    'wkhtmltopdf'
    ' --enable-local-file-access --enable-external-links'
    f' --dpi {DPI}'
    f' --margin-bottom {MARGIN_BOTTOM}mm'
    f' --margin-top {MARGIN_TOP}mm'
    f' --margin-left {MARGIN_LEFT}mm'
    f' --margin-right {MARGIN_RIGHT}mm'
    ' --footer-spacing 5 --footer-font-size 10'
).split()
BASE_FOOTER = 'Page [page] / [topage]'


def pdf_from_letters(*args: LetterSchema, letters=None):
    from .html import render_letter

    if not letters:
        letters = []
    letters = list(letters) + list(args)
    cmd = BASE_CMD.copy()
    with tempfile.TemporaryDirectory() as dir:
        dir = Path(dir)
        output = dir / 'output.pdf'
        for i, letter in enumerate(letters):
            path = dir / f'{i}.html'
            with path.open('w') as f:
                f.write(render_letter(letter))
            cmd += [
                str(path),
                '--footer-center',
                f'{BASE_FOOTER}\nID {letter.id} - {letter.email}'
            ]
        cmd += [str(output)]
        logs = subprocess.run(cmd, capture_output=True)
        print(logs.stdout)
        print(logs.stderr, file=sys.stderr)
        result = output.read_bytes()
    return result
