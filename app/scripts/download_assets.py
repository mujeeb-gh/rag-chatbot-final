"""
Download assets (models and ChromaDB) from HuggingFace Hub if not already present locally.
This script runs at container startup to ensure required files are available.
"""
import os
import shutil
import sys
import tarfile
import zipfile
from pathlib import Path
from src.settings import settings

try:
    from huggingface_hub import snapshot_download, hf_hub_download
    from huggingface_hub.utils import HfHubHTTPError
except ImportError:
    print("ERROR: huggingface_hub not installed. Please install it first.")
    sys.exit(1)


def get_project_root():
    """Get the project root directory."""
    # This script is in app/scripts/, so go up two levels
    script_dir = Path(__file__).parent
    return script_dir.parent.parent


def download_models(models_repo: str, models_dir: Path, hf_token: str | None = None) -> None:
    """
    Download models from HuggingFace Hub if not present locally.
    
    Args:
        models_repo: HuggingFace Hub repository (e.g., "username/astra-models")
        models_dir: Local directory to store models
        hf_token: Optional HuggingFace token for private repos
    """
    if not models_repo:
        print("WARNING: HF_MODELS_REPO not set. Skipping model download.")
        return
    
    print(f"Checking models in {models_dir}...")
    
    # Check if models directory already has content
    if models_dir.exists() and any(models_dir.iterdir()):
        print(f"Models directory already contains files. Skipping download.")
        print(f"To force re-download, delete {models_dir} and restart.")
        return
    
    print(f"Downloading models from {models_repo}...")
    try:
        # Ensure models directory exists
        models_dir.mkdir(parents=True, exist_ok=True)
        
        # Download the entire repository
        snapshot_download(
            repo_id=models_repo,
            local_dir=str(models_dir),
            token=hf_token,
            resume_download=True,
        )
        print(f"✓ Models downloaded successfully to {models_dir}")
    except HfHubHTTPError as e:
        print(f"ERROR: Failed to download models from {models_repo}")
        print(f"Error: {e}")
        print("Make sure the repository exists and is accessible.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error while downloading models: {e}")
        sys.exit(1)


def download_chromadb(chromadb_repo: str, chromadb_dir: Path, hf_token: str | None = None) -> None:
    """
    Download ChromaDB archive from HuggingFace Hub and extract it.
    
    Args:
        chromadb_repo: HuggingFace Hub repository (e.g., "username/astra-chromadb")
        chromadb_dir: Local directory for ChromaDB
        hf_token: Optional HuggingFace token for private repos
    """
    if not chromadb_repo:
        print("WARNING: HF_CHROMADB_REPO not set. Skipping ChromaDB download.")
        return
    
    print(f"Checking ChromaDB in {chromadb_dir}...")
    
    # Check if ChromaDB directory already has content
    expected_chroma_path = chromadb_dir / "bge-small-finetuned-chroma" # should be settings.chroma_db
    if expected_chroma_path.exists() and any(expected_chroma_path.iterdir()):
        print(f"ChromaDB directory already contains files. Skipping download.")
        print(f"To force re-download, delete {chromadb_dir} and restart.")
        return
    
    print(f"Downloading ChromaDB from {chromadb_repo}...")
    try:
        # Ensure chromadb directory exists
        chromadb_dir.mkdir(parents=True, exist_ok=True)
        
        # Try common archive filenames
        archive_names = ["chromadb.tar.gz", "chromadb.zip", "chroma.tar.gz", "chroma.zip", ".chroma.tar.gz", ".chroma.zip"]
        
        downloaded = False
        for archive_name in archive_names:
            try:
                archive_path = hf_hub_download(
                    repo_id=chromadb_repo,
                    filename=archive_name,
                    local_dir=str(chromadb_dir.parent),
                    token=hf_token,
                    resume_download=True,
                )
                
                # Extract the archive
                print(f"Extracting {archive_name}...")
                if archive_name.endswith('.tar.gz'):
                    with tarfile.open(archive_path, 'r:gz') as tar:
                        # Get members and check if they're in a subdirectory
                        members = tar.getmembers()
                        # Extract to parent directory
                        tar.extractall(path=chromadb_dir.parent)
                        
                        # If archive contains .chroma subdirectory, move contents up
                        extracted_chroma = chromadb_dir.parent / ".chroma"
                        if extracted_chroma.exists() and extracted_chroma != chromadb_dir:
                            # Move contents from .chroma to chromadb_dir
                            for item in extracted_chroma.iterdir():
                                shutil.move(str(item), str(chromadb_dir / item.name))
                            extracted_chroma.rmdir()
                elif archive_name.endswith('.zip'):
                    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                        zip_ref.extractall(path=chromadb_dir.parent)
                        
                        # If archive contains .chroma subdirectory, move contents up
                        extracted_chroma = chromadb_dir.parent / ".chroma"
                        if extracted_chroma.exists() and extracted_chroma.is_dir():
                            # Move contents from .chroma to chromadb_dir
                            for item in extracted_chroma.iterdir():
                                shutil.move(str(item), str(chromadb_dir / item.name))
                            extracted_chroma.rmdir()
                
                # Clean up the archive file
                os.remove(archive_path)
                print(f"✓ ChromaDB downloaded and extracted successfully to {chromadb_dir}")
                downloaded = True
                break
            except HfHubHTTPError:
                # Try next archive name
                continue
        
        if not downloaded:
            # If no archive found, try downloading as a snapshot (directory structure)
            print("No archive found, trying to download as directory snapshot...")
            snapshot_download(
                repo_id=chromadb_repo,
                local_dir=str(chromadb_dir),
                token=hf_token,
                resume_download=True,
            )
            print(f"✓ ChromaDB downloaded successfully to {chromadb_dir}")
            
    except HfHubHTTPError as e:
        print(f"ERROR: Failed to download ChromaDB from {chromadb_repo}")
        print(f"Error: {e}")
        print("Make sure the repository exists and is accessible.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Unexpected error while downloading ChromaDB: {e}")
        sys.exit(1)


def main():
    """Main function to download all required assets."""
    print("=" * 60)
    print("Downloading assets from HuggingFace Hub...")
    print("=" * 60)
    
    project_root = get_project_root()
    models_dir = project_root / "models"
    chromadb_dir = project_root / ".chroma"
    
    # Get configuration from environment variables
    models_repo = os.getenv("HF_MODELS_REPO", "")
    chromadb_repo = os.getenv("HF_CHROMADB_REPO", "")
    hf_token = os.getenv("HF_TOKEN", None)
    
    # Download models
    if models_repo:
        download_models(models_repo, models_dir, hf_token)
    else:
        print("INFO: HF_MODELS_REPO not configured. Models must be available locally.")
    
    # Download ChromaDB
    if chromadb_repo:
        download_chromadb(chromadb_repo, chromadb_dir, hf_token)
    else:
        print("INFO: HF_CHROMADB_REPO not configured. ChromaDB must be available locally.")
    
    print("=" * 60)
    print("Asset download complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

