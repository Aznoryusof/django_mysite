from django.db import models


class approvals(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    MARRIED_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    EDUCATION_CHOICES = (
        ('Graduate', 'Graduate'),
        ('Not_Graduate', 'Not_Graduate')
    )
    SELF_EMPLOYED_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    PROPERTY_AREA_CHOICES = (
        ('Rural', 'Rural'),
        ('Semiurban', 'Semiurban'),
        ('Urban', 'Urban')
    )


    Firstname=models.CharField(max_length=15)
    Lastname=models.CharField(max_length=15)
    Gender=models.CharField(max_length=15, choices=GENDER_CHOICES)
    Married=models.CharField(max_length=15, choices=MARRIED_CHOICES)
    Dependents=models.PositiveIntegerField(default=0)
    Education=models.CharField(max_length=15, choices=EDUCATION_CHOICES)
    Self_Employed=models.CharField(max_length=15, choices=SELF_EMPLOYED_CHOICES)
    ApplicantIncome=models.PositiveIntegerField(default=0)
    CoapplicantIncome=models.PositiveIntegerField(default=0)
    LoanAmount=models.PositiveIntegerField(default=0)
    Loan_Amount_Term=models.PositiveIntegerField(default=0)
    Credit_History=models.PositiveIntegerField(default=0)
    Property_Area=models.CharField(max_length=15, choices=PROPERTY_AREA_CHOICES)

    def __str__(self):
        return self.firstname, self.lastname