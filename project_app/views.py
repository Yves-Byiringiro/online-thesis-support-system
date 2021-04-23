from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import login as auth_login
from .models import *



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'project_app/register.html', {'form': form})


def dashboard(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProposedProjectForm(request.POST)
            if form.is_valid():
                save_project = form.save(commit=False)
                save_project.teacher = request.user
                save_project.save()
                return redirect('dashboard')
        else:
            form = ProposedProjectForm()
        
        return render(request, 'project_app/dashboard.html', {'form':form})

    else:  
        projects = Topic.objects.all().exclude(status='APPROVED')
        assigned_project = SelectedTopic.objects.get(student=request.user)


    return render(request, 'project_app/dashboard.html', {'projects':projects, 'assigned_project':assigned_project})




def selected_project(request):
    selected_project = SelectedTopic.objects.filter(project__teacher=request.user).filter(status='PENDING')
    return render(request, 'project_app/selected_project.html',{'selected_project':selected_project})


def confirm_project(request, pk):
    project = SelectedTopic.objects.get(id=pk)

    form = ConfirmProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        check_assigned_twice = SelectedTopic.objects.filter(student=project.student).filter(status='APPROVED').exists() and form.cleaned_data.get('status') == 'APPROVED'

        if check_assigned_twice:
            return render(request, 'project_app/confirm_denie_project.html',{'form':form, "error": "The student has another project assigned to him/her"})

        form.save()
        return redirect('selected_project')

    return render(request, 'project_app/confirm_denie_project.html',{'form':form})

def denied_project(request):
    denied_projects = SelectedTopic.objects.filter(project__teacher=request.user).filter(status='DENIED')

    return render(request, 'project_app/denied_projects.html',{'denied_projects':denied_projects})


def proposal_projects(request):
    proposal_projects = ProjectProposal.objects.all().filter(status=False)
    return render(request, 'project_app/proposal_projects.html', {'proposal_projects':proposal_projects})


def write_feedback(request, pk):
    project_proposal = ProjectProposal.objects.get(id=pk)

    if request.method == 'POST':
        form = ProposalFeedbackForm(request.POST or None, request.FILES)
        if form.is_valid():
            write_feedback = form.save(commit=False)
            write_feedback.teacher = request.user
            write_feedback.project_proposal = project_proposal
            write_feedback.save()
            return redirect('proposal_projects')
    else:
        form = ProposalFeedbackForm()
    
    already_gave_feedback = ProposalFeedback.objects.filter(project_proposal=project_proposal).exists()

    return render(request, 'project_app/write_feedback.html',{'form':form, 'already_gave_feedback':already_gave_feedback})



def submitted_projects(request):
    submitted_projects = ProjectSubmission.objects.all()
    return render(request, 'project_app/submitted_projects.html', {'submitted_projects':submitted_projects})



def provide_feedback(request, pk):
    project = ProjectSubmission.objects.get(id=pk)

    if request.method == 'POST':
        form = ProjectSubmissionFeedbackForm(request.POST or None, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.teacher = request.user
            feedback.project = project
            feedback.save()
            return redirect('proposal_projects')
    else:
        form = ProjectSubmissionFeedbackForm()

    already_gave_feedback = ProjectSubmissionFeedback.objects.filter(project=project).filter(project__status=project.status).exists()

    return render(request, 'project_app/provide_feedback.html',{'form':form,'already_gave_feedback':already_gave_feedback})



def add_project_materials(request):
    if request.method == 'POST':
        form = ProjectMaterialForm(request.POST or None, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.teacher = request.user
            material.save()
            return redirect('dashboard')
    else:
        form = ProjectMaterialForm()
    return render(request, 'project_app/add_project_materials.html', {'form':form})


def all_feedback_materials(request):
    feedback_materials = ProjectMaterialsFeedback.objects.filter(project__teacher=request.user)
    return render(request ,'project_app/all_feedback_materials.html',{'feedback_materials':feedback_materials})




########################################    Students     ########################################


def book_project(request, pk):
    project = Topic.objects.get(id=pk)

    if request.method == 'POST':
        form = SelectedTopicForm(request.POST)
        if form.is_valid():

            check_book_twice = SelectedTopic.objects.filter(project=project).filter(student=request.user).exists()

            if check_book_twice:
                return render(request, 'project_app/topic_proposal.html',{'project':project, 'form':form, "error": "You can't select the same project twice"})

            book_project = form.save(commit=False)
            book_project.project = project
            book_project.student = request.user
            book_project.save()
            return redirect('dashboard')
    else:
        form = SelectedTopicForm()

    return render(request, 'project_app/project_proposal.html',{'project':project, 'form':form})


def upload_proposal(request):
    if request.method == 'POST':
        form = ProjectProposalForm(request.POST or None, request.FILES)
        if form.is_valid():

            upload_proposal = form.save(commit=False)
            upload_proposal.student = request.user
            upload_proposal.save()
            return redirect('dashboard')
    else:
        form =  ProjectProposalForm()
    
    already_exist = ProjectProposal.objects.filter(student=request.user).exists()

    return render(request, 'project_app/upload_proposal.html',{'form':form, 'already_exist':already_exist})



def proposal_feedback(request):
    try:
        feedback = ProposalFeedback.objects.get(project_proposal__student=request.user)
        return render(request ,'project_app/proposal_feedback.html',{'feedback':feedback})

    except:
        return redirect('no_proposal_feedback')


def no_proposal_feedback(request):
    return render(request, 'project_app/no_proposal_feedback.html')


def submit_project(request):
    feedback = ProposalFeedback.objects.filter(project_proposal__student=request.user).exists()
    if feedback:
        selected_topic = SelectedTopic.objects.get(student=request.user)
        if request.method == 'POST':
            form = ProjectSubmissionForm(request.POST or None, request.FILES)
            if form.is_valid():
                status = form.cleaned_data.get('status')
                check_draft_exist = ProjectSubmission.objects.filter(student=request.user).filter(status=status).exists()

                if check_draft_exist:
                    return render(request, 'project_app/submit_project.html',{'form':form, 'error':status})

                submit_project = form.save(commit=False)
                submit_project.student = request.user
                submit_project.project = selected_topic
                
                submit_project.save()
                return redirect('dashboard')
        else:
            form = ProjectSubmissionForm() 
    else:
        return redirect('no_feedback')
    return render(request, 'project_app/submit_project.html',{'form':form})



def no_feedback(request):
    return render(request, 'project_app/no_feedback.html')

def draft_feedback(request):
    try:
        draft_feedback = ProjectSubmissionFeedback.objects.all().filter(project__student=request.user).filter(project__status='DRAFT')
        final_feedback = ProjectSubmissionFeedback.objects.all().filter(project__student=request.user).filter(project__status='FINAL')
        
        return render(request,'project_app/draft_feedback.html',{'draft_feedback':draft_feedback, 'final_feedback':final_feedback})
    except:
        return redirect('no_draft_feedback')

def no_draft_feedback(request):
    return render(request, 'project_app/no_draft_feedback.html')


def project_materials(request):
    materials = ProjectMaterial.objects.filter(project__student=request.user)
    return render(request, 'project_app/project_materials.html',{'materials':materials})

def feedback_materials(request, pk):
    material = ProjectMaterial.objects.get(id=pk)
    if request.method == 'POST':
        form = ProjectMaterialsFeedbackForm(request.POST or None, instance=material)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user
            feedback.project = material.project
            feedback.save()
            return redirect('dashboard')
    else:
        form = ProjectMaterialsFeedbackForm()
    return render(request, 'project_app/feedback_materials.html',{'form':form})
