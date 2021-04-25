from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *





urlpatterns = [

    path('', auth_views.LoginView.as_view(template_name='project_app/login.html'), name='login'),
    path('register/', signup, name='register'),
    path('dashboard/', dashboard, name='dashboard'),

    path('write-topic/', write_topic, name='write_topic'),
    path('selected-topics/', selected_project, name='selected_project'),
    path('approve-deny-selected-topic/<int:pk>', confirm_project, name='confirm_project'),
    path('approved-topics', approved_topics, name='approved_topic'),
    path('denied-topics', denied_topics, name='denied_topics'),
    path('proposal-projects', proposal_projects, name='proposal_projects'),
    path('write-feedback/<int:pk>', write_feedback, name='write_feedback'),
    path('submitted-projects', submitted_projects, name='submitted_projects'),
    path('provide-feedback/<int:pk>', provide_feedback, name='provide_feedback'),
    path('add-project-materials', add_project_materials, name='add_project_materials'),
    path('feedback-materials/', all_feedback_materials, name='all_feedback_materials'),






    path('book-project/<int:pk>', book_project, name='book_project'),
    path('upload-proposal-project', upload_proposal, name='upload_proposal'),
    path('proposal-feedback', proposal_feedback, name='proposal_feedback'),
    path('no-proposal-feedback', no_proposal_feedback, name='no_proposal_feedback'),
    path('submit-project', submit_project, name='submit_project'),
    path('no-feedback', no_feedback, name='no_feedback'),
    path('project-submission-feedback', draft_feedback, name='draft_feedback'),
    path('no-draft-feedback', no_draft_feedback, name='no_draft_feedback'),
    path('project-materials', project_materials, name='project_materials'),
    path('add-feedback-materials/<int:pk>', feedback_materials, name='feedback_materials'),







]
