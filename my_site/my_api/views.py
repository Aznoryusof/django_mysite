import os, sys
main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(main_dir)

import numpy as np
import pandas as pd

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from src.predictor.predict import make_prediction
from django.shortcuts import render
from django.http import JsonResponse
from .models import approvals
from .forms import ApprovalForm
from .serializers import approvalsSerializers
from django.contrib import messages


class ApprovalsView(viewsets.ModelViewSet):
    queryset = approvals.objects.all()
    serializer_class = approvalsSerializers


#@api_view(["POST"])
def approvereject(request):
    try:
        mydata = request.data
        mydata_df = pd.DataFrame(mydata, index=[0])
        mydata_df = mydata_df.drop(["Firstname", "Lastname"], axis=1)
        result_df = pd.DataFrame(make_prediction(mydata_df), columns=["Status"], index=[0])
        return JsonResponse('Your Status is {}'.format(result_df), safe=False)      
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


def cxcontact(request):
    if request.method=="POST":
        form=ApprovalForm(request.POST)
        if form.is_valid():
            Firstname=form.cleaned_data['Firstname']
            Lastname=form.cleaned_data['Lastname']
            Gender=form.cleaned_data['Gender']
            Married=form.cleaned_data['Married']
            Dependents=form.cleaned_data['Dependents']
            Education=form.cleaned_data['Education']
            Self_Employed=form.cleaned_data['Self_Employed']
            ApplicantIncome=form.cleaned_data['ApplicantIncome']
            CoapplicantIncome=form.cleaned_data['CoapplicantIncome']
            LoanAmount=form.cleaned_data['LoanAmount']
            Loan_Amount_Term=form.cleaned_data['Loan_Amount_Term']
            Credit_History=form.cleaned_data['Credit_History']
            Property_Area=form.cleaned_data['Property_Area']

            input_dict = (request.POST).dict()
            input_df = pd.DataFrame(input_dict, index=[0])
            input_df = input_df.drop(["Firstname", "Lastname", "csrfmiddlewaretoken"], axis=1)
            int_cols = [
                "Dependents", "ApplicantIncome", "CoapplicantIncome",
                "LoanAmount", "Loan_Amount_Term", "Credit_History"
            ]
            for col in int_cols:
                input_df[col] = input_df[col].astype(np.int64)
            result_df = pd.DataFrame(make_prediction(input_df), columns=["Status"], index=[0])
            if input_df['LoanAmount'][0] < 25000:
                messages.success(request, 'Application Status: {}'.format(result_df["Status"][0]))
            else:
                messages.success(request, 'Invalid: Your Loan Request Exceeds the $25,000 Limit')           

    form=ApprovalForm()

    return render(request, 'my_form/cxform.html', {'form':form})

