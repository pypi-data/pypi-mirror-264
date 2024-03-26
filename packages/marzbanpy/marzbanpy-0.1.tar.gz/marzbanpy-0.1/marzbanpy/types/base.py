from typing import Any

class Base:
    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)
    
    def __str__(self) -> str:
        return str(self.__dict__)