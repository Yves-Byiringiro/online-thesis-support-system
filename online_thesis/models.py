from django.db import models
from django.contrib.auth.models import User
import os




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

    def snippet(self):
        return self.description[:200] + '...'

    def snippet2(self):
        return self.description[:400] + '...'

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
        return self.project.name


class ProjectProposal(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(SelectedTopic, on_delete=models.CASCADE)
    proposal_file = models.FileField(upload_to='proposal_files', blank=False)
    comment = models.TextField(blank=True, max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def filename(self):
        return os.path.basename(self.proposal_file.name)


class ProposalFeedback(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    project_proposal = models.ForeignKey(ProjectProposal, on_delete=models.CASCADE)
    feedback_file = models.FileField(upload_to='feedback_files',blank=True)
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def filename(self):
        return os.path.basename(self.feedback_file.name)


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

    def filename(self):
        return os.path.basename(self.report.name)

    def design(self):
        return os.path.basename(self.design_images.name)


class ProjectSubmissionFeedback(models.Model):
    project = models.ForeignKey(ProjectSubmission, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.FileField(upload_to='report_files')
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.report.name)


class ProjectMaterial(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(SelectedTopic, on_delete=models.CASCADE)
    similar_topic_file = models.FileField(upload_to='similar_topic_file')
    date = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.similar_topic_file.name)



class ProjectMaterialsFeedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectMaterial, on_delete=models.CASCADE)
    similar_topic_file = models.FileField(upload_to='similar_topic_file')
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.similar_topic_file.name)