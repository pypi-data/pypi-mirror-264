from django import forms
from django.db import router
from django.db.models.deletion import Collector
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse


class BaseActionView(generic.FormView):
    viewset = None
    model = None

    def get_success_url(self):
        """Redirect back to the list view if no `success_url` is configured."""
        if self.success_url is None:
            opts = self.model._meta
            return reverse('{}:{}_list'.format(opts.app_label, opts.model_name))
        return super(BaseActionView, self).get_success_url()

    def get_objects(self):
        self.objects_pks = self.request.POST.getlist('pk')
        return self.model._default_manager.filter(pk__in=self.objects_pks)

    def get_form_class(self):
        class ActionForm(forms.Form):
            pk = forms.ModelMultipleChoiceField(
                queryset=self.model._default_manager.all(),
                widget=forms.MultipleHiddenInput)
        return ActionForm

    def form_not_confirmed(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.form = self.get_form()
        if self.form.is_valid():
            self.objects = self.form.cleaned_data['pk']
            if '_confirm' in self.request.POST:
                return self.form_valid(self.form)
            else:
                return self.form_not_confirmed(self.form)
        else:
            return self.form_invalid(self.form)


class DeleteActionView(BaseActionView):
    template_name_suffix = '_delete_action'

    def _get_deleted_objects(self):
        collector = Collector(using=router.db_for_write(self.model))
        collector.collect(self.objects)
        return collector.data

    def get_context_data(self, **kwargs):
        """Extend view context data.

        `{{ deleted_objects }}` - list of related objects to delete
        """
        if self.form.is_valid():
            kwargs.setdefault('deleted_objects', self._get_deleted_objects())
        return super(DeleteActionView, self).get_context_data(**kwargs)

    def get_template_names(self):
        """
        List of templates for the view.

        If no `self.template_name` defined, returns::

             [<app_label>/<model_label>_delete_action.html
              'material/frontend/views/delete_action.html']
        """
        if self.template_name is None:
            opts = self.model._meta
            return [
                '{}/{}{}.html'.format(
                    opts.app_label,
                    opts.model_name,
                    self.template_name_suffix),
                'material/frontend/views/delete_action.html',
            ]

        return [self.template_name]

    def form_valid(self, form):
        self.form.cleaned_data['pk'].delete()
        self.message_user()
        return HttpResponseRedirect(self.get_success_url())

    def message_user(self):
        message = "The objects was deleted successfully"
        messages.add_message(self.request, messages.SUCCESS, message, fail_silently=True)
