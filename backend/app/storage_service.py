import hashlib
from pathlib import Path
from .core import settings

ALLOWED={"application/pdf":".pdf","application/vnd.openxmlformats-officedocument.wordprocessingml.document":".docx","text/plain":".txt"}
def save_private(data:bytes,content_type:str,original_name:str,file_id:str)->tuple[str,str]:
    if content_type not in ALLOWED:raise ValueError("Unsupported file type")
    if not data or len(data)>settings().private_upload_max_bytes:raise ValueError("File size is invalid")
    root=Path(settings().private_storage_root);root.mkdir(parents=True,exist_ok=True);key=f"{file_id}{ALLOWED[content_type]}";path=root/key;path.write_bytes(data);return key,hashlib.sha256(data).hexdigest()
def private_path(key:str)->Path:return Path(settings().private_storage_root)/Path(key).name
