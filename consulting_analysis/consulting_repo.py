from pydantic import BaseModel
from typing import Any, Dict, Tuple
from pprint import pprint

class ConsultingResult(BaseModel):
    short_name: str
    name: str
    value: float
    units: str
    display_units: str

class ConsultingResultRepo(BaseModel):
    consulting_results: list[ConsultingResult]

    def clear_all(self) -> None: 
        self.consulting_results.clear()

    def put(self, ConsultingResult) -> None:
        self.consulting_results.append(ConsultingResult)

    def list_all(self) -> list[ConsultingResult]:
        pprint(self.consulting_results)

    def get(self, s_name: str) -> ConsultingResult:
        for result in self.consulting_results:
            if s_name in result.short_name:
                return result
    
    def to_dict(self) -> Dict[Any, Any]:
        return self.model_dump()