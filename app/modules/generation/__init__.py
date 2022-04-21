from app import Blueprint


bp = Blueprint(__name__, prefix=True)


from .html import render_letter
from .schema import LetterSchema
from .pdf import pdf_from_letters


@bp.route('/test')
def test():
    return render_letter(LetterSchema(
        content='lorem ipsum ' * 50,
        signature='signature',
        image_url='https://cataas.com/cat',
    ))
