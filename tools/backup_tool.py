#!/usr/bin/env python3
"""
WordPress Backup Tool
A comprehensive tool for backing up WordPress installations
"""

import os
import sys
import subprocess
import json
import tarfile
import zipfile
import gzip
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import argparse
from datetime import datetime
import hashlib
import tempfile

class WordPressBackup:
    """WordPress backup and restore tool"""
    
    def __init__(self, wp_path: str = None):
        self.wp_path = os.path.abspath(wp_path) if wp_path else os.getcwd()
        self.wp_cli_path = None
        self.backup_config = {
            'exclude_files': [
                'wp-content/cache/*',
                'wp-content/uploads/cache/*',
                'wp-content/backup*',
                'wp-content/backups/*',
                'wp-content/upgrade/*',
                'wp-content/debug.log',
                '.git/*',
                '.svn/*',
                'node_modules/*',
                '*.log',
                '.DS_Store',
                'Thumbs.db'
            ],
            'exclude_dirs': [
                'wp-content/cache',
                'wp-content/backup*',
                'wp-content/backups',
                'wp-content/upgrade',
                '.git',
                '.svn',
                'node_modules'
            ]
        }
    
    def check_wp_cli(self) -> bool:
        """Check if WP-CLI is available"""
        try:
            result = subprocess.run(['wp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.wp_cli_path = 'wp'
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Check for local wp-cli.phar
        wp_cli_path = os.path.join(self.wp_path, 'wp-cli.phar')
        if os.path.exists(wp_cli_path):
            try:
                result = subprocess.run(['php', wp_cli_path, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.wp_cli_path = f'php {wp_cli_path}'
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        
        return False
    
    def run_wp_cli(self, command: str) -> Tuple[bool, str, str]:
        """Run WP-CLI command"""
        if not self.check_wp_cli():
            return False, "", "WP-CLI not available"
        
        try:
            original_dir = os.getcwd()
            os.chdir(self.wp_path)
            
            full_command = f"{self.wp_cli_path} {command}"
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
            
            return result.returncode == 0, result.stdout, result.stderr
            
        except Exception as e:
            return False, "", str(e)
        finally:
            os.chdir(original_dir)
    
    def get_backup_info(self) -> Dict[str, Any]:
        """Get information about the WordPress installation for backup"""
        print("Gathering WordPress installation information...")
        
        info = {
            'wp_path': self.wp_path,
            'backup_date': datetime.now().isoformat(),
            'wordpress_version': None,
            'database_config': None,
            'file_count': 0,
            'total_size': 0,
            'themes': [],
            'plugins': []
        }
        
        # Get WordPress version
        if self.check_wp_cli():
            success, output, error = self.run_wp_cli("core version")
            if success:
                info['wordpress_version'] = output.strip()
        
        # Get database configuration
        wp_config_path = os.path.join(self.wp_path, 'wp-config.php')
        if os.path.exists(wp_config_path):
            info['database_config'] = self.extract_db_config(wp_config_path)
        
        # Count files and calculate size
        file_count, total_size = self.calculate_directory_size()
        info['file_count'] = file_count
        info['total_size'] = total_size
        
        # Get themes and plugins
        if self.check_wp_cli():
            # Get themes
            success, output, error = self.run_wp_cli("theme list --format=json")
            if success:
                try:
                    info['themes'] = json.loads(output)
                except json.JSONDecodeError:
                    pass
            
            # Get plugins
            success, output, error = self.run_wp_cli("plugin list --format=json")
            if success:
                try:
                    info['plugins'] = json.loads(output)
                except json.JSONDecodeError:
                    pass
        
        return info
    
    def extract_db_config(self, wp_config_path: str) -> Dict[str, str]:
        """Extract database configuration from wp-config.php"""
        config = {}
        try:
            with open(wp_config_path, 'r') as f:
                content = f.read()
            
            import re
            
            # Extract database configuration
            patterns = {
                'db_name': r"define\s*\(\s*['\"]DB_NAME['\"]\s*,\s*['\"]([^'\"]*)['\"]",
                'db_user': r"define\s*\(\s*['\"]DB_USER['\"]\s*,\s*['\"]([^'\"]*)['\"]",
                'db_host': r"define\s*\(\s*['\"]DB_HOST['\"]\s*,\s*['\"]([^'\"]*)['\"]",
                'table_prefix': r"\$table_prefix\s*=\s*['\"]([^'\"]*)['\"]"
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                if match:
                    config[key] = match.group(1)
            
        except Exception as e:
            print(f"Failed to extract database config: {e}")
        
        return config
    
    def calculate_directory_size(self) -> Tuple[int, int]:
        """Calculate total file count and size in WordPress directory"""
        file_count = 0
        total_size = 0
        
        for root, dirs, files in os.walk(self.wp_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not self.should_exclude_directory(os.path.join(root, d))]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                if not self.should_exclude_file(file_path):
                    try:
                        total_size += os.path.getsize(file_path)
                        file_count += 1
                    except OSError:
                        pass  # Skip files that can't be accessed
        
        return file_count, total_size
    
    def should_exclude_file(self, file_path: str) -> bool:
        """Check if a file should be excluded from backup"""
        relative_path = os.path.relpath(file_path, self.wp_path)
        
        for pattern in self.backup_config['exclude_files']:
            if self.match_pattern(relative_path, pattern):
                return True
        
        return False
    
    def should_exclude_directory(self, dir_path: str) -> bool:
        """Check if a directory should be excluded from backup"""
        relative_path = os.path.relpath(dir_path, self.wp_path)
        
        for pattern in self.backup_config['exclude_dirs']:
            if self.match_pattern(relative_path, pattern):
                return True
        
        return False
    
    def match_pattern(self, path: str, pattern: str) -> bool:
        """Simple pattern matching for backup exclusions"""
        import fnmatch
        
        # Convert pattern to Unix-style path
        pattern = pattern.replace('\\', '/')
        path = path.replace('\\', '/')
        
        return fnmatch.fnmatch(path, pattern)
    
    def create_full_backup(self, output_path: str, compress: bool = True) -> bool:
        """Create a full WordPress backup including files and database"""
        print(f"Creating full WordPress backup: {output_path}")
        
        try:
            # Create temporary directory for backup
            with tempfile.TemporaryDirectory() as temp_dir:
                backup_dir = os.path.join(temp_dir, 'backup')
                os.makedirs(backup_dir, exist_ok=True)
                
                # Backup files
                files_backup = os.path.join(backup_dir, 'files.tar')
                if not self.backup_files(files_backup):
                    return False
                
                # Backup database
                db_backup = os.path.join(backup_dir, 'database.sql')
                if not self.backup_database(db_backup):
                    return False
                
                # Create backup info
                info = self.get_backup_info()
                info_file = os.path.join(backup_dir, 'backup_info.json')
                with open(info_file, 'w') as f:
                    json.dump(info, f, indent=2)
                
                # Create final backup archive
                if compress:
                    if output_path.endswith('.zip'):
                        self.create_zip_archive(backup_dir, output_path)
                    else:
                        self.create_tar_archive(backup_dir, output_path, compress=True)
                else:
                    if output_path.endswith('.zip'):
                        self.create_zip_archive(backup_dir, output_path)
                    else:
                        self.create_tar_archive(backup_dir, output_path, compress=False)
                
                print(f"Full backup created successfully: {output_path}")
                return True
                
        except Exception as e:
            print(f"Failed to create full backup: {e}")
            return False
    
    def backup_files(self, output_path: str) -> bool:
        """Backup WordPress files"""
        print("Backing up WordPress files...")
        
        try:
            with tarfile.open(output_path, 'w') as tar:
                for root, dirs, files in os.walk(self.wp_path):
                    # Skip excluded directories
                    dirs[:] = [d for d in dirs if not self.should_exclude_directory(os.path.join(root, d))]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        if not self.should_exclude_file(file_path):
                            arcname = os.path.relpath(file_path, self.wp_path)
                            tar.add(file_path, arcname=arcname)
            
            print(f"Files backed up successfully: {output_path}")
            return True
            
        except Exception as e:
            print(f"Failed to backup files: {e}")
            return False
    
    def backup_database(self, output_path: str) -> bool:
        """Backup WordPress database"""
        print("Backing up WordPress database...")
        
        if self.check_wp_cli():
            success, output, error = self.run_wp_cli(f"db export {output_path}")
            if success:
                print(f"Database backed up successfully: {output_path}")
                return True
            else:
                print(f"WP-CLI database backup failed: {error}")
        
        # Fallback to manual database backup
        print("WP-CLI not available, attempting manual database backup...")
        return self.manual_database_backup(output_path)
    
    def manual_database_backup(self, output_path: str) -> bool:
        """Manual database backup without WP-CLI"""
        try:
            db_config = self.extract_db_config(os.path.join(self.wp_path, 'wp-config.php'))
            
            if not db_config:
                print("Database configuration not found")
                return False
            
            # Try to use mysqldump
            cmd = [
                'mysqldump',
                '-h', db_config.get('db_host', 'localhost'),
                '-u', db_config.get('db_user', 'root'),
                f'-p{db_config.get("db_pass", "")}',
                '--single-transaction',
                '--routines',
                '--triggers',
                db_config.get('db_name', 'wordpress')
            ]
            
            with open(output_path, 'w') as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
            
            if result.returncode == 0:
                print(f"Database backed up successfully: {output_path}")
                return True
            else:
                print(f"mysqldump failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Manual database backup failed: {e}")
            return False
    
    def create_tar_archive(self, source_dir: str, output_path: str, compress: bool = True) -> bool:
        """Create tar archive from directory"""
        try:
            mode = 'w:gz' if compress else 'w'
            
            with tarfile.open(output_path, mode) as tar:
                tar.add(source_dir, arcname='backup')
            
            return True
            
        except Exception as e:
            print(f"Failed to create tar archive: {e}")
            return False
    
    def create_zip_archive(self, source_dir: str, output_path: str) -> bool:
        """Create zip archive from directory"""
        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)
            
            return True
            
        except Exception as e:
            print(f"Failed to create zip archive: {e}")
            return False
    
    def restore_backup(self, backup_path: str, target_path: str = None) -> bool:
        """Restore WordPress from backup"""
        if not target_path:
            target_path = self.wp_path
        
        print(f"Restoring WordPress backup: {backup_path}")
        print(f"Target path: {target_path}")
        
        if not os.path.exists(backup_path):
            print(f"Backup file not found: {backup_path}")
            return False
        
        try:
            # Extract backup to temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                self.extract_backup(backup_path, temp_dir)
                
                backup_dir = os.path.join(temp_dir, 'backup')
                
                # Check if backup info exists
                info_file = os.path.join(backup_dir, 'backup_info.json')
                backup_info = {}
                if os.path.exists(info_file):
                    with open(info_file, 'r') as f:
                        backup_info = json.load(f)
                
                # Restore files
                files_backup = os.path.join(backup_dir, 'files.tar')
                if os.path.exists(files_backup):
                    if not self.restore_files(files_backup, target_path):
                        return False
                
                # Restore database
                db_backup = os.path.join(backup_dir, 'database.sql')
                if os.path.exists(db_backup):
                    if not self.restore_database(db_backup, target_path):
                        return False
                
                print("WordPress backup restored successfully!")
                return True
                
        except Exception as e:
            print(f"Failed to restore backup: {e}")
            return False
    
    def extract_backup(self, backup_path: str, extract_dir: str) -> bool:
        """Extract backup archive"""
        print(f"Extracting backup: {backup_path}")
        
        try:
            if backup_path.endswith('.zip'):
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    zipf.extractall(extract_dir)
            elif backup_path.endswith('.tar.gz') or backup_path.endswith('.tgz'):
                with tarfile.open(backup_path, 'r:gz') as tar:
                    tar.extractall(extract_dir)
            elif backup_path.endswith('.tar'):
                with tarfile.open(backup_path, 'r') as tar:
                    tar.extractall(extract_dir)
            else:
                print(f"Unsupported backup format: {backup_path}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Failed to extract backup: {e}")
            return False
    
    def restore_files(self, files_backup: str, target_path: str) -> bool:
        """Restore WordPress files"""
        print("Restoring WordPress files...")
        
        try:
            # Create target directory if it doesn't exist
            os.makedirs(target_path, exist_ok=True)
            
            # Extract files
            with tarfile.open(files_backup, 'r') as tar:
                tar.extractall(target_path)
            
            print("Files restored successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to restore files: {e}")
            return False
    
    def restore_database(self, db_backup: str, target_path: str) -> bool:
        """Restore WordPress database"""
        print("Restoring WordPress database...")
        
        if self.check_wp_cli():
            original_dir = os.getcwd()
            os.chdir(target_path)
            
            success, output, error = self.run_wp_cli(f"db import {db_backup}")
            
            os.chdir(original_dir)
            
            if success:
                print("Database restored successfully!")
                return True
            else:
                print(f"WP-CLI database restore failed: {error}")
        
        # Fallback to manual database restore
        print("WP-CLI not available, attempting manual database restore...")
        return self.manual_database_restore(db_backup, target_path)
    
    def manual_database_restore(self, db_backup: str, target_path: str) -> bool:
        """Manual database restore without WP-CLI"""
        try:
            wp_config_path = os.path.join(target_path, 'wp-config.php')
            db_config = self.extract_db_config(wp_config_path)
            
            if not db_config:
                print("Database configuration not found")
                return False
            
            # Try to use mysql command
            cmd = [
                'mysql',
                '-h', db_config.get('db_host', 'localhost'),
                '-u', db_config.get('db_user', 'root'),
                f'-p{db_config.get("db_pass", "")}',
                db_config.get('db_name', 'wordpress')
            ]
            
            with open(db_backup, 'r') as f:
                result = subprocess.run(cmd, stdin=f, stderr=subprocess.PIPE, text=True)
            
            if result.returncode == 0:
                print("Database restored successfully!")
                return True
            else:
                print(f"mysql restore failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Manual database restore failed: {e}")
            return False
    
    def list_backups(self, backup_dir: str) -> List[Dict[str, Any]]:
        """List available backups in a directory"""
        backups = []
        
        if not os.path.exists(backup_dir):
            return backups
        
        for file in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, file)
            
            if os.path.isfile(file_path) and (file.endswith('.zip') or file.endswith('.tar.gz') or file.endswith('.tar')):
                try:
                    stat = os.stat(file_path)
                    backup_info = {
                        'filename': file,
                        'path': file_path,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'type': 'full'
                    }
                    backups.append(backup_info)
                except OSError:
                    pass
        
        # Sort by modification time (newest first)
        backups.sort(key=lambda x: x['modified'], reverse=True)
        
        return backups
    
    def verify_backup(self, backup_path: str) -> bool:
        """Verify backup integrity"""
        print(f"Verifying backup: {backup_path}")
        
        if not os.path.exists(backup_path):
            print("Backup file not found")
            return False
        
        try:
            # Check if archive can be opened
            if backup_path.endswith('.zip'):
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    if zipf.testzip() is not None:
                        print("Backup archive is corrupted")
                        return False
            elif backup_path.endswith('.tar.gz') or backup_path.endswith('.tgz'):
                with tarfile.open(backup_path, 'r:gz') as tar:
                    pass  # Test opening
            elif backup_path.endswith('.tar'):
                with tarfile.open(backup_path, 'r') as tar:
                    pass  # Test opening
            
            print("Backup verification successful!")
            return True
            
        except Exception as e:
            print(f"Backup verification failed: {e}")
            return False

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='WordPress Backup Tool')
    parser.add_argument('--wp-path', default='.', help='WordPress installation path')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create backup
    backup_parser = subparsers.add_parser('backup', help='Create backup')
    backup_parser.add_argument('output', help='Output backup file path')
    backup_parser.add_argument('--compress', action='store_true', help='Compress backup')
    
    # Restore backup
    restore_parser = subparsers.add_parser('restore', help='Restore backup')
    restore_parser.add_argument('backup', help='Backup file path')
    restore_parser.add_argument('--target', help='Target path for restore')
    
    # List backups
    list_parser = subparsers.add_parser('list', help='List backups')
    list_parser.add_argument('directory', help='Directory to search for backups')
    
    # Verify backup
    verify_parser = subparsers.add_parser('verify', help='Verify backup')
    verify_parser.add_argument('backup', help='Backup file path')
    
    # Backup info
    info_parser = subparsers.add_parser('info', help='Get backup information')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    backup_tool = WordPressBackup(args.wp_path)
    
    if args.command == 'backup':
        success = backup_tool.create_full_backup(args.output, args.compress)
        sys.exit(0 if success else 1)
    
    elif args.command == 'restore':
        success = backup_tool.restore_backup(args.backup, args.target)
        sys.exit(0 if success else 1)
    
    elif args.command == 'list':
        backups = backup_tool.list_backups(args.directory)
        for backup in backups:
            print(f"{backup['filename']} - {backup['size']} bytes - {backup['modified']}")
    
    elif args.command == 'verify':
        success = backup_tool.verify_backup(args.backup)
        sys.exit(0 if success else 1)
    
    elif args.command == 'info':
        info = backup_tool.get_backup_info()
        print(json.dumps(info, indent=2))

if __name__ == '__main__':
    main()
