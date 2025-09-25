#!/usr/bin/env python3
"""
Plugin/Extension System for Intelligence Gathering Platform
Provides a flexible plugin architecture for extending platform capabilities
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class PluginType(Enum):
    """Plugin types supported by the system"""
    SCANNER = "scanner"
    PROCESSOR = "processor" 
    REPORTER = "reporter"
    AUTHENTICATOR = "authenticator"
    NOTIFIER = "notifier"
    ANALYZER = "analyzer"

class PluginStatus(Enum):
    """Plugin status states"""
    INACTIVE = "inactive"
    ACTIVE = "active"
    ERROR = "error"

@dataclass
class PluginMetadata:
    """Plugin metadata structure"""
    name: str
    version: str
    description: str
    author: str
    plugin_type: PluginType
    dependencies: List[str]
    compatibility_version: str

@dataclass
class PluginInfo:
    """Complete plugin information"""
    metadata: PluginMetadata
    status: PluginStatus
    file_path: str
    load_time: Optional[datetime] = None
    error_message: Optional[str] = None
    config: Dict[str, Any] = None

class BasePlugin(ABC):
    """Base class for all plugins"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(f"plugin.{self.__class__.__name__}")
        self._initialized = False
    
    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata"""
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the plugin"""
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """Cleanup plugin resources"""
        pass

class PluginManager:
    """Main plugin management system"""
    
    def __init__(self, plugins_directory: str = "plugins"):
        self.plugins_directory = Path(plugins_directory)
        self.plugins: Dict[str, PluginInfo] = {}
        
        # Create plugins directory if it doesn't exist
        self.plugins_directory.mkdir(exist_ok=True)
        
        logger.info(f"🔌 Plugin Manager initialized with directory: {self.plugins_directory}")
    
    def get_plugin_statistics(self) -> Dict[str, Any]:
        """Get plugin system statistics"""
        plugins_by_status = {}
        plugins_by_type = {}
        
        for plugin_info in self.plugins.values():
            status = plugin_info.status.value
            plugin_type = plugin_info.metadata.plugin_type.value
            
            plugins_by_status[status] = plugins_by_status.get(status, 0) + 1
            plugins_by_type[plugin_type] = plugins_by_type.get(plugin_type, 0) + 1
        
        return {
            "total_plugins": len(self.plugins),
            "active_plugins": len([p for p in self.plugins.values() if p.status == PluginStatus.ACTIVE]),
            "by_status": plugins_by_status,
            "by_type": plugins_by_type,
            "plugins_directory": str(self.plugins_directory)
        }

# Global plugin manager instance
plugin_manager = PluginManager()

if __name__ == "__main__":
    print("🔌 Plugin system initialized successfully!")
    stats = plugin_manager.get_plugin_statistics()
    print(f"Statistics: {stats}")
    print("✅ Plugin system test completed!")