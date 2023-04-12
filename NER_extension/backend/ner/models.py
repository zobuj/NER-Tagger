from django.db import models

# Create your models here.


class Paragraph(models.Model):
    content = models.TextField()
    modified_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.content[:50]