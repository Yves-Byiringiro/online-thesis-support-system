from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *




class TeacherSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']



class StudentSignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ['username','email','password']



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
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProjectProposalForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = SelectedTopic.objects.filter(student=self.request.user).filter(status='APPROVED')



    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request')
    #     super(AddUserProfileForm, self).__init__(*args, **kwargs)
    #     self.fields['project_name'].queryset = Project.objects.exclude(
    #         project_name=self.request.user.user_profile.project_name)



class ProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = ProjectSubmission
        fields = ['report','design_images','status']

class ProjectMaterialsFeedbackForm(forms.ModelForm):
    class Meta:
        model = ProjectMaterialsFeedback
        fields = ['similar_topic_file','comment']

