from django.db import models

from django.db import models

class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pdf_file.name
