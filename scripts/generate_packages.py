import tempfile
import subprocess
from datetime import datetime, timedelta

from sqlalchemy.sql.expression import func

from app import db
from app.models import Letter, Recipient, Package

MAX_MONTHS_SINCE_LETTER = 12  # We don't send letters that are more than MAX_MONTHS_SINCE_LETTER months old


def compute_limit_date_letters():
    today = datetime.utcnow()
    if MAX_MONTHS_SINCE_LETTER < today.month:
        return today.replace(month=(today.month - MAX_MONTHS_SINCE_LETTER),
                             day=1, hour=0, minute=0, second=0)
    else:
        return today.replace(year=today.year - 1,
                             month=12 + today.month - MAX_MONTHS_SINCE_LETTER,
                             day=1, hour=0, minute=0, second=0)


def generate_packages():
    recipients = db.session.query(Recipient).filter((Recipient.nb_letters > 0) &
                                                    (Recipient.status == Recipient.Status.approved))
    limit_date_letters = compute_limit_date_letters()
    for recipient in recipients:
        if recipient.needs_new_package:
            letters = db.session.query(Letter).filter((Letter.status == Letter.Status.approved) &
                                                      (Letter.created_at >= limit_date_letters) &
                                                      (Letter.id.not_in(recipient.received_letters)) &
                                                      (Letter.language_code.in_([
                                                          language.code for language in recipient.languages
                                                      ])))
            specific_letters = letters.filter_by(specific_recipient=recipient)
            nb_specific_letters = specific_letters.count()
            letters = letters.except_(specific_letters).order_by(func.random()).limit(
                recipient.nb_letters - nb_specific_letters)
            package = letters.union(specific_letters)
            print(f'Recipient {recipient.name}')
            print([letter.id for letter in package])
            html_package = [letter_to_html(letter=letter,
                                           template_path='../app/templates/letter.html',
                                           logo_path='app/static/logo/logo-150x.png')
                            for letter in package]
            html_package_to_pdf(html_package,
                                f"{recipient.id}_{recipient.name.replace(' ', '-')}_{datetime.today().date()}.pdf")


def letter_to_html(letter, template_path, logo_path):
    with open(template_path, "r") as f:
        html = f.read()

    html = html.replace("{{ logo_path }}", logo_path)
    html = html.replace("{{ letter.greeting }}", str(letter.greeting))
    html = html.replace("{{ letter.content }}", letter.content)
    html = html.replace("{{ letter.signature }}", letter.signature)
    return html


def html_package_to_pdf(html_package, output_path):
    temp_htmls = []
    for letter in html_package:
        temp_html = tempfile.NamedTemporaryFile(
            mode="w+", suffix=".html", delete=False, encoding="UTF-8"
        )
        temp_html.write(letter)
        temp_html.seek(0)
        temp_htmls.append(temp_html)
    letters_command = [
        [
            temp_html.name,
            "--encoding",
            "UTF-8",
            "--load-error-handling",
            "ignore",
            "--footer-center",
            "test footer",
            "--footer-spacing",
            "5",
            "--footer-font-size",
            "10",
            # "--debug-javascript",
        ]
        for temp_html in temp_htmls
    ]
    command = (
            [
                "wkhtmltopdf",
                # "--quiet",
                "--disable-smart-shrinking",
                "--enable-local-file-access",
                "--enable-external-links",
                "--javascript-delay",
                "10000",
                "--dpi",
                "96",
                "--margin-bottom",
                "25mm",
                "--margin-top",
                "25mm",
                "--margin-left",
                "15mm",
                "--margin-right",
                "15mm",
            ]
            + [c for l_c in letters_command for c in l_c]
            + [output_path]
    )
    subprocess.run(
        command, check=True, capture_output=True
    )
    for temp_file in temp_htmls:
        temp_file.close()


def main():
    generate_packages()


if __name__ == '__main__':
    main()
