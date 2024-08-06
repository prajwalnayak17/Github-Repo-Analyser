from django.db import models


class RepositoryAnalysis(models.Model):
    repo_name = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=1000)
    context = models.TextField(null=True, blank=True)
    feedback = models.TextField()
    score = models.FloatField()
    updated_file_structure = models.JSONField()
    last_commit_hash = models.CharField(max_length=255, null=True, blank=True)  # New field
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.repo_name

class FileAnalysis(models.Model):
    file_path = models.CharField(max_length=255, unique=True)
    analysis = models.JSONField()  # Store the analysis as JSON
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update the timestamp

    def __str__(self):
        return self.file_path
