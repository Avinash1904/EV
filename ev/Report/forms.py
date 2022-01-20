from django import forms
from .models import Report2 as Report
import datetime


class DateInput(forms.DateInput):
    input_type = "date"


class ReportForm(forms.ModelForm):
    # start_date = forms.DateField(initial=datetime.date.today)
    # end_date = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = Report
        fields = ["start_date", "end_date"]
        widgets = {
            "start_date": DateInput(),
            "end_date": DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial["start_date"] = datetime.date.today().isoformat()
        self.initial["end_date"] = datetime.date.today().isoformat()


class ReportListForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["start_date", "end_date", "report_csv"]
