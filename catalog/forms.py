from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class RenewBookForm(forms.Form):
	renewal_date = forms.DateField(help_text="현재 날짜부터 4주 후 날짜까지 선택 가능합니다(기본 3일).")

	def clean_renewal_date(self):
		data = self.cleaned_data['renewal_date']

		if data < datetime.date.today():
			raise ValidationError(_('현재 시간보다 과거를 선택하셨습니당'))

		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('4주를 초과하셨습니당'))

		return data


from django.forms import ModelForm
from .models import BookInstance


class RenewBookModelForm(ModelForm):
	def clean_due_back(self):
		data = self.cleaned_data['due_back']

		if data < datetime.date.today():
			raise ValidationError(_('현재 시간보다 과거를 선택하셨습니당'))

		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('4주를 초과하셨습니당'))
		return data

	class Meta:
		model = BookInstance
		fields = ['due_back',]
		labels = { 'due_back':_('수정 날짜'),}
		help_texts = {'due_back':_('현재 날짜부터 4주 후 날짜까지 선택 가능합니다(기본 3일).'),}