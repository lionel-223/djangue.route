from app import Blueprint


bp = Blueprint(__name__)

from .forms.letter import LetterForm
from .forms.login import LoginForm, RegistrationForm
from .forms.recipient import RecipientForm
from .forms.contact import ContactForm
from .routes import index, login, write, recipient, recipient_list, contact
