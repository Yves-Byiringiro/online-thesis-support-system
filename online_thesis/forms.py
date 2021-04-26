from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *




class TeacherSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['first_name','last_name','username','email','password']



class StudentSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your username'}))
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProposedProjectForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name','description']




class ConfirmProjectForm(forms.ModelForm):
    class Meta:
        model = SelectedTopic
        fields = ['status']

class ProposalFeedbackForm(forms.ModelForm):
    class Meta:
        model = ProposalFeedback
        fields = ['feedback_file','comment']


class ProjectSubmissionFeedbackForm(forms.ModelForm):
    class Meta:
        model =  ProjectSubmissionFeedback
        fields = ['report','comment']


class ProjectMaterialForm(forms.ModelForm):
    class Meta:
        model = ProjectMaterial
        fields = ['project','similar_topic_file']




#####################################           Students           #########################

class SelectedTopicForm(forms.ModelForm):
    class Meta:
        model = SelectedTopic
        fields = ['student_view']


class ProjectProposalForm(forms.ModelForm):
    class Meta:
        model = ProjectProposal
        fields = ['project','proposal_file','comment']


class ProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = ProjectSubmission
        fields = ['report','design_images','status']

class ProjectMaterialsFeedbackForm(forms.ModelForm):
    class Meta:
        model = ProjectMaterialsFeedback
        fields = ['similar_topic_file','comment']

