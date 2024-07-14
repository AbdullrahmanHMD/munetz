from dataclasses import dataclass

@dataclass
class AssistantConfig:
    name : str
    instructions : str
    tools : list
    model : str
