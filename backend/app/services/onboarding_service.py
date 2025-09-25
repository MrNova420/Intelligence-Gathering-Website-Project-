#!/usr/bin/env python3
"""
User Onboarding and Tutorial System
Provides guided user onboarding, interactive tutorials, and progress tracking
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)

class OnboardingStep(Enum):
    """Onboarding steps enumeration"""
    WELCOME = "welcome"
    PROFILE_SETUP = "profile_setup"
    FIRST_SCAN = "first_scan"
    REPORT_GENERATION = "report_generation"
    SECURITY_SETUP = "security_setup"
    DASHBOARD_TOUR = "dashboard_tour"
    ADVANCED_FEATURES = "advanced_features"
    COMPLETION = "completion"

class TutorialType(Enum):
    """Tutorial types"""
    INTERACTIVE = "interactive"
    VIDEO = "video"
    TEXT = "text"
    HANDS_ON = "hands_on"

@dataclass
class TutorialContent:
    """Tutorial content structure"""
    id: str
    title: str
    description: str
    type: TutorialType
    estimated_duration: int  # minutes
    steps: List[Dict[str, Any]]
    prerequisites: List[str]
    completion_criteria: Dict[str, Any]
    resources: List[Dict[str, str]]

@dataclass
class UserProgress:
    """User onboarding progress tracking"""
    user_id: str
    current_step: OnboardingStep
    completed_steps: List[OnboardingStep]
    started_at: datetime
    last_activity: datetime
    completed_tutorials: List[str]
    skipped_steps: List[OnboardingStep]
    completion_percentage: float
    estimated_time_remaining: int  # minutes

class OnboardingService:
    """Main onboarding service class"""
    
    def __init__(self):
        self.tutorials: Dict[str, TutorialContent] = {}
        self.user_progress: Dict[str, UserProgress] = {}
        self._initialize_tutorials()
        logger.info("🎓 Onboarding Service initialized")
    
    def _initialize_tutorials(self):
        """Initialize default tutorial content"""
        
        # Welcome Tutorial
        welcome_tutorial = TutorialContent(
            id="welcome",
            title="Welcome to Intelligence Gathering Platform",
            description="Get started with your intelligence gathering journey",
            type=TutorialType.INTERACTIVE,
            estimated_duration=5,
            steps=[
                {
                    "id": "intro",
                    "title": "Platform Introduction",
                    "content": "Welcome! This platform helps you gather and analyze intelligence from various sources.",
                    "action": "show_welcome_modal",
                    "data": {
                        "features": [
                            "Email intelligence gathering",
                            "Phone number analysis", 
                            "Social media profiling",
                            "Comprehensive reporting",
                            "Advanced security features"
                        ]
                    }
                },
                {
                    "id": "navigation",
                    "title": "Platform Navigation",
                    "content": "Let's explore the main navigation areas",
                    "action": "highlight_navigation",
                    "data": {
                        "areas": ["dashboard", "scanners", "reports", "settings"]
                    }
                }
            ],
            prerequisites=[],
            completion_criteria={"steps_completed": 2},
            resources=[
                {"type": "documentation", "url": "/docs/getting-started"},
                {"type": "video", "url": "/tutorials/welcome-video"}
            ]
        )
        
        # First Scan Tutorial
        first_scan_tutorial = TutorialContent(
            id="first_scan",
            title="Your First Intelligence Scan",
            description="Learn how to perform your first intelligence gathering scan",
            type=TutorialType.HANDS_ON,
            estimated_duration=10,
            steps=[
                {
                    "id": "choose_target",
                    "title": "Choose Your Target",
                    "content": "Select what type of intelligence you want to gather",
                    "action": "show_scanner_options",
                    "data": {
                        "options": ["email", "phone", "social_media"],
                        "recommended": "email"
                    }
                },
                {
                    "id": "enter_data", 
                    "title": "Enter Target Information",
                    "content": "Enter the email address or information you want to analyze",
                    "action": "focus_input_field",
                    "data": {
                        "field": "target_input",
                        "example": "example@domain.com"
                    }
                },
                {
                    "id": "start_scan",
                    "title": "Start Your Scan",
                    "content": "Click the scan button to begin the intelligence gathering process",
                    "action": "highlight_scan_button",
                    "data": {}
                },
                {
                    "id": "view_results",
                    "title": "Review Results",
                    "content": "Examine the intelligence gathered about your target",
                    "action": "show_results_explanation",
                    "data": {
                        "sections": ["basic_info", "social_presence", "security_assessment"]
                    }
                }
            ],
            prerequisites=["welcome"],
            completion_criteria={"scan_completed": True, "results_viewed": True},
            resources=[
                {"type": "guide", "url": "/docs/scanning-guide"},
                {"type": "video", "url": "/tutorials/first-scan"}
            ]
        )
        
        # Security Setup Tutorial
        security_tutorial = TutorialContent(
            id="security_setup",
            title="Secure Your Account",
            description="Set up two-factor authentication and security preferences",
            type=TutorialType.INTERACTIVE,
            estimated_duration=8,
            steps=[
                {
                    "id": "mfa_setup",
                    "title": "Enable Two-Factor Authentication",
                    "content": "Secure your account with 2FA for enhanced protection",
                    "action": "navigate_to_security",
                    "data": {
                        "section": "two_factor_auth"
                    }
                },
                {
                    "id": "backup_codes",
                    "title": "Save Backup Codes",
                    "content": "Download and securely store your backup recovery codes", 
                    "action": "generate_backup_codes",
                    "data": {}
                },
                {
                    "id": "security_preferences",
                    "title": "Configure Security Preferences",
                    "content": "Set up login notifications and session management",
                    "action": "show_security_settings",
                    "data": {
                        "settings": ["login_notifications", "session_timeout", "ip_restrictions"]
                    }
                }
            ],
            prerequisites=["welcome", "profile_setup"],
            completion_criteria={"mfa_enabled": True, "backup_codes_saved": True},
            resources=[
                {"type": "security_guide", "url": "/docs/security-best-practices"}
            ]
        )
        
        # Advanced Features Tutorial
        advanced_tutorial = TutorialContent(
            id="advanced_features",
            title="Advanced Intelligence Features",
            description="Discover powerful advanced features and integrations",
            type=TutorialType.TEXT,
            estimated_duration=15,
            steps=[
                {
                    "id": "batch_scanning",
                    "title": "Batch Processing",
                    "content": "Learn how to process multiple targets simultaneously",
                    "action": "show_batch_interface",
                    "data": {
                        "max_batch_size": 100,
                        "supported_formats": ["csv", "txt", "json"]
                    }
                },
                {
                    "id": "api_access",
                    "title": "API Integration",
                    "content": "Access the platform programmatically via REST API",
                    "action": "show_api_documentation",
                    "data": {
                        "endpoints": ["/api/v1/scan", "/api/v1/reports", "/api/v1/users"]
                    }
                },
                {
                    "id": "custom_reports",
                    "title": "Custom Report Generation",
                    "content": "Create tailored reports with custom templates",
                    "action": "show_report_builder",
                    "data": {
                        "templates": ["executive_summary", "technical_details", "compliance_report"]
                    }
                },
                {
                    "id": "integrations",
                    "title": "Third-party Integrations",
                    "content": "Connect with external tools and services",
                    "action": "show_integrations_page",
                    "data": {
                        "available": ["slack", "jira", "splunk", "elastic"]
                    }
                }
            ],
            prerequisites=["first_scan", "report_generation"],
            completion_criteria={"features_explored": 3},
            resources=[
                {"type": "api_docs", "url": "/api/docs"},
                {"type": "integration_guide", "url": "/docs/integrations"}
            ]
        )
        
        # Store tutorials
        self.tutorials = {
            "welcome": welcome_tutorial,
            "first_scan": first_scan_tutorial,
            "security_setup": security_tutorial,
            "advanced_features": advanced_tutorial
        }
    
    def start_onboarding(self, user_id: str) -> UserProgress:
        """Start onboarding process for a user"""
        if user_id in self.user_progress:
            logger.info(f"User {user_id} already has onboarding in progress")
            return self.user_progress[user_id]
        
        progress = UserProgress(
            user_id=user_id,
            current_step=OnboardingStep.WELCOME,
            completed_steps=[],
            started_at=datetime.now(),
            last_activity=datetime.now(),
            completed_tutorials=[],
            skipped_steps=[],
            completion_percentage=0.0,
            estimated_time_remaining=45  # Total estimated time
        )
        
        self.user_progress[user_id] = progress
        logger.info(f"🚀 Started onboarding for user {user_id}")
        
        return progress
    
    def get_user_progress(self, user_id: str) -> Optional[UserProgress]:
        """Get current onboarding progress for user"""
        return self.user_progress.get(user_id)
    
    def complete_step(self, user_id: str, step: OnboardingStep) -> Dict[str, Any]:
        """Mark an onboarding step as completed"""
        if user_id not in self.user_progress:
            return {"success": False, "error": "User not found in onboarding"}
        
        progress = self.user_progress[user_id]
        
        if step not in progress.completed_steps:
            progress.completed_steps.append(step)
            progress.last_activity = datetime.now()
            
            # Update completion percentage
            total_steps = len(OnboardingStep)
            progress.completion_percentage = (len(progress.completed_steps) / total_steps) * 100
            
            # Update estimated time remaining
            avg_time_per_step = 6  # minutes
            remaining_steps = total_steps - len(progress.completed_steps)
            progress.estimated_time_remaining = remaining_steps * avg_time_per_step
            
            # Move to next step
            next_step = self._get_next_step(progress.completed_steps)
            if next_step:
                progress.current_step = next_step
            
            logger.info(f"✅ User {user_id} completed step: {step.value}")
            
            return {
                "success": True,
                "completed_step": step.value,
                "next_step": progress.current_step.value if progress.current_step else None,
                "completion_percentage": progress.completion_percentage,
                "remaining_time": progress.estimated_time_remaining
            }
        
        return {"success": False, "error": "Step already completed"}
    
    def skip_step(self, user_id: str, step: OnboardingStep, reason: str = "") -> Dict[str, Any]:
        """Skip an onboarding step"""
        if user_id not in self.user_progress:
            return {"success": False, "error": "User not found in onboarding"}
        
        progress = self.user_progress[user_id]
        
        if step not in progress.skipped_steps:
            progress.skipped_steps.append(step)
            progress.last_activity = datetime.now()
            
            # Move to next step
            next_step = self._get_next_step(progress.completed_steps + progress.skipped_steps)
            if next_step:
                progress.current_step = next_step
            
            logger.info(f"⏭️ User {user_id} skipped step: {step.value} (reason: {reason})")
            
            return {
                "success": True,
                "skipped_step": step.value,
                "next_step": progress.current_step.value if progress.current_step else None,
                "reason": reason
            }
        
        return {"success": False, "error": "Step already skipped"}
    
    def _get_next_step(self, completed_or_skipped: List[OnboardingStep]) -> Optional[OnboardingStep]:
        """Determine the next onboarding step"""
        all_steps = list(OnboardingStep)
        
        for step in all_steps:
            if step not in completed_or_skipped:
                return step
        
        return None  # All steps completed
    
    def get_tutorial(self, tutorial_id: str) -> Optional[TutorialContent]:
        """Get tutorial content by ID"""
        return self.tutorials.get(tutorial_id)
    
    def complete_tutorial(self, user_id: str, tutorial_id: str) -> Dict[str, Any]:
        """Mark a tutorial as completed"""
        if user_id not in self.user_progress:
            return {"success": False, "error": "User not found in onboarding"}
        
        if tutorial_id not in self.tutorials:
            return {"success": False, "error": "Tutorial not found"}
        
        progress = self.user_progress[user_id]
        
        if tutorial_id not in progress.completed_tutorials:
            progress.completed_tutorials.append(tutorial_id)
            progress.last_activity = datetime.now()
            
            logger.info(f"📚 User {user_id} completed tutorial: {tutorial_id}")
            
            return {
                "success": True,
                "completed_tutorial": tutorial_id,
                "total_completed": len(progress.completed_tutorials)
            }
        
        return {"success": False, "error": "Tutorial already completed"}
    
    def get_recommended_tutorials(self, user_id: str) -> List[TutorialContent]:
        """Get recommended tutorials for user based on progress"""
        if user_id not in self.user_progress:
            return []
        
        progress = self.user_progress[user_id]
        completed_tutorials = set(progress.completed_tutorials)
        
        recommended = []
        
        for tutorial_id, tutorial in self.tutorials.items():
            # Skip if already completed
            if tutorial_id in completed_tutorials:
                continue
            
            # Check prerequisites
            prerequisites_met = all(
                prereq in completed_tutorials 
                for prereq in tutorial.prerequisites
            )
            
            if prerequisites_met:
                recommended.append(tutorial)
        
        # Sort by estimated duration (shorter first)
        recommended.sort(key=lambda t: t.estimated_duration)
        
        return recommended
    
    def get_onboarding_analytics(self) -> Dict[str, Any]:
        """Get analytics about onboarding process"""
        if not self.user_progress:
            return {"total_users": 0}
        
        total_users = len(self.user_progress)
        completed_users = len([
            p for p in self.user_progress.values() 
            if p.completion_percentage == 100
        ])
        
        # Calculate average completion time
        completed_progresses = [
            p for p in self.user_progress.values() 
            if p.completion_percentage == 100
        ]
        
        avg_completion_time = 0
        if completed_progresses:
            completion_times = [
                (p.last_activity - p.started_at).total_seconds() / 3600  # hours
                for p in completed_progresses
            ]
            avg_completion_time = sum(completion_times) / len(completion_times)
        
        # Step completion rates
        step_completion = {}
        for step in OnboardingStep:
            completed_count = len([
                p for p in self.user_progress.values() 
                if step in p.completed_steps
            ])
            step_completion[step.value] = (completed_count / total_users) * 100
        
        # Tutorial completion rates
        tutorial_completion = {}
        for tutorial_id in self.tutorials.keys():
            completed_count = len([
                p for p in self.user_progress.values() 
                if tutorial_id in p.completed_tutorials
            ])
            tutorial_completion[tutorial_id] = (completed_count / total_users) * 100
        
        return {
            "total_users": total_users,
            "completed_users": completed_users,
            "completion_rate": (completed_users / total_users) * 100 if total_users > 0 else 0,
            "average_completion_time_hours": avg_completion_time,
            "step_completion_rates": step_completion,
            "tutorial_completion_rates": tutorial_completion,
            "most_skipped_steps": [
                step.value for step in OnboardingStep 
                if sum(1 for p in self.user_progress.values() if step in p.skipped_steps) > 0
            ]
        }
    
    def export_progress(self, user_id: str) -> Dict[str, Any]:
        """Export user's onboarding progress"""
        if user_id not in self.user_progress:
            return {"error": "User not found"}
        
        progress = self.user_progress[user_id]
        
        return {
            "user_id": user_id,
            "progress": {
                **asdict(progress),
                "started_at": progress.started_at.isoformat(),
                "last_activity": progress.last_activity.isoformat(),
                "current_step": progress.current_step.value,
                "completed_steps": [step.value for step in progress.completed_steps],
                "skipped_steps": [step.value for step in progress.skipped_steps]
            },
            "available_tutorials": [
                {
                    "id": tutorial.id,
                    "title": tutorial.title,
                    "completed": tutorial.id in progress.completed_tutorials,
                    "duration": tutorial.estimated_duration
                }
                for tutorial in self.tutorials.values()
            ],
            "export_timestamp": datetime.now().isoformat()
        }

# Global onboarding service instance
onboarding_service = OnboardingService()

if __name__ == "__main__":
    # Test onboarding service
    print("🧪 Testing Onboarding Service...")
    
    service = OnboardingService()
    
    # Start onboarding for test user
    user_id = "test-user-123"
    progress = service.start_onboarding(user_id)
    print(f"Started onboarding: {asdict(progress)}")
    
    # Complete a step
    result = service.complete_step(user_id, OnboardingStep.WELCOME)
    print(f"Completed step: {result}")
    
    # Get recommended tutorials
    tutorials = service.get_recommended_tutorials(user_id)
    print(f"Recommended tutorials: {[t.title for t in tutorials]}")
    
    # Get analytics
    analytics = service.get_onboarding_analytics()
    print(f"Analytics: {analytics}")
    
    print("✅ Onboarding service test completed!")