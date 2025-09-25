#!/usr/bin/env python3
"""
Backup and Recovery Service
Provides comprehensive backup and disaster recovery capabilities
"""

import os
import shutil
import tarfile
import gzip
import json
import sqlite3
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import hashlib
import subprocess

logger = logging.getLogger(__name__)

class BackupType(Enum):
    """Types of backups supported"""
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    DATABASE_ONLY = "database_only"
    CONFIG_ONLY = "config_only"

class BackupStatus(Enum):
    """Backup operation status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class BackupMetadata:
    """Backup metadata structure"""
    backup_id: str
    backup_type: BackupType
    created_at: datetime
    completed_at: Optional[datetime]
    status: BackupStatus
    file_path: str
    file_size: int
    checksum: str
    description: str
    includes: List[str]
    excludes: List[str]
    compression: bool
    retention_days: int

class BackupService:
    """Main backup and recovery service"""
    
    def __init__(self, backup_directory: str = "backups"):
        self.backup_directory = Path(backup_directory)
        self.backup_directory.mkdir(exist_ok=True)
        
        self.metadata_file = self.backup_directory / "backup_metadata.json"
        self.metadata: List[BackupMetadata] = []
        self.lock = threading.Lock()
        
        # Load existing metadata
        self._load_metadata()
        
        # Default configurations
        self.default_includes = [
            "backend/app",
            "backend/intelligence_platform.db",
            "frontend/pages",
            "frontend/components",
            "config",
            ".env.example"
        ]
        
        self.default_excludes = [
            "node_modules",
            "__pycache__",
            "*.pyc",
            ".git",
            "logs/*.log",
            "tmp",
            "*.tmp"
        ]
        
        logger.info(f"💾 Backup Service initialized with directory: {self.backup_directory}")
    
    def _load_metadata(self):
        """Load backup metadata from file"""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.metadata = [
                        BackupMetadata(
                            backup_id=item['backup_id'],
                            backup_type=BackupType(item['backup_type']),
                            created_at=datetime.fromisoformat(item['created_at']),
                            completed_at=datetime.fromisoformat(item['completed_at']) if item['completed_at'] else None,
                            status=BackupStatus(item['status']),
                            file_path=item['file_path'],
                            file_size=item['file_size'],
                            checksum=item['checksum'],
                            description=item['description'],
                            includes=item['includes'],
                            excludes=item['excludes'],
                            compression=item['compression'],
                            retention_days=item['retention_days']
                        )
                        for item in data
                    ]
                logger.info(f"📋 Loaded {len(self.metadata)} backup records")
        except Exception as e:
            logger.error(f"Error loading backup metadata: {e}")
            self.metadata = []
    
    def _save_metadata(self):
        """Save backup metadata to file"""
        try:
            data = []
            for backup in self.metadata:
                item = asdict(backup)
                item['backup_type'] = backup.backup_type.value
                item['status'] = backup.status.value
                item['created_at'] = backup.created_at.isoformat()
                item['completed_at'] = backup.completed_at.isoformat() if backup.completed_at else None
                data.append(item)
            
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            logger.error(f"Error saving backup metadata: {e}")
    
    def create_backup(
        self,
        backup_type: BackupType = BackupType.FULL,
        description: str = "",
        includes: Optional[List[str]] = None,
        excludes: Optional[List[str]] = None,
        compression: bool = True,
        retention_days: int = 30
    ) -> str:
        """Create a new backup"""
        
        backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        timestamp = datetime.now()
        
        # Use defaults if not specified
        includes = includes or self.default_includes
        excludes = excludes or self.default_excludes
        
        # Create backup filename
        extension = ".tar.gz" if compression else ".tar"
        backup_filename = f"{backup_id}{extension}"
        backup_path = self.backup_directory / backup_filename
        
        # Create initial metadata
        metadata = BackupMetadata(
            backup_id=backup_id,
            backup_type=backup_type,
            created_at=timestamp,
            completed_at=None,
            status=BackupStatus.PENDING,
            file_path=str(backup_path),
            file_size=0,
            checksum="",
            description=description or f"Automated {backup_type.value} backup",
            includes=includes,
            excludes=excludes,
            compression=compression,
            retention_days=retention_days
        )
        
        with self.lock:
            self.metadata.append(metadata)
            self._save_metadata()
        
        logger.info(f"🚀 Starting backup: {backup_id}")
        
        # Start backup in background thread
        thread = threading.Thread(
            target=self._perform_backup,
            args=(metadata,),
            daemon=True
        )
        thread.start()
        
        return backup_id
    
    def _perform_backup(self, metadata: BackupMetadata):
        """Perform the actual backup operation"""
        try:
            # Update status to running
            metadata.status = BackupStatus.RUNNING
            with self.lock:
                self._save_metadata()
            
            # Create archive
            mode = "w:gz" if metadata.compression else "w"
            
            with tarfile.open(metadata.file_path, mode) as tar:
                for include_path in metadata.includes:
                    full_path = Path(include_path)
                    
                    if full_path.exists():
                        # Check if path should be excluded
                        should_exclude = False
                        for exclude_pattern in metadata.excludes:
                            if exclude_pattern in str(full_path):
                                should_exclude = True
                                break
                        
                        if not should_exclude:
                            if full_path.is_file():
                                tar.add(full_path, arcname=str(full_path))
                                logger.debug(f"Added file: {full_path}")
                            elif full_path.is_dir():
                                # Add directory recursively
                                for file_path in full_path.rglob("*"):
                                    if file_path.is_file():
                                        # Check exclusions
                                        skip_file = False
                                        for exclude_pattern in metadata.excludes:
                                            if exclude_pattern in str(file_path):
                                                skip_file = True
                                                break
                                        
                                        if not skip_file:
                                            tar.add(file_path, arcname=str(file_path))
                    else:
                        logger.warning(f"Include path not found: {include_path}")
            
            # Calculate file size and checksum
            file_size = Path(metadata.file_path).stat().st_size
            checksum = self._calculate_checksum(metadata.file_path)
            
            # Update metadata
            metadata.status = BackupStatus.COMPLETED
            metadata.completed_at = datetime.now()
            metadata.file_size = file_size
            metadata.checksum = checksum
            
            with self.lock:
                self._save_metadata()
            
            duration = (metadata.completed_at - metadata.created_at).total_seconds()
            logger.info(f"✅ Backup completed: {metadata.backup_id} ({file_size} bytes, {duration:.1f}s)")
            
        except Exception as e:
            # Update status to failed
            metadata.status = BackupStatus.FAILED
            metadata.completed_at = datetime.now()
            
            with self.lock:
                self._save_metadata()
            
            logger.error(f"❌ Backup failed: {metadata.backup_id} - {e}")
    
    def _calculate_checksum(self, file_path: str) -> str:
        """Calculate SHA-256 checksum of file"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating checksum: {e}")
            return ""
    
    def get_backup_status(self, backup_id: str) -> Optional[BackupMetadata]:
        """Get status of a specific backup"""
        with self.lock:
            for backup in self.metadata:
                if backup.backup_id == backup_id:
                    return backup
        return None
    
    def list_backups(self, 
                    status: Optional[BackupStatus] = None,
                    backup_type: Optional[BackupType] = None,
                    days: Optional[int] = None) -> List[BackupMetadata]:
        """List backups with optional filtering"""
        
        backups = self.metadata.copy()
        
        # Filter by status
        if status:
            backups = [b for b in backups if b.status == status]
        
        # Filter by type
        if backup_type:
            backups = [b for b in backups if b.backup_type == backup_type]
        
        # Filter by age
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            backups = [b for b in backups if b.created_at >= cutoff_date]
        
        # Sort by creation date (newest first)
        backups.sort(key=lambda x: x.created_at, reverse=True)
        
        return backups
    
    def restore_backup(self, backup_id: str, restore_path: str = ".") -> bool:
        """Restore from a backup"""
        try:
            # Find backup metadata
            backup_metadata = self.get_backup_status(backup_id)
            if not backup_metadata:
                logger.error(f"Backup not found: {backup_id}")
                return False
            
            if backup_metadata.status != BackupStatus.COMPLETED:
                logger.error(f"Backup not completed: {backup_id}")
                return False
            
            # Verify backup file exists
            backup_file = Path(backup_metadata.file_path)
            if not backup_file.exists():
                logger.error(f"Backup file not found: {backup_file}")
                return False
            
            # Verify checksum
            current_checksum = self._calculate_checksum(str(backup_file))
            if current_checksum != backup_metadata.checksum:
                logger.error(f"Backup file corrupted: checksum mismatch")
                return False
            
            logger.info(f"🔄 Starting restore from backup: {backup_id}")
            
            # Extract backup
            restore_path = Path(restore_path)
            restore_path.mkdir(exist_ok=True)
            
            with tarfile.open(backup_file, "r:*") as tar:
                tar.extractall(path=restore_path)
            
            logger.info(f"✅ Restore completed: {backup_id} to {restore_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Restore failed: {backup_id} - {e}")
            return False
    
    def delete_backup(self, backup_id: str) -> bool:
        """Delete a backup"""
        try:
            backup_metadata = self.get_backup_status(backup_id)
            if not backup_metadata:
                logger.error(f"Backup not found: {backup_id}")
                return False
            
            # Delete backup file
            backup_file = Path(backup_metadata.file_path)
            if backup_file.exists():
                backup_file.unlink()
            
            # Remove from metadata
            with self.lock:
                self.metadata = [b for b in self.metadata if b.backup_id != backup_id]
                self._save_metadata()
            
            logger.info(f"🗑️ Deleted backup: {backup_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting backup: {backup_id} - {e}")
            return False
    
    def cleanup_old_backups(self):
        """Clean up expired backups based on retention policy"""
        try:
            cleaned_count = 0
            
            for backup in self.metadata.copy():
                if backup.retention_days > 0:
                    expiry_date = backup.created_at + timedelta(days=backup.retention_days)
                    
                    if datetime.now() > expiry_date:
                        if self.delete_backup(backup.backup_id):
                            cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info(f"🧹 Cleaned up {cleaned_count} expired backups")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error during backup cleanup: {e}")
            return 0
    
    def get_backup_statistics(self) -> Dict[str, Any]:
        """Get backup system statistics"""
        try:
            total_backups = len(self.metadata)
            completed_backups = len([b for b in self.metadata if b.status == BackupStatus.COMPLETED])
            failed_backups = len([b for b in self.metadata if b.status == BackupStatus.FAILED])
            
            total_size = sum(b.file_size for b in self.metadata if b.status == BackupStatus.COMPLETED)
            
            # Calculate disk usage
            disk_usage = sum(Path(b.file_path).stat().st_size for b in self.metadata 
                           if Path(b.file_path).exists())
            
            # Recent backup info
            recent_backups = self.list_backups(days=7)
            
            return {
                "total_backups": total_backups,
                "completed_backups": completed_backups,
                "failed_backups": failed_backups,
                "success_rate": (completed_backups / total_backups * 100) if total_backups > 0 else 0,
                "total_size_bytes": total_size,
                "disk_usage_bytes": disk_usage,
                "recent_backups_count": len(recent_backups),
                "backup_directory": str(self.backup_directory),
                "oldest_backup": min(self.metadata, key=lambda x: x.created_at).created_at.isoformat() if self.metadata else None,
                "newest_backup": max(self.metadata, key=lambda x: x.created_at).created_at.isoformat() if self.metadata else None
            }
            
        except Exception as e:
            logger.error(f"Error calculating backup statistics: {e}")
            return {"error": str(e)}

# Global backup service instance
backup_service = BackupService()

if __name__ == "__main__":
    # Test backup service
    print("🧪 Testing Backup Service...")
    
    service = BackupService("test_backups")
    
    # Create a test backup
    backup_id = service.create_backup(
        backup_type=BackupType.CONFIG_ONLY,
        description="Test backup",
        includes=["README.md", "package.json"],
        retention_days=7
    )
    
    print(f"Created backup: {backup_id}")
    
    # Wait a moment for backup to complete
    import time
    time.sleep(2)
    
    # Check status
    status = service.get_backup_status(backup_id)
    if status:
        print(f"Backup status: {status.status.value}")
    
    # Get statistics
    stats = service.get_backup_statistics()
    print(f"Backup statistics: {stats}")
    
    # List backups
    backups = service.list_backups()
    print(f"Total backups: {len(backups)}")
    
    # Cleanup test directory
    import shutil
    if Path("test_backups").exists():
        shutil.rmtree("test_backups")
    
    print("✅ Backup service test completed!")