from django.db import models

# Create your models here.

class Photo(models.Model):
    """ Model representing a receipt """
    title = models.CharField(max_length=200)
    # 'picture' field to upload the receipts
    picture = models.ImageField(upload_to='images/')
    # 'actual_date' field that records the actual date of receipt
    # null and blank are true as there may be no date in the receipt
    actual_date = models.DateField("Actual Date of Receipts", null=True, blank=True, help_text = "Enter in YYYY-MM-DD format") 
    extracted_date = models.DateField("OCR Extracted Date", null=True, blank=True)

    def __str__ (self):
        """String for representing the Model Object"""
        return self.title


