from typing import Optional
from app import models


class LetterSchema:
    """Standardized structure to use as a letter that can be converted to pdf"""

    def __init__(
        self,

        obj: Optional[models.Letter] = None,

        content: Optional[str] = None,
        signature: Optional[str] = None,
        greeting: Optional[str] = None,
        id: Optional[int] = None,
        email: Optional[str] = None,
        image_url: Optional[str] = None,

        raw_dict: Optional[dict] = None,
    ):
        if raw_dict:
            content = raw_dict.get('content', content)
            signature = raw_dict.get('signature', signature)
            greeting = raw_dict.get('greeting', greeting)
            id = raw_dict.get('id', id)
            email = raw_dict.get('email', email)
            image_url = raw_dict.get('image_url', image_url)

        self.signature = signature
        if greeting:
            self.content = f'{greeting}\n\n{content}'
        else:
            self.content = content
        self.id = id
        self.email = email
        self.image_url = image_url
        if obj:
            self.content = obj.content
            self.signature = obj.signature
            self.id = obj.id
            self.email = obj.email
            if obj.upload:
                self.image_url = obj.upload.url
        if not self.content:
            raise Exception('No content')

