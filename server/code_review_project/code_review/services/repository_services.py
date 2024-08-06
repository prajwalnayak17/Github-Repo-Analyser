import os
import re
import shutil
import json
import logging
from pygit2 import Repository
from .git_utils import clone, tree_walk, create_structure, CustomCallback
from ..repo_analysis import repo_analysis
from ..models import RepositoryAnalysis
from ..serializers import RepositoryAnalysisSerializer
from django.conf import settings

logger = logging.getLogger(__name__)

def analyze_repository(url, context=None):
    try:
        if url.startswith("http"):
            url_parts = url.split("/")
            owner, repo = url_parts[3], url_parts[4]
        else:
            ssh_pattern = re.compile(r'git@[\w.-]+:([\w.-]+)/([\w.-]+).git')
            match = ssh_pattern.match(url)
            if match:
                owner, repo = match.groups()
            else:
                raise ValueError("Invalid SSH URL")

        existing_repo = RepositoryAnalysis.objects.filter(repo_name=repo).first()

        app_dir = os.path.dirname(os.path.abspath(__file__))
        clone_folder = os.path.join(app_dir, "repositories", repo)

        if existing_repo:
            repo_instance = Repository(clone_folder)
            callbacks = CustomCallback()
            repo_instance.remotes['origin'].fetch(callbacks=callbacks)

            branch_name = 'main' if f'refs/remotes/origin/main' in repo_instance.references else 'master'
            if f'refs/remotes/origin/{branch_name}' not in repo_instance.references:
                raise Exception("Neither 'main' nor 'master' branch exists on the remote.")

            latest_commit_hash = str(repo_instance.references[f'refs/remotes/origin/{branch_name}'].target)

            if existing_repo.last_commit_hash != latest_commit_hash:
                shutil.rmtree(clone_folder)
                os.makedirs(clone_folder, exist_ok=True)
                cloned_repo = clone(url, clone_folder)
                branches = cloned_repo.listall_branches()
                repo_tree = cloned_repo.revparse_single(branch_name).tree

                excludes = [
                    "package.json", "package-lock.json", ".vscode",
                    "HelloWorld.vue", "TheWelcome.vue", "WelcomeItem.vue",
                    "base.css", re.compile(".*\\.svg"), re.compile(".*\\.mp3"),
                    re.compile(".*\\.png"), re.compile(".*\\.jpg"),
                    re.compile(".*\\.jpeg"), re.compile(".*\\.webp"),
                    re.compile(".*\\.ico"), re.compile(".*\\.odt")
                ]
                file_structure = list(tree_walk(repo_tree, content=False, excludes=excludes))
                directory_structure = create_structure(file_structure)
                analysis_response = repo_analysis(directory_structure)
                analysis_json = json.loads(analysis_response)

                existing_repo.feedback = analysis_json['feedback']
                existing_repo.score = analysis_json['score']
                existing_repo.updated_file_structure = directory_structure
                existing_repo.last_commit_hash = latest_commit_hash
                existing_repo.save()

                return analysis_json['feedback'], analysis_json['score'], analysis_json['updated_file_structure'], latest_commit_hash
            else:
                return existing_repo.feedback, existing_repo.score, existing_repo.updated_file_structure, existing_repo.last_commit_hash
        else:
            if os.path.exists(clone_folder):
                shutil.rmtree(clone_folder)
            os.makedirs(clone_folder, exist_ok=True)
            cloned_repo = clone(url, clone_folder)
            branches = cloned_repo.listall_branches()
            repo_tree = cloned_repo.revparse_single('main' if 'main' in branches else 'master').tree

            excludes = [
                "package.json", "package-lock.json", ".vscode",
                "HelloWorld.vue", "TheWelcome.vue", "WelcomeItem.vue",
                "base.css", "node_modules", re.compile(".*\\.svg"), re.compile(".*\\.mp3"),
                re.compile(".*\\.png"), re.compile(".*\\.jpg"),
                re.compile(".*\\.jpeg"), re.compile(".*\\.webp"),
                re.compile(".*\\.ico"), re.compile(".*\\.odt")
            ]
            file_structure = list(tree_walk(repo_tree, content=False, excludes=excludes))
            directory_structure = create_structure(file_structure)
            analysis_response = repo_analysis(directory_structure)
            analysis_json = json.loads(analysis_response)

            analysis_data = {
                'repo_name': repo,
                'url': url,
                'context': context or None,
                'feedback': analysis_json['feedback'],
                'score': analysis_json['score'],
                'updated_file_structure': directory_structure,
                'last_commit_hash': str(cloned_repo.head.target)
            }

            analysis_serializer = RepositoryAnalysisSerializer(data=analysis_data)
            if analysis_serializer.is_valid():
                analysis_serializer.save()
            else:
                logger.error(f"Error saving analysis data: {analysis_serializer.errors}")
                raise Exception("Error saving analysis data")

            return analysis_json['feedback'], analysis_json['score'], directory_structure, analysis_data['last_commit_hash']

    except Exception as e:
        logger.error(f"Error processing repository: {str(e)}")
        raise e
