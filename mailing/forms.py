from django.db.models import BooleanField
from django.forms import ModelForm
from mailing.models import Client, Message, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ('comment', 'owner')


class ClientModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ('comment', 'owner')


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class MessageModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = ('message',)

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user')
            super(MailingForm, self).__init__(*args, **kwargs)
            self.fields['clients'].queryset = Client.objects.filter(client_manager=user)
            self.fields['message'].queryset = Message.objects.filter(client_manager=user)


class MailingModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = ('message',)
