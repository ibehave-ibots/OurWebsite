from pydantic import BaseModel, DirectoryPath


class Config(BaseModel):
    base_url: str = ''
    base_dir: DirectoryPath = DirectoryPath('.')
    

