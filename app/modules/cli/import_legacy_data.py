"""
Legacy data refers to data that has been exported directly from the old db,
using WordPress columns
"""

import click
import csv
import traceback
from progress.bar import Bar

from app import db
from app.models import Letter
from . import bp

class Bar(Bar):
    suffix = '%(index)s/%(max)s %(percent).1f%% ETA: %(eta_td)s'

class LetterParser:
    countries = None

    class Row:
        def __init__(self, data: list):
            self.form_id = int(data[1])
            if self.form_id != 2:
                self.type = None
                return
            self.entry_id = int(data[2])
            type_id = data[3]
            self.type = {
                    "3": "email",
                    "4": "gender",
                    "6": "greeting",
                    "9": "content",
                    "10": "signature",
                    "21": "greeting",
                    "15": "image",
                    "24.3": "city",
                    "24.5": "zipcode",
                    "24.6": "country",
                    "28": "language_code",
                    "43.1": "allow_reuse",
                    "44": "event",
                    "46": "signature",
                    "55": "image",

                    "edit_lock": None,
                    "29": None, # Harvard longest letter event
                    "32": None, # recipient "random" or "choose"
                    "35": None, # recipient coordinates
                    "36": None, # recipient ID
                    "37": None, # recipient name
                    "38": None, # feedback_track
                    "39": None, # School
                    "42.1": None, # rgpd
            }.get(type_id, 'unknown')
            if len(type_id) > 10:
                # probably a picture
                self.type = None
            self.content = data[4]
            if self.type == 'unknown':
                raise Exception(f'Unknown type {type_id} with content {self.content}')
            if self.type == "event":
                if self.content == "0":
                    self.content = None
            if self.type == "gender":
                self.type = "is_male"
                self.content = any(x in self.content.lower() for x in ("monsieur"))
            if self.type == "allow_reuse":
                self.content = self.content != None
            if self.type == "country":
                # Country field is language dependant
                self.type = None
                return

    current = None
    queue = set()


    @classmethod
    def from_row(cls, row):
        if not cls.current or row.entry_id != cls.current.id:
            if cls.current:
                cls.queue.add(cls.current)
            cls.current = db.get_or_create(Letter, {'id': row.entry_id}, stage=False)
            cls.current.allow_reuse = False
            cls.current.language_code = "fr"
            cls.current.country_code = "FR"
        setattr(cls.current, row.type, row.content)
        return cls.current

    @staticmethod
    def print_letter(letter: Letter):
        print('\n'.join(
            f'{k}: {v}' for k, v
            in letter.__dict__.items()
        ))

    @classmethod
    def from_data(cls, data):
        result = []
        for row in Bar('Parsing', max=2390065).iter(data):
            try:
                row = cls.Row(row)
                if not row.type:
                    continue
            except Exception as e:
                print(e)
                continue
            cls.from_row(row)
            while cls.queue:
                letter = cls.queue.pop()
                result.append(letter)
                try:
                    db.session.add(letter)
                    db.session.commit()
                except Exception:
                    db.session.rollback()
                    traceback.print_exc()
                    cls.print_letter(letter)
        return result

@bp.cli.command("import-legacy")
@click.argument('path')
def import_file(path: str):
    f = open(path)
    reader = csv.reader(f)
    # data = list(reader)
    data = reader
    letters = LetterParser.from_data(data)
    # db.session.commit()
    f.close()
