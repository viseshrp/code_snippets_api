from django.db import models

# Imports for formatting code
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# Create your models here.

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True,
                             default='', help_text='snippet title' )
    code = models.TextField(help_text='code content')
    linenos = models.BooleanField(default=False, help_text='display linenos')
    # choices = list of choices to display in the dropdown
    # of the form.
    # default = default value for the field
    language = models.CharField(choices=LANGUAGE_CHOICES,
                                default='python',
                                max_length=100,
                                help_text='chosen language')
    style = models.CharField(choices=STYLE_CHOICES,
                             default='friendly',
                             max_length=100,
                             help_text='chosen style')
    # User who created the snippet is a foreign key to
    # Django's auth.User table.
    # many to one relationship
    owner = models.ForeignKey('auth.User',
                              related_name='snippets',
                              on_delete=models.CASCADE)

    # field to store HTML representation of code
    highlighted = models.TextField()

    # override save, to format the code using pygments library
    # before saving it.

    def save(self, *args, **kwargs):
        """
        Use pygments to create highlighted html repr
        of code snippet

        :param args:
        :param kwargs:
        :return:
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style,
                                  linenos=linenos,
                                  full=True,
                                  **options)
        self.highlighted = highlight(self.code,
                                     lexer,
                                     formatter)
        super(Snippet, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)
