#!/usr/bin/env python3
"""
WordPress Database Manager Tool
A comprehensive tool for managing WordPress databases
"""

import os
import sys
import subprocess
import json
import sqlite3
import mysql.connector
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import argparse
from datetime import datetime
import gzip
import shutil

class DatabaseManager:
    """WordPress database management tool"""
    
    def __init__(self, wp_path: str = None):
        self.wp_path = wp_path or os.getcwd()
        self.wp_cli_path = None
        self.db_config = self.get_db_config()
        
    def get_db_config(self) -> Dict[str, str]:
        """Get database configuration from wp-config.php"""
        wp_config_path = os.path.join(self.wp_path, 'wp-config.php')
        
        if not os.path.exists(wp_config_path):
            print("wp-config.php not found")
            return {}
        
        config = {}
        try:
            with open(wp_config_path, 'r') as f:
                content = f.read()
            
            # Extract database configuration
            import re
            
            db_name_match = re.search(r"define\s*\(\s*['\"]DB_NAME['\"]\s*,\s*['\"]([^'\"]*)['\"]", content)
            if db_name_match:
                config['db_name'] = db_name_match.group(1)
            
            db_user_match = re.search(r"define\s*\(\s*['\"]DB_USER['\"]\s*,\s*['\"]([^'\"]*)['\"]", content)
            if db_user_match:
                config['db_user'] = db_user_match.group(1)
            
            db_pass_match = re.search(r"define\s*\(\s*['\"]DB_PASSWORD['\"]\s*,\s*['\"]([^'\"]*)['\"]", content)
            if db_pass_match:
                config['db_pass'] = db_pass_match.group(1)
            
            db_host_match = re.search(r"define\s*\(\s*['\"]DB_HOST['\"]\s*,\s*['\"]([^'\"]*)['\"]", content)
            if db_host_match:
                config['db_host'] = db_host_match.group(1)
            
            table_prefix_match = re.search(r"\$table_prefix\s*=\s*['\"]([^'\"]*)['\"]", content)
            if table_prefix_match:
                config['table_prefix'] = table_prefix_match.group(1)
            
        except Exception as e:
            print(f"Failed to read wp-config.php: {e}")
        
        return config
    
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
    
    def get_database_connection(self):
        """Get database connection based on configuration"""
        if not self.db_config:
            print("Database configuration not found")
            return None
        
        db_host = self.db_config.get('db_host', 'localhost')
        
        # Check if it's SQLite
        if db_host.startswith('localhost:') and db_host.endswith('.db'):
            db_path = db_host.split(':', 1)[1]
            try:
                return sqlite3.connect(db_path)
            except Exception as e:
                print(f"Failed to connect to SQLite database: {e}")
                return None
        
        # MySQL/MariaDB connection
        try:
            return mysql.connector.connect(
                host=db_host,
                database=self.db_config['db_name'],
                user=self.db_config['db_user'],
                password=self.db_config['db_pass']
            )
        except Exception as e:
            print(f"Failed to connect to MySQL database: {e}")
            return None
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database information"""
        print("Getting database information...")
        
        conn = self.get_database_connection()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor()
            
            # Get database version
            if isinstance(conn, sqlite3.Connection):
                cursor.execute("SELECT sqlite_version()")
                version = cursor.fetchone()[0]
                db_type = "SQLite"
            else:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                db_type = "MySQL"
            
            # Get table count
            table_prefix = self.db_config.get('table_prefix', 'wp_')
            
            if isinstance(conn, sqlite3.Connection):
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?", (f"{table_prefix}%",))
                tables = cursor.fetchall()
            else:
                cursor.execute(f"SHOW TABLES LIKE '{table_prefix}%'")
                tables = cursor.fetchall()
            
            table_count = len(tables)
            
            # Get database size
            if isinstance(conn, sqlite3.Connection):
                db_path = conn.execute("PRAGMA database_list").fetchone()[2]
                db_size = os.path.getsize(db_path)
            else:
                cursor.execute("""
                    SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'DB Size in MB'
                    FROM information_schema.tables
                    WHERE table_schema = %s
                """, (self.db_config['db_name'],))
                db_size = cursor.fetchone()[0] * 1024 * 1024  # Convert to bytes
            
            info = {
                'db_type': db_type,
                'version': version,
                'table_count': table_count,
                'database_size': db_size,
                'table_prefix': table_prefix,
                'last_checked': datetime.now().isoformat()
            }
            
            cursor.close()
            return info
            
        except Exception as e:
            print(f"Failed to get database info: {e}")
            return {}
        finally:
            conn.close()
    
    def list_tables(self) -> List[str]:
        """List all WordPress tables"""
        print("Listing WordPress tables...")
        
        conn = self.get_database_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            table_prefix = self.db_config.get('table_prefix', 'wp_')
            
            if isinstance(conn, sqlite3.Connection):
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?", (f"{table_prefix}%",))
                tables = [row[0] for row in cursor.fetchall()]
            else:
                cursor.execute(f"SHOW TABLES LIKE '{table_prefix}%'")
                tables = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            return tables
            
        except Exception as e:
            print(f"Failed to list tables: {e}")
            return []
        finally:
            conn.close()
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get information about a specific table"""
        print(f"Getting information for table: {table_name}")
        
        conn = self.get_database_connection()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor()
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            row_count = cursor.fetchone()[0]
            
            # Get table structure
            if isinstance(conn, sqlite3.Connection):
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
            else:
                cursor.execute(f"DESCRIBE `{table_name}`")
                columns = cursor.fetchall()
            
            # Get table size
            if isinstance(conn, sqlite3.Connection):
                # SQLite doesn't have easy table size info
                table_size = 0
            else:
                cursor.execute("""
                    SELECT ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size in MB'
                    FROM information_schema.TABLES
                    WHERE table_schema = %s AND table_name = %s
                """, (self.db_config['db_name'], table_name))
                result = cursor.fetchone()
                table_size = result[0] * 1024 * 1024 if result else 0
            
            info = {
                'table_name': table_name,
                'row_count': row_count,
                'column_count': len(columns),
                'table_size': table_size,
                'columns': columns
            }
            
            cursor.close()
            return info
            
        except Exception as e:
            print(f"Failed to get table info: {e}")
            return {}
        finally:
            conn.close()
    
    def backup_database(self, output_file: str, compress: bool = True) -> bool:
        """Backup the WordPress database"""
        print(f"Creating database backup: {output_file}")
        
        if not self.db_config:
            print("Database configuration not found")
            return False
        
        try:
            # Use WP-CLI for backup if available
            if self.check_wp_cli():
                success, output, error = self.run_wp_cli(f"db export {output_file}")
                if success:
                    if compress and not output_file.endswith('.gz'):
                        # Compress the backup
                        with open(output_file, 'rb') as f_in:
                            with gzip.open(f"{output_file}.gz", 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        os.remove(output_file)
                        print(f"Database backup created and compressed: {output_file}.gz")
                    else:
                        print(f"Database backup created: {output_file}")
                    return True
                else:
                    print(f"WP-CLI backup failed: {error}")
            
            # Fallback to direct database backup
            conn = self.get_database_connection()
            if not conn:
                return False
            
            if isinstance(conn, sqlite3.Connection):
                # SQLite backup
                backup_conn = sqlite3.connect(output_file)
                conn.backup(backup_conn)
                backup_conn.close()
            else:
                # MySQL backup using mysqldump
                import subprocess
                
                cmd = [
                    'mysqldump',
                    '-h', self.db_config['db_host'],
                    '-u', self.db_config['db_user'],
                    f'-p{self.db_config["db_pass"]}',
                    '--single-transaction',
                    '--routines',
                    '--triggers',
                    self.db_config['db_name']
                ]
                
                with open(output_file, 'w') as f:
                    result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
                
                if result.returncode != 0:
                    print(f"mysqldump failed: {result.stderr}")
                    return False
            
            conn.close()
            
            if compress and not output_file.endswith('.gz'):
                # Compress the backup
                with open(output_file, 'rb') as f_in:
                    with gzip.open(f"{output_file}.gz", 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(output_file)
                print(f"Database backup created and compressed: {output_file}.gz")
            else:
                print(f"Database backup created: {output_file}")
            
            return True
            
        except Exception as e:
            print(f"Failed to create database backup: {e}")
            return False
    
    def restore_database(self, backup_file: str) -> bool:
        """Restore database from backup"""
        print(f"Restoring database from: {backup_file}")
        
        if not os.path.exists(backup_file):
            print(f"Backup file not found: {backup_file}")
            return False
        
        try:
            # Handle compressed backups
            if backup_file.endswith('.gz'):
                # Decompress backup
                decompressed_file = backup_file[:-3]  # Remove .gz
                with gzip.open(backup_file, 'rb') as f_in:
                    with open(decompressed_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                backup_file = decompressed_file
            
            # Use WP-CLI for restore if available
            if self.check_wp_cli():
                success, output, error = self.run_wp_cli(f"db import {backup_file}")
                if success:
                    print("Database restored successfully!")
                    return True
                else:
                    print(f"WP-CLI restore failed: {error}")
            
            # Fallback to direct database restore
            conn = self.get_database_connection()
            if not conn:
                return False
            
            if isinstance(conn, sqlite3.Connection):
                # SQLite restore
                conn.close()
                shutil.copy2(backup_file, conn.execute("PRAGMA database_list").fetchone()[2])
            else:
                # MySQL restore
                import subprocess
                
                cmd = [
                    'mysql',
                    '-h', self.db_config['db_host'],
                    '-u', self.db_config['db_user'],
                    f'-p{self.db_config["db_pass"]}',
                    self.db_config['db_name']
                ]
                
                with open(backup_file, 'r') as f:
                    result = subprocess.run(cmd, stdin=f, stderr=subprocess.PIPE, text=True)
                
                if result.returncode != 0:
                    print(f"mysql restore failed: {result.stderr}")
                    return False
            
            print("Database restored successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to restore database: {e}")
            return False
        finally:
            # Clean up decompressed file if it was created
            if backup_file.endswith('.gz') and os.path.exists(backup_file[:-3]):
                os.remove(backup_file[:-3])
    
    def optimize_database(self) -> bool:
        """Optimize WordPress database"""
        print("Optimizing database...")
        
        if self.check_wp_cli():
            success, output, error = self.run_wp_cli("db optimize")
            if success:
                print("Database optimized successfully!")
                return True
            else:
                print(f"WP-CLI optimization failed: {error}")
        
        # Fallback to manual optimization
        conn = self.get_database_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            tables = self.list_tables()
            
            for table in tables:
                if isinstance(conn, sqlite3.Connection):
                    cursor.execute(f"VACUUM `{table}`")
                else:
                    cursor.execute(f"OPTIMIZE TABLE `{table}`")
            
            conn.commit()
            cursor.close()
            print("Database optimized successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to optimize database: {e}")
            return False
        finally:
            conn.close()
    
    def repair_database(self) -> bool:
        """Repair WordPress database"""
        print("Repairing database...")
        
        if self.check_wp_cli():
            success, output, error = self.run_wp_cli("db repair")
            if success:
                print("Database repaired successfully!")
                return True
            else:
                print(f"WP-CLI repair failed: {error}")
        
        # Fallback to manual repair
        conn = self.get_database_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            tables = self.list_tables()
            
            for table in tables:
                if isinstance(conn, sqlite3.Connection):
                    # SQLite doesn't have a repair command
                    cursor.execute(f"REINDEX `{table}`")
                else:
                    cursor.execute(f"REPAIR TABLE `{table}`")
            
            conn.commit()
            cursor.close()
            print("Database repaired successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to repair database: {e}")
            return False
        finally:
            conn.close()
    
    def clean_database(self) -> bool:
        """Clean up WordPress database"""
        print("Cleaning database...")
        
        if self.check_wp_cli():
            # Clean revisions, spam comments, etc.
            commands = [
                "post delete $(wp post list --post_type=revision --format=ids)",
                "comment delete $(wp comment list --status=spam --format=ids)",
                "comment delete $(wp comment list --status=trash --format=ids)",
                "post delete $(wp post list --post_status=trash --format=ids)",
                "post delete $(wp post list --post_type=attachment --post_status=inherit --format=ids)",
            ]
            
            for command in commands:
                success, output, error = self.run_wp_cli(command)
                if not success:
                    print(f"Cleanup command failed: {error}")
            
            print("Database cleaned successfully!")
            return True
        
        print("WP-CLI not available for database cleaning")
        return False
    
    def search_replace(self, search: str, replace: str, dry_run: bool = True) -> bool:
        """Search and replace in database"""
        print(f"Search and replace: '{search}' -> '{replace}'")
        
        if self.check_wp_cli():
            command = f"search-replace '{search}' '{replace}'"
            if dry_run:
                command += " --dry-run"
            
            success, output, error = self.run_wp_cli(command)
            
            if success:
                if dry_run:
                    print("Dry run completed. Use --execute to perform the replacement.")
                else:
                    print("Search and replace completed successfully!")
                return True
            else:
                print(f"Search and replace failed: {error}")
                return False
        
        print("WP-CLI not available for search and replace")
        return False
    
    def query_database(self, query: str) -> List[Tuple]:
        """Execute a custom database query"""
        print(f"Executing query: {query}")
        
        conn = self.get_database_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
            
        except Exception as e:
            print(f"Query failed: {e}")
            return []
        finally:
            conn.close()

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='WordPress Database Manager Tool')
    parser.add_argument('--wp-path', default='.', help='WordPress installation path')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Database info
    info_parser = subparsers.add_parser('info', help='Get database information')
    
    # List tables
    tables_parser = subparsers.add_parser('tables', help='List database tables')
    
    # Table info
    table_info_parser = subparsers.add_parser('table-info', help='Get table information')
    table_info_parser.add_argument('table', help='Table name')
    
    # Backup database
    backup_parser = subparsers.add_parser('backup', help='Backup database')
    backup_parser.add_argument('output', help='Output file path')
    backup_parser.add_argument('--compress', action='store_true', help='Compress backup')
    
    # Restore database
    restore_parser = subparsers.add_parser('restore', help='Restore database')
    restore_parser.add_argument('backup', help='Backup file path')
    
    # Optimize database
    optimize_parser = subparsers.add_parser('optimize', help='Optimize database')
    
    # Repair database
    repair_parser = subparsers.add_parser('repair', help='Repair database')
    
    # Clean database
    clean_parser = subparsers.add_parser('clean', help='Clean database')
    
    # Search and replace
    sr_parser = subparsers.add_parser('search-replace', help='Search and replace in database')
    sr_parser.add_argument('search', help='Search string')
    sr_parser.add_argument('replace', help='Replace string')
    sr_parser.add_argument('--execute', action='store_true', help='Execute replacement (default is dry run)')
    
    # Query database
    query_parser = subparsers.add_parser('query', help='Execute custom query')
    query_parser.add_argument('sql', help='SQL query')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    db_manager = DatabaseManager(args.wp_path)
    
    if args.command == 'info':
        info = db_manager.get_database_info()
        print(json.dumps(info, indent=2))
    
    elif args.command == 'tables':
        tables = db_manager.list_tables()
        for table in tables:
            print(table)
    
    elif args.command == 'table-info':
        info = db_manager.get_table_info(args.table)
        print(json.dumps(info, indent=2))
    
    elif args.command == 'backup':
        success = db_manager.backup_database(args.output, args.compress)
        sys.exit(0 if success else 1)
    
    elif args.command == 'restore':
        success = db_manager.restore_database(args.backup)
        sys.exit(0 if success else 1)
    
    elif args.command == 'optimize':
        success = db_manager.optimize_database()
        sys.exit(0 if success else 1)
    
    elif args.command == 'repair':
        success = db_manager.repair_database()
        sys.exit(0 if success else 1)
    
    elif args.command == 'clean':
        success = db_manager.clean_database()
        sys.exit(0 if success else 1)
    
    elif args.command == 'search-replace':
        success = db_manager.search_replace(args.search, args.replace, not args.execute)
        sys.exit(0 if success else 1)
    
    elif args.command == 'query':
        results = db_manager.query_database(args.sql)
        for row in results:
            print(row)

if __name__ == '__main__':
    main()
