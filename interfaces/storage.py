"""
Storage interface abstraction
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class StorageInterface(ABC):
    """Abstract interface for storage operations"""
    
    @abstractmethod
    def save(self, key: str, data: Dict[str, Any]) -> bool:
        """Save data with given key"""
        pass
    
    @abstractmethod
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """Load data by key"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete data by key"""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        pass
    
    @abstractmethod
    def list_keys(self, prefix: str = "") -> List[str]:
        """List all keys with optional prefix"""
        pass


class MemoryStorage(StorageInterface):
    """In-memory storage implementation"""
    
    def __init__(self):
        self._data: Dict[str, Dict[str, Any]] = {}
    
    def save(self, key: str, data: Dict[str, Any]) -> bool:
        """Save data to memory"""
        self._data[key] = data.copy()
        return True
    
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """Load data from memory"""
        return self._data.get(key)
    
    def delete(self, key: str) -> bool:
        """Delete data from memory"""
        if key in self._data:
            del self._data[key]
            return True
        return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in memory"""
        return key in self._data
    
    def list_keys(self, prefix: str = "") -> List[str]:
        """List all keys with optional prefix"""
        return [key for key in self._data.keys() if key.startswith(prefix)]
    
    def clear(self) -> None:
        """Clear all data (useful for testing)"""
        self._data.clear()