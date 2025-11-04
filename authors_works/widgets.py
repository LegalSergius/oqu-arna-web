from django import forms
from django.forms import Widget, Select, RadioSelect, FileInput


class InputGroupText(Widget):
    template_name = 'widgets/input_group.html'

    def __init__(self, text='', input_type='text', default="", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.input_type = input_type
        self.default = default

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'group_text': self.text,
            'input_type': self.input_type,
            'default': self.default,
        })

        return context

class SelectInput(Select):
    template_name = 'widgets/select_input.html'

    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'group_text': self.text,
        })

        return context

class RadioInput(RadioSelect):
    template_name = 'widgets/radio_input.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class CustomFileInput(FileInput):
    template_name = 'widgets/input_file.html'
