from django import forms
from django.template import loader


class TemplateWidget(forms.Widget):
    """
    Template based widget. It renders the ``template_name`` set as attribute
    which can be overridden by the ``template_name`` argument to the
    ``__init__`` method.
    """

    field = None
    template_name = None
    value_context_name = None

    def __init__(self, *args, **kwargs):
        template_name = kwargs.pop('template_name', None)
        if template_name is not None:
            self.template_name = template_name
        super(TemplateWidget, self).__init__(*args, **kwargs)
        self.context_instance = None

    def get_context_data(self):
        return {}

    def get_context(self, name, value, attrs=None):
        context = {
            'name': name,
            'hidden': self.is_hidden,
            'required': self.is_required,
            # In our case ``value`` is the form or formset instance.
            'value': value,
        }
        if self.value_context_name:
            context[self.value_context_name] = value

        if self.is_hidden:
            context['hidden'] = True

        context.update(self.get_context_data())
        context['attrs'] = self.build_attrs(attrs)

        return context

    def render(self, name, value, attrs=None, **kwargs):
        template_name = kwargs.pop('template_name', None)
        if template_name is None:
            template_name = self.template_name
        context = self.get_context(name, value, attrs=attrs or {}, **kwargs)
        return loader.render_to_string(
            template_name,
            dictionary=context,
            context_instance=self.context_instance)


class FormWidget(TemplateWidget):
    template_name = 'superform/formfield.html'
    value_context_name = 'form'


class FormSetWidget(TemplateWidget):
    template_name = 'superform/formsetfield.html'
    value_context_name = 'formset'


class AjaxModelSelect(forms.TextInput):
    """A widget for ModelChoiceField with ajax based autocomplete.

    To get AJAX results, GET requests with the additional
    `X-Requested-Content=Autocomplete` http header are performed to the same url as
    the form view.

    Expected response is json like::

        {
            suggestions: [
                { value: 'Chicago Blackhawks', data: { id: 1 } },
                { value: 'Chicago Bulls', data: { id: 2 } }
            ]
        ]

    :keyword lookups: list of field to query a model

    Example::

        class AddressForm(forms.Form):
            city = forms.ModelChoiceField(
                queryset=models.City.objects.all(),
                widget=AjaxModelSelect(loopups=['name__icontains'])
            )

    """
    def __init__(self, *args, **kwargs):
        self.lookups = kwargs.pop('lookups', None)
        if not self.lookups:
            raise ValueError('AjaxModelSelect need `lookups` to be provided')
        super(AjaxModelSelect, self).__init__(*args, **kwargs)


class AjaxMultipleModelSelect(forms.TextInput):
    """A widget for ModelMultipleChoiceField with ajax based autocomplete.

    .. seealso::
        :class: material.form.widgets.AjaxModelSelect

    """
    def __init__(self, *args, **kwargs):
        self.lookups = kwargs.pop('lookups', None)
        if not self.lookups:
            raise ValueError('AjaxMultiModelSelect need `lookups` to be provided')
        super(AjaxMultipleModelSelect, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
        except AttributeError:
            getter = data.get
        return getter(name)


class MediumEditorWidget(forms.TextInput):
    """A WYSIWYG editor widget.

    Example::

        class OceanViewSet(ModelViewSet):
            model = models.Ocean
            form_widgets = {
                'description': MediumEditorWidget(
                    options={
                        'targetBlank': True,
                        'toolbar': {
                            'buttons': ['h1', 'h2', 'h3', 'bold', 'italic', 'quote'],
                        },
                        'placeholder': {'text': 'Click to edit'}
                    },
                )
            }

    .. seealso::
        https://github.com/yabwe/medium-editor
    """
    def __init__(self, options=None, *args, **kwargs):
        self.options = options
        super(MediumEditorWidget, self).__init__(*args, **kwargs)


class DependentModelSelect(forms.Select):
    component = 'dmc-dependent-select'

    def __init__(self, *args, **kwargs):
        self.depends_on = kwargs.pop('depends_on', None)
        self.queryset = kwargs.pop('queryset', None)

        if not self.depends_on or self.queryset is None:
            raise ValueError('DependentModelSelect need both depends_on and queryset been provided')
        super().__init__(*args, **kwargs)
        self.attrs['data-parent'] = self.depends_on
