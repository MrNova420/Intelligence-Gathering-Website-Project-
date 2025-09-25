"""
Integrated Automation System
===========================

Unified automation system integrated within the Intelligence Gathering Platform.
All automation capabilities are now part of the main website application.
"""

from .platform_automation import PlatformAutomation
from .system_management import SystemManager
from .deployment_automation import DeploymentManager

__all__ = ['PlatformAutomation', 'SystemManager', 'DeploymentManager']