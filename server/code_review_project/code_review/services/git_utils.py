import os
import re
import shutil
import logging
import pygit2
from pygit2 import Repository
from django.conf import settings

logger = logging.getLogger(__name__)

class CustomCallback(pygit2.RemoteCallbacks):
    def credentials(self, url, username_from_url, allowed_types):
        if allowed_types & pygit2.enums.CredentialType.USERNAME:
            return pygit2.Username("git")
        elif allowed_types & pygit2.enums.CredentialType.SSH_KEY:
            private_key_path = settings.GIT_SSH_KEY
            public_key_path = settings.GIT_SSH_KEY_PUBLIC
            if not os.path.isfile(private_key_path):
                raise FileNotFoundError(f"Private key file not found: {private_key_path}")
            return pygit2.Keypair("git", public_key_path, private_key_path, "")
        return None

def clone(repo, folder=None) -> Repository:
    logger.info(f"Cloning {repo} into {folder}")
    callbacks = CustomCallback()
    return pygit2.clone_repository(repo, folder, callbacks=callbacks)

def tree_walk(tree, prefix=[], content=False, excludes=[]):
    for e in tree:
        if not matches(e.name, excludes):
            if content and not e.is_binary:
                yield prefix, e, e.data.decode()
            else:
                yield prefix, e, None

            if e.type_str == "tree":
                yield from tree_walk(e, prefix=prefix + [e], content=content, excludes=excludes)

def matches(name, excludes):
    for ex in excludes:
        if isinstance(ex, str) and name == ex:
            return True
        elif isinstance(ex, re.Pattern) and ex.match(name):
            return True
    return False

def create_structure(file_structure):
    directory_structure = {}
    for parents, file, _ in file_structure:
        current_level = directory_structure
        for parent in parents:
            current_level = current_level.setdefault(parent.name, {})
        if file.type_str == "tree":
            current_level[file.name] = {}
        else:
            current_level[file.name] = None
    return directory_structure
