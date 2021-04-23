from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    PROJECT_STATUS = (
        ('PENDING','PENDING'),
        ('DENIED','DENIED'),
        ('APPROVED','APPROVED'),

    )
    name = models.CharField(max_length=300)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=300, choices=PROJECT_STATUS, default='PENDING')

    def __str__(self):
        return self.name
    



class SelectedTopic(models.Model):
    PROJECT_STATUS = (
        ('PENDING','PENDING'),
        ('DENIED','DENIED'),
        ('APPROVED','APPROVED'),

    )
    project = models.ForeignKey(Topic, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    student_view = models.TextField()
    status = models.CharField(max_length=300, choices=PROJECT_STATUS, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}  <-----------------> {}'.format(self.project.name, self.student.username)


class ProjectProposal(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(SelectedTopic, on_delete=models.CASCADE)
    proposal_file = models.FileField(upload_to='proposal_files', blank=False)
    comment = models.TextField(blank=True, max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


class ProposalFeedback(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    project_proposal = models.ForeignKey(ProjectProposal, on_delete=models.CASCADE)
    feedback_file = models.FileField(upload_to='feedback_files',blank=True)
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

class ProjectSubmission(models.Model):
    STATUS = (
        ('DRAFT','DRAFT'),
        ('FINAL','FINAL')

    )
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(SelectedTopic, on_delete=models.CASCADE)
    report = models.FileField(upload_to='report_files')
    design_images = models.ImageField(upload_to='design_images')
    status = models.CharField(max_length=300, choices=STATUS , default='DRAFT')
    date = models.DateTimeField(auto_now_add=True)



class ProjectSubmissionFeedback(models.Model):
    project = models.ForeignKey(ProjectSubmission, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.FileField(upload_to='report_files')
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)



class ProjectMaterial(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(SelectedTopic, on_delete=models.CASCADE)
    similar_topic_file = models.FileField(upload_to='similar_topic_file')
    date = models.DateTimeField(auto_now_add=True)



class ProjectMaterialsFeedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaterial, on_delete=models.CASCADE)
    similar_topic_file = models.FileField(upload_to='similar_topic_file')
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)












# class Student(models.Model):
#     first_name = models.CharField(max_length=120)
#     last_name = models.CharField(max_length=120)
#     email = models.CharField(max_length=120)
#     phone_number = models.CharField(max_length=120)
#     field_study = models.CharField(max_length=120,choices=)
#     sex = models.CharField(max_length=120, choices=)


# class ProjectProposal(models.Model):
#     title = models.CharField(max_length=120)
#     description = models.TextField()
#     teacher = models.ForeignKey()


# class Teacher(models.Model):
#     first_name = models.CharField(max_length=120)
#     last_name = models.CharField(max_length=120)
#     email = models.CharField(max_length=120)
#     phone_number = models.CharField(max_length=120)
#     sex = models.CharField(max_length=120, choices=)


# class Proposal(models.Model):
#     student = models.ForeignKey(max_length=120)
#     project = models.CharField(max_length=120)
#     file = models.FileField(max_length=120)
#     submitted_date = models.DateTimeField(auto_now_add=True)
 


# class ProjectSubmission(models.Model):
#     student = models.ForeignKey(max_length=120)
#     project = models.CharField(max_length=120)
#     description = models.CharField(max_length=120)
#     thesis = models.FileField(max_length=120)
#     link =
#     project_images = multiple images
#     status = models.CharField(max_length=100, choices= draft, final)
#     submission_date =

 
