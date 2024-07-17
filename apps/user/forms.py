from django import forms

role_choices = (("1", "Administrator"), ("2", "Normal"))

user_role_choices = (("requester", "requester"), ("tasker", "tasker"))

walletType_choices = (("solana", "solana"), ("ethereum", "ethereum"))


class UserRegisterationStep1Form(forms.Form):
    wallet_address = forms.CharField(required=True)
    wallet_type = forms.CharField(required=True)
    avatar = forms.CharField(required=False)
    name = forms.CharField(required=True)
    nation = forms.CharField(required=True)

class UserRegisterationStep2Form(forms.Form):
    wallet_address = forms.CharField(required=True)
    wallet_type = forms.CharField(required=True)
    skills = forms.JSONField(required=False)
    desired_skills = forms.JSONField(required=False)


class UserLoginForm(forms.Form):
    request_nonce = forms.CharField(required=True)
    public_key = forms.CharField(required=True)
    wallet_type = forms.ChoiceField(choices=walletType_choices, required=True)
    signature = forms.CharField(required=False)


class UserExistForm(forms.Form):
    wallet_type = forms.CharField(required=True)
    public_key = forms.CharField(required=True)
