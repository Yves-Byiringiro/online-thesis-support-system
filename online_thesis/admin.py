from django.contrib import admin
from .models import *



admin.site.register(Topic)
admin.site.register(SelectedTopic)

admin.site.register(ProjectProposal)
admin.site.register(ProposalFeedback)

admin.site.register(ProjectSubmission)
admin.site.register(ProjectSubmissionFeedback)

admin.site.register(ProjectMaterial)
admin.site.register(ProjectMaterialsFeedback)