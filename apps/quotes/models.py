from __future__ import unicode_literals
from django.db import models
from ..login_registration.models import User

class QuoteManager(models.Manager):
    # creates new quotes given that the quote passes all validation tests
    def post_quote(self,postData, user_id):
        errors = self.validate(postData)
        if not errors:
            posted_by = User.objects.get(id=user_id)
            quote = Quote.objects.create(
                quote=postData['quote'],
                author=postData['author'],
                posted_by=posted_by
            )
            return quote
        else:
            return errors

    # adds quote to user's favorites list
    def add_to_list(self, quote_id, user_id, first_name, last_name):
        liker = Liker.objects.create(
            quote=Quote.objects.get(id=quote_id),
            user=User.objects.get(id=user_id),
            first_name=first_name,
            last_name=last_name
        )
        return liker

    # determines whether user input for quotes is valid
    def validate(self, postData):
        errors = []
        if len(postData['quote']) < 10:
            errors.append("Quote must be longer than 10 characters!")
        if len(postData['author']) < 3:
            errors.append("Author Name must be longer than 3 characters!")
        return errors

class Quote(models.Model):
    quote = models.TextField(max_length=1000)
    author = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name='poster')
    liked_by = models.ManyToManyField(User, through='Liker')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    def __str__(self):
        return "{}: {}".format(self.author, self.quote)

class Liker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    quote = models.ForeignKey(Quote)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
