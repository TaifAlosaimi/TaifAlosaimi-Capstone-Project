
from datetime import timedelta
from zoneinfo import ZoneInfo

from django import forms
from django.core.validators import RegexValidator
from django.utils import timezone

from .models import Booking


SAUDI_TIMEZONE = ZoneInfo("Asia/Riyadh")


class BookingForm(forms.ModelForm):
    email = forms.EmailField(
        required=False,
        error_messages={
            "invalid": "يرجى إدخال بريد إلكتروني صحيح.",
        },
    )
    phone = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[
            RegexValidator(
                regex=r"^05[0-9]{8}$",
                message="رقم الجوال يجب أن يبدأ بـ 05 .",
            ),
        ],
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "inputmode": "numeric",
                "maxlength": "10",
                "placeholder": "05xxxxxxxx",
            }
        ),
        error_messages={
            "required": "يرجى إدخال رقم الجوال.",
            "min_length": "رقم الجوال يجب أن يتكون من 10 أرقام.",
            "max_length": "رقم الجوال يجب أن يتكون من 10 أرقام.",
        },
    )
    class Meta:
        model = Booking

        fields = [
            "name",
            "phone",
            "email",
            "event_type",
            "event_date",
            "event_location",
            "package",
            "notes",
        ]

        widgets = {
            "event_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "package": forms.RadioSelect(),
        }

        error_messages = {
            "name": {
                "required": "يرجى إدخال الاسم.",
            },
            "phone": {
                "required": "يرجى إدخال رقم الجوال.",
            },
            "event_type": {
                "required": "يرجى اختيار نوع المناسبة.",
                "invalid_choice": "يرجى اختيار نوع مناسبة صحيح.",
            },
            "event_date": {
                "required": "يرجى تحديد تاريخ المناسبة.",
                "invalid": "يرجى إدخال تاريخ صحيح.",
            },
            "event_location": {
                "required": "يرجى إدخال موقع المناسبة.",
            },
            "package": {
                "required": "يرجى اختيار الباقة المناسبة.",
                "invalid_choice": "يرجى اختيار باقة صحيحة.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.localdate(timezone=SAUDI_TIMEZONE)
        tomorrow = today + timedelta(days=1)

        self.fields["event_date"].widget.attrs["min"] = (
            tomorrow.isoformat()
        )

    def clean_event_date(self):
        event_date = self.cleaned_data.get("event_date")
        today = timezone.localdate(timezone=SAUDI_TIMEZONE)

        if event_date and event_date <= today:
            raise forms.ValidationError(
                "يجب اختيار تاريخ المناسبة من الغد وما بعده."
            )

        return event_date
