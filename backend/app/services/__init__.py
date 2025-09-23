from typing import Dict, Any, List, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)


# Mock User class
class MockUser:
    def __init__(self, id=1, username="demo_user", email="demo@example.com", role="user"):
        self.id = id
        self.username = username
        self.email = email
        self.role = type('Role', (), {'value': role})()
        self.is_active = True


# Mock Query class
class MockQuery:
    def __init__(self, id=1, query_type="email", query_value="test@example.com", user_id=1):
        self.id = id
        self.query_type = query_type
        self.query_value = query_value
        self.user_id = user_id
        self.status = "pending"
        self.metadata = {}


# Mock services
class UserService:
    def __init__(self, db):
        self.db = db
    
    async def get_by_username(self, username: str):
        return MockUser(username=username)
    
    async def authenticate(self, username: str, password: str):
        if username and password:
            return MockUser(username=username)
        return None
    
    async def update_last_login(self, user_id: int):
        pass


class QueryService:
    def __init__(self, db):
        self.db = db
    
    async def create(self, query_data, user_id: int):
        return MockQuery(
            query_type=query_data.query_type,
            query_value=query_data.query_value,
            user_id=user_id
        )
    
    async def get(self, query_id: int):
        return MockQuery(id=query_id)
    
    async def get_user_queries(self, user_id: int, filters):
        return [MockQuery(user_id=user_id)]
    
    async def get_scan_results(self, query_id: int):
        return []
    
    async def get_reports(self, query_id: int):
        return []
    
    async def update(self, query_id: int, update_data):
        return MockQuery(id=query_id)


class ScannerOrchestrator:
    def __init__(self, db):
        self.db = db
    
    async def start_scanning(self, query_id: int):
        logger.info(f"Starting scan for query {query_id}")
        await asyncio.sleep(1)  # Simulate scanning
        logger.info(f"Completed scan for query {query_id}")


class ReportService:
    def __init__(self, db):
        self.db = db
    
    async def generate_preview_report(self, query_id: int):
        return {"id": 1, "query_id": query_id, "report_type": "preview"}
    
    async def generate_full_report(self, query_id: int):
        return {"id": 1, "query_id": query_id, "report_type": "full"}
    
    async def get(self, report_id: int):
        return {"id": report_id, "query_id": 1, "report_type": "preview"}


class AdminService:
    def __init__(self, db):
        self.db = db
    
    async def get_dashboard_stats(self):
        return {
            "total_queries": 150,
            "active_queries": 25,
            "completed_queries": 125,
            "total_users": 50,
            "active_subscriptions": 15
        }