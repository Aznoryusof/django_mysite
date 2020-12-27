from django import forms


class ApprovalForm(forms.Form):
    Firstname=forms.CharField(
        max_length=15, 
        strip=True,
        widget=forms.TextInput(attrs={'placehoder': 'Enter Firstname'})
    )
    Lastname=forms.CharField(
        max_length=15, 
        strip=True,
        widget=forms.TextInput(attrs={'placehoder': 'Enter Lastname'})
    )
    Gender=forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')],
        required=True
    )
    Married=forms.ChoiceField(
        choices=[('Yes', 'Yes'), ('No', 'No')],
        required=True
    )
    Dependents=forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Number of Dependents'})
    )
    Education=forms.ChoiceField(
        choices=[('Graduate', 'Graduate'), ('Not_Graduate', 'Not_Graduate')],
        required=True
    )
    Self_Employed=forms.ChoiceField(
        choices=[('Yes', 'Yes'), ('No', 'No')],
        required=True
    )
    ApplicantIncome=forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Monthly Gross Income'})
    )
    CoapplicantIncome=forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Co-Applicant Monthly Gross Income'})
    )
    LoanAmount=forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Requested Loan Amount'})
    )
    Loan_Amount_Term=forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Loan Term in Months'})
    )
    Credit_History=forms.ChoiceField(
        choices=[('0', 0), ('1', 1), ('2', 2), ('3', 3)]
    )
    Property_Area=forms.ChoiceField(
        choices=[('Rural', 'Rural'), ('Semiurban', 'Semiurban'), ('Urban', 'Urban')],
        required=True
    )