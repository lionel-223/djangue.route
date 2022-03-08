import os
import subprocess
import tempfile

from datetime import datetime
from flask import render_template

import app
from . import bp
from app import db
from app.models import Recipient, Package
from app.utils.email import send_email

MAX_MONTHS_SINCE_LETTER = 12  # We don't send letters that are more than MAX_MONTHS_SINCE_LETTER months old
LOGO_PATH = os.path.join(app.APP_FOLDER, 'static', 'logo', 'logo-150x.png')
LETTER_CSS = os.path.join(app.APP_FOLDER, 'static', 'letter.css')


def compute_limit_date_letters():
    today = datetime.utcnow()
    if MAX_MONTHS_SINCE_LETTER < today.month:
        return today.replace(month=(today.month - MAX_MONTHS_SINCE_LETTER),
                             day=1, hour=0, minute=0, second=0)
    else:
        return today.replace(year=today.year - 1,
                             month=12 + today.month - MAX_MONTHS_SINCE_LETTER,
                             day=1, hour=0, minute=0, second=0)


@bp.cli.command("generate-packages")
def generate_packages():

    today = datetime.utcnow().date()
    upload_directory = os.path.join(app.PDF_UPLOAD_FOLDER, str(today.year), str(today.month))
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)

    recipients = db.session.query(Recipient).filter((Recipient.nb_letters > 0) &
                                                    (Recipient.status == Recipient.Status.approved))
    limit_date_letters = compute_limit_date_letters()
    for recipient in recipients:
        if recipient.needs_new_package:
            print(f"Generating package for recipient {recipient.name} (id: {recipient.id})...")
            package, is_complete = recipient.generate_package(limit_date=limit_date_letters)
            if not package:
                print("No letters found for this recipient.")
                continue
            html_package = [
                {
                    "html": render_template('letter.html', letter=letter, logo_path=LOGO_PATH, css_path=LETTER_CSS,
                                            image_path=os.path.join(app.FILE_UPLOAD_FOLDER,
                                                                    letter.upload_hash + letter.upload.extension)
                                                        if letter.upload_hash else None
                                            ),
                    "id": letter.id,
                    "author_email": letter.email
                }
                for letter in package
            ]
            filename = f"{recipient.id}_{recipient.name.replace(' ', '-')}_{today}.pdf"
            filepath = os.path.join(upload_directory, filename)
            html_package_to_pdf(html_package, filepath)
            print("PDF generated")
            db.session.add(Package(file=filename,
                                   recipient=recipient,
                                   letters=[letter for letter in package],
                                   is_complete=is_complete))
            db.session.commit()
            print("Database updated")
            email_body = f"Vos lettres sont disponibles ici: {filepath}"
            if not is_complete:
                email_body += f"\nNous n'avons pas reçu assez de lettres pour vous envoyer les {recipient.nb_letters}" \
                              f" lettres demandées, vous n'en trouverez que {package.count()} dans ce PDF."
            send_email(subject="Vos lettres 1 Lettre 1 Sourire",
                       sender="admin@1lettre1sourire.org",
                       recipients=[user.email for user in recipient.users],
                       text_body=email_body)
            print("Package sent")


def html_package_to_pdf(html_package, output_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        for letter in html_package:
            path_tempfile = os.path.join(tmpdir, f"{str(letter['id'])}.html")
            with open(path_tempfile, "w") as temp_file:
                temp_file.write(letter["html"])
            letter['temp_file'] = path_tempfile
        letters_command = [
            [
                letter['temp_file'],
                "--footer-center",
                f"Page [page] sur [topage] \t-\t Lettre n° {letter['id']} \t-\t {letter['author_email']}",
            ]
            for letter in html_package
        ]
        command = (
                [
                    "wkhtmltopdf",
                    "--enable-local-file-access",
                    "--enable-external-links",
                    "--encoding",
                    "UTF-8",
                    "--load-error-handling",
                    "ignore",
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
                    "--footer-spacing",
                    "5",
                    "--footer-font-size",
                    "10",
                ]
                + [c for l_c in letters_command for c in l_c]
                + [output_path]
        )
        subprocess.run(
            command, check=True, capture_output=True
        )


def main():
    generate_packages()


if __name__ == '__main__':
    main()
