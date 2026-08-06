from dataclasses import dataclass, field

@dataclass
class BackupTask:
    enabled: bool=True
    source_folder:str=""
    destination_folder:str=""
    execution_time:str="22:00"

@dataclass
class AppConfig:
    version:str="1.0"
    language:str="es"
    theme:str="darkly"
    auto_run:bool=True
    tasks:list[BackupTask]=field(default_factory=lambda:[BackupTask()])
