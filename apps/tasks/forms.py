from django import forms


class ChatForm(forms.Form):
    task_id = forms.CharField(required=False)
    message = forms.CharField(required=True)
    history = forms.JSONField(required=False)


class SubmissionForm(forms.Form):
    task_id = forms.CharField(required=True)
    description = forms.CharField(required=True)
    upload_paths = forms.JSONField(required=False)


class FeedbackForm(forms.Form):
    is_feedback = forms.BooleanField(required=True)
    content = forms.CharField(required=False)
    rate = forms.IntegerField(required=False)
