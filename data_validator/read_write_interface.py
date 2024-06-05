from datetime import datetime
import json
from pathlib import Path
from typing import Tuple
from pydantic import BaseModel

class ConsultingSession(BaseModel):
    date: datetime
    name: str
    type: str
    consultant: str
    duration_mins: int

class ConsultingSessionList(BaseModel):
    sessions: Tuple[ConsultingSession, ...]

    @classmethod
    def read_from_paths(cls, paths: list[Path]) -> 'ConsultingSessionList':
        sessions = []
        for path in paths:
            session = ConsultingSession.parse_file(path)
            sessions.append(session)
        
        return ConsultingSessionList(
            sessions=sessions
        )
    
    
    def write_to_directory(self, path: Path) -> None:
        if path.exists():
            assert path.is_dir()
        
        path.mkdir(parents=True, exist_ok=True)
        for session in self.sessions:
            json_text = session.model_dump_json()
            json_text_pretty = json.dumps(json.loads(json_text), indent=3)
            filename = session.name[:3] + session.consultant[:3] + session.date.strftime("%Y-%m-%d")
            path.joinpath(f'{filename}.json').write_text(json_text_pretty)
