# code_review/serializers.py

from rest_framework import serializers
import re
from .models import RepositoryAnalysis, FileAnalysis


class RepositoryAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepositoryAnalysis
        fields = ['repo_name', 'url', 'context', 'feedback', 'score', 'updated_file_structure', 'last_commit_hash', 'updated_at']


class RepoSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=1000)
    context = serializers.CharField(max_length=1000, allow_blank=True,  required=False, default="")

    def validate_url(self, value):
        """
        Check that the URL is either a valid HTTP/HTTPS URL or a valid SSH URL.
        """
        http_pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        ssh_pattern = re.compile(
            r'^(git@[\w.-]+:[\w.-]+/[\w.-]+.git)$', re.IGNORECASE)

        if not http_pattern.match(value) and not ssh_pattern.match(value):
            raise serializers.ValidationError("Enter a valid HTTP/HTTPS or SSH URL.")
        return value

class FileAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAnalysis
        fields = ['file_path', 'analysis', 'updated_at']