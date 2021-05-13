from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import login as auth_login
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group



def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


def register_student(request):
    if request.method=='POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            return redirect('login')
    else:
        form = StudentSignUpForm()
    return render(request,'student/register.html',{'form':form})


@login_required
def register_teacher(request):
    form = TeacherSignUpForm()
    if request.method=='POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            return redirect('teachers')
    return render(request,'academic_affairs/register_teacher.html',{'form':form})




@login_required
def teachers(request):
    teachers = User.objects.filter(groups__name='TEACHER')
    return render(request, 'academic_affairs/teachers.html',{'teachers':teachers})



@login_required
def students(request):
    students = User.objects.filter(groups__name='STUDENT')
    return render(request, 'academic_affairs/students.html',{'students':students})



@login_required
def dashboard(request):
    if is_teacher(request.user):
        my_topics = Topic.objects.filter(teacher=request.user)
        return render(request,'teacher/dashboard.html', {'my_topics':my_topics})
    elif request.user.is_superuser:
        context = {
            'topics':Topic.objects.all().count(),
            'selected_topics':SelectedTopic.objects.filter(status="APPROVED").count(),
            'draft_projects':ProjectSubmission.objects.filter(status="DRAFT").count(),
            'final_projects':ProjectSubmission.objects.filter(status="FINAL").count(),
            'students':User.objects.filter(groups__name='STUDENT').count(),
            'teachers':User.objects.filter(groups__name='TEACHER').count()      
        }
        return render(request,'academic_affairs/dashboard.html',context)
    else:
        projects = Topic.objects.exclude(status='APPROVED').order_by('-id')
        assigned_project = SelectedTopic.objects.filter(student=request.user).filter(status='APPROVED').order_by('-id')
        return render(request,'student/dashboard.html',{'projects':projects, 'assigned_project':assigned_project})


@login_required
@user_passes_test(is_teacher)
def write_topic(request):
    if request.method == 'POST':
        form = ProposedProjectForm(request.POST)
        if form.is_valid():
            save_project = form.save(commit=False)
            save_project.teacher = request.user
            save_project.name = request.POST['name']
            save_project.description = request.POST['description']
            save_project.save()
            return redirect('dashboard')
    else:
        form = ProposedProjectForm()
    
    return render(request , 'teacher/create_topic.html', {'form':form})


@login_required
@user_passes_test(is_teacher)
def selected_project(request):
    selected_topics = SelectedTopic.objects.filter(project__teacher=request.user).filter(status='PENDING').order_by('-id')
    return render(request, 'teacher/selected_topic.html',{'selected_topics':selected_topics})


@login_required
@user_passes_test(is_teacher)
def confirm_project(request, pk):
    project = SelectedTopic.objects.get(id=pk)

    form = ConfirmProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        check_assigned_twice = SelectedTopic.objects.filter(student=project.student).filter(status='APPROVED').exists() and form.cleaned_data.get('status') == 'APPROVED'

        if check_assigned_twice:
            return render(request, 'teacher/approve.html',{'form':form, "error": "The student has another project assigned to him/her"})

        form.save()
        return redirect('selected_project')

    return render(request, 'teacher/approve.html',{'form':form})


@login_required
@user_passes_test(is_teacher)
def approved_topics(request):
    approved_topics = SelectedTopic.objects.filter(project__teacher=request.user).filter(status='APPROVED').order_by('-id')
    return render(request, 'teacher/approved_topics.html',{'approved_topics':approved_topics})



@login_required
@user_passes_test(is_teacher)
def denied_topics(request):
    denied_topics = SelectedTopic.objects.filter(project__teacher=request.user).filter(status='DENIED').order_by('-id')
    return render(request, 'teacher/denied_topics.html',{'denied_topics':denied_topics})


@login_required
@user_passes_test(is_teacher)
def proposal_projects(request):
    proposal_projects = ProjectProposal.objects.filter(status=False).filter(project__project__teacher=request.user).order_by('-id')
    return render(request, 'teacher/proposal_projects.html', {'proposal_projects':proposal_projects})



@login_required
@user_passes_test(is_teacher)
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

    return render(request, 'teacher/write_feedback.html',{'form':form, 'already_gave_feedback':already_gave_feedback})



@login_required
@user_passes_test(is_teacher)
def submitted_projects(request):
    draft_submitted_projects = ProjectSubmission.objects.filter(project__project__teacher=request.user).filter(status='DRAFT').order_by('-id')
    final_submitted_projects = ProjectSubmission.objects.filter(project__project__teacher=request.user).filter(status='FINAL').order_by('-id')

    return render(request, 'teacher/submitted_projects.html', {'draft_submitted_projects':draft_submitted_projects, 'final_submitted_projects':final_submitted_projects})




@login_required
@user_passes_test(is_teacher)
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

    return render(request, 'teacher/project_feedback.html',{'form':form,'already_gave_feedback':already_gave_feedback})



@login_required
@user_passes_test(is_teacher)
def add_project_materials(request):
    if request.method == 'POST':
        form = ProjectMaterialForm(request.POST or None, request.FILES, request=request)
        if form.is_valid():
            material = form.save(commit=False)
            material.teacher = request.user
            material.save()
            return redirect('dashboard')
    else:
        form = ProjectMaterialForm(request=request)
    return render(request, 'teacher/add_project_materials.html', {'form':form})



@login_required
@user_passes_test(is_teacher)
def all_feedback_materials(request):
    feedback_materials = ProjectMaterialsFeedback.objects.filter(project__teacher=request.user).order_by('-id')
    return render(request ,'teacher/all_feedback_materials.html',{'feedback_materials':feedback_materials})




########################################    Students     ########################################



@login_required
def book_project(request, pk):
    project = Topic.objects.get(id=pk)

    if request.method == 'POST':
        form = SelectedTopicForm(request.POST)
        if form.is_valid():

            check_book_twice = SelectedTopic.objects.filter(project=project).filter(student=request.user).exists()
            check_booked_before = SelectedTopic.objects.filter(project=project).filter(status='APPROVED').exists()

            if check_book_twice:
                return render(request, 'student/take_project.html',{'project':project, 'form':form, "error": "You can't select the same project twice"})
            elif check_booked_before:
                return render(request, 'student/take_project.html',{'project':project, 'form':form, "error_before": "This project has been already assigned to other student, try other projects"})

            book_project = form.save(commit=False)
            book_project.project = project
            book_project.student = request.user
            book_project.save()
            return redirect('dashboard')
    else:
        form = SelectedTopicForm()

    return render(request, 'student/take_project.html',{'project':project, 'form':form})



@login_required
def upload_proposal(request):
    if request.method == 'POST':
        form = ProjectProposalForm(request.POST or None, request.FILES, request=request)
        if form.is_valid():

            upload_proposal = form.save(commit=False)
            upload_proposal.student = request.user
            upload_proposal.save()
            return redirect('dashboard')
    else:
        form =  ProjectProposalForm(request=request)
    
    already_exist = ProjectProposal.objects.filter(student=request.user).exists()

    return render(request, 'student/upload_proposal.html',{'form':form, 'already_exist':already_exist})




@login_required
def proposal_feedback(request):
    try:
        feedback = ProposalFeedback.objects.get(project_proposal__student=request.user)
        return render(request ,'student/proposal_feedback.html',{'feedback':feedback})

    except:
        return redirect('no_proposal_feedback')




@login_required
def no_proposal_feedback(request):
    return render(request, 'student/no_proposal_feedback.html')



@login_required
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
                    return render(request, 'student/submit_project.html',{'form':form, 'error':status})

                submit_project = form.save(commit=False)
                submit_project.student = request.user
                submit_project.project = selected_topic
                
                submit_project.save()
                return redirect('dashboard')
        else:
            form = ProjectSubmissionForm() 
    else:
        return redirect('no_feedback')
    return render(request, 'student/submit_project.html',{'form':form})




@login_required
def no_feedback(request):
    return render(request, 'student/no_feedback.html')



@login_required
def project_submission_feedback(request):
    try:
        draft_feedback = ProjectSubmissionFeedback.objects.all().filter(project__student=request.user).filter(project__status='DRAFT').order_by('-id')
        final_feedback = ProjectSubmissionFeedback.objects.all().filter(project__student=request.user).filter(project__status='FINAL').order_by('-id')
        
        return render(request,'student/project_submission_feedback.html',{'draft_feedback':draft_feedback, 'final_feedback':final_feedback})
    except:
        return redirect('no_feedback_project_submission')




@login_required
def no_feedback_project_submission(request):
    return render(request, 'student/no_feedback_project_submission.html')




@login_required
def project_materials(request):
    materials = ProjectMaterial.objects.filter(project__student=request.user).order_by('-id')
    return render(request, 'student/project_materials.html',{'materials':materials})



@login_required
def feedback_materials(request, pk):
    material = ProjectMaterial.objects.get(id=pk)
    if request.method == 'POST':
        form = ProjectMaterialsFeedbackForm(request.POST or None, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user
            feedback.project = material
            feedback.save()
            return redirect('dashboard')
    else:
        form = ProjectMaterialsFeedbackForm()
    return render(request, 'student/feedback_materials.html',{'form':form})
