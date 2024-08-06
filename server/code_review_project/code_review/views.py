import logging
import pdb

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RepoSerializer, RepositoryAnalysisSerializer, FileAnalysisSerializer
from .services.repository_services import analyze_repository
from .models import RepositoryAnalysis, FileAnalysis
from .ai_analysis import analyze_code
import os

logger = logging.getLogger(__name__)

class RepoView(APIView):
    def post(self, request):
        serializer = RepoSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            context = serializer.validated_data.get('context', '')

            try:
                feedback, score, updated_file_structure, last_commit_hash = analyze_repository(url, context)

                return Response({
                    "feedback": feedback,
                    "score": score,
                    "file_structure": updated_file_structure,
                    "last_commit_hash": last_commit_hash
                }, status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(f"Error processing repository: {str(e)}")
                return Response({"error": f"Error processing repository: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnalysisDetailView(APIView):
    def get(self, request, repo_name):
        try:
            analysis = RepositoryAnalysis.objects.get(repo_name=repo_name)
            analysis_data = RepositoryAnalysisSerializer(analysis).data
            return Response(analysis_data, status=status.HTTP_200_OK)
        except RepositoryAnalysis.DoesNotExist:
            return Response({"error": "Repository analysis not found"}, status=status.HTTP_404_NOT_FOUND)

class FileContentView(APIView):
    def get(self, request, repo_name, file_path):
        try:
            file_full_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'services',
                'repositories', repo_name, file_path
            )

            if os.path.exists(file_full_path):
                with open(file_full_path, 'r') as file:
                    content = file.read()
                return Response({"content": content}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Error fetching file content: {str(e)}")
            return Response({"error": f"Error fetching file content: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FileAnalysisView(APIView):
    def post(self, request):
        try:
            file_name = request.data.get('fileName')
            file_path = request.data.get('filePath')
            content = request.data.get('content')

            analysis = analyze_code(content)

            file_analysis, created = FileAnalysis.objects.update_or_create(
                file_path=file_path,
                defaults={'analysis': analysis}
            )

            serializer = FileAnalysisSerializer(file_analysis)

            return Response({"analysis": analysis}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error analyzing file: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)