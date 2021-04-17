from django.db import models



class Student(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    field_study = models.CharField(max_length=120,choices=)
    sex = models.CharField(max_length=120, choices=)


class ProjectProposal(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    teacher = models.ForeignKey()


class Teacher(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    sex = models.CharField(max_length=120, choices=)


class Proposal(models.Model):
    student = models.ForeignKey(max_length=120)
    project = models.CharField(max_length=120)
    file = models.FileField(max_length=120)
    submitted_date = models.DateTimeField(auto_now_add=True)
 


class ProjectSubmission(models.Model):
    student = models.ForeignKey(max_length=120)
    project = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    thesis = models.FileField(max_length=120)
    link =
    project_images = multiple images
    status = models.CharField(max_length=100, choices= draft, final)
    submission_date =

 
