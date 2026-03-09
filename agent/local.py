"""
Local execution mode for the AI agent.
"""

import json
import os
import logging
import tempfile
import zipfile
from typing import List
import git
import glob
from agent.services.evmbench import submit_job
from agent.config import Settings

logger = logging.getLogger(__name__)

def clone_repository(repo_url: str, commit_hash: str | None = None) -> str:
    """
    Clone a GitHub repository to a temporary directory.
    
    Args:
        repo_url: URL of the GitHub repository
        commit_hash: Optional specific commit hash to checkout
        
    Returns:
        Path to the cloned repository
    """
    logger.info(f"Cloning repository: {repo_url}")
    temp_dir = tempfile.mkdtemp()
    repo = git.Repo.clone_from(repo_url, temp_dir)
    
    if commit_hash:
        logger.info(f"Checking out commit: {commit_hash}")
        repo.git.checkout(commit_hash)
        
    return temp_dir

def save_audit_results(output_path: str, audit: str):
    """
    Save audit results to a file.
    
    Args:
        output_path: Path to save the results to
        audit: Audit results
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(audit)
        logger.info(f"Security audit results saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving audit results: {str(e)}")
        raise

def process_local(repo_url: str, output_path: str, config: Settings, commit_hash: str | None = None):
    """
    Process a repository in local mode.
    
    Args:
        repo_url: URL of the GitHub repository
        output_path: Path to save the audit results
        config: Application configuration
        commit_hash: Optional specific commit hash to checkout
    """

    # Configure logging to both console and file
    log_file = config.log_file
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    try:
        # Clone the repository
        repo_path = clone_repository(repo_url, commit_hash)

        # Create a ZIP of the cloned repository and submit to evmbench
        from pathlib import Path
        zip_fd, zip_path = tempfile.mkstemp(suffix=".zip")
        os.close(zip_fd)
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _dirs, files in os.walk(repo_path):
                    for file in files:
                        full = os.path.join(root, file)
                        zf.write(full, os.path.relpath(full, repo_path))
            result = submit_job(config.evmbench_url, config.model, config.api_key, Path(zip_path))
        finally:
            os.unlink(zip_path)

        # Save results
        save_audit_results(output_path, json.dumps(result["findings"], indent=2))
        
        logger.info("Security audit completed successfully")
        
    except Exception as e:
        logger.error(f"Error in local processing: {str(e)}")
        raise