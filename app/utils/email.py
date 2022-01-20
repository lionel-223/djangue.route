# Function to simulate the sending of an email
# To be taken up when we start the real mailing !


def send_email(subject, sender, recipients, text_body):
    print(f'{subject} : {sender}')
    print(f'Envoyé à : {recipients}')
    print(f'Corps du message : {text_body}')
