from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

#Two ways to work with forms pure forms.Form or simpler, forms.ModelForm
#forms serve same role as html pages.
class RenewBookForm(forms.Form): 
	renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

	def clean_renewal_date(self):
		data = self.cleaned_data['renewal_date']
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - renewal date in the past'))
		if data > datetime.date.today() + datetime.timedelta(weeks=4): 
			raise ValidationError(_('Invalid date - renewal time more than 4 weeks ahead'))
		return data

from django.forms import ModelForm
from .models import BookInstance

"""

class RenewBookModelForm(ModelForm):
	def clean_due_back(self):
		data = self.cleaned_data['due_back']
		if data < datetime.date.today(): 
			raise ValidationError(_("Invalid date"))
		return data
	class Meta:
		model = BookInstance
		fields = ['due_back']
		labels = {'due_back': _('Renewal date'), }
		help_texts = { 'due_back ': _('Enter date'), }

"""


