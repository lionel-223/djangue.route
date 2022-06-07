from pathlib import Path

from app import db
from app.models import Country, Language, Recipient
from app.utils.model import Model
from scripts.import_countries_and_langs import get_countries_data
from . import group, read_file


country_data = None


def get_language(d: dict):
    if 'lang' not in d:
        return None
    return db.session.get(Language, d['lang'])


def get_country(d: dict):
    global country_data
    if 'country' not in d:
        return None
    if not country_data:
        country_data = {
            x['Country']:
            x['Alpha-2 code']
            for x in get_countries_data()
        }
    country = country_data.get(d['country'])
    if not country:
        return None
    return db.session.get(Country, country)


def get_nb_letters(d: dict):
    try:
        female = int(d.get('nb_w', 0))
        male = int(d.get('nb_m', 0))
        return female + male
    except Exception:
        return None


def get_address(d: dict):
    address = d.get('address_1') or d.get('address')
    if address:
        address = address.strip()
    return address


class EhpadModel(Model):
    id = int
    email = Model.str(lower=True)
    name = Model.getter('title', type=str)
    phone = str
    receives_letters = Model.const(True)
    nb_letters = get_nb_letters
    frequency = Model.const(2)
    type = Model.const(Recipient.Types.RETIREMENT_HOME)
    status = Model.const(Recipient.Status.NOT_MODERATED)
    language = get_language

    country = get_country
    address = get_address
    zipcode = Model.getter('postal_code', type=str)
    city = str
    latitude = Model.getter('lattitude', type=float, cond=Model.true, default=None)
    longitude = Model.getter(type=float, cond=Model.true, default=None)



def import_ehpads(path: Path):
    data = read_file(path)
    for entry in data:
        obj_dict = EhpadModel.dict(entry)
        language = obj_dict.pop('language')
        obj_db = db.get_or_create(Recipient, obj_dict, ['id'])
        if language:
            obj_db.languages.append(language)
        db.session.commit()
        if db.Action.is_created():
            print('Added', obj_db)



@group.command('ehpads')
def ehpads(path: Path):
    import_ehpads(path)
