#!/usr/bin/env python3
"""
WordPress Installer Tool
A comprehensive tool for installing and configuring WordPress installations
"""

import os
import sys
import subprocess
import requests
import zipfile
import tempfile
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse

class WordPressInstaller:
    """WordPress installation and configuration tool"""
    
    def __init__(self):
        self.wp_cli_path = None
        self.wordpress_version = "latest"
        self.default_config = {
            'db_host': 'localhost',
            'db_name': 'wordpress',
            'db_user': 'root',
            'db_pass': '',
            'table_prefix': 'wp_',
            'site_url': 'http://localhost',
            'admin_user': 'admin',
            'admin_pass': 'admin',
            'admin_email': 'admin@example.com',
            'site_title': 'My WordPress Site'
        }
    
    def check_wp_cli(self) -> bool:
        """Check if WP-CLI is installed and available"""
        try:
            result = subprocess.run(['wp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.wp_cli_path = 'wp'
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Check for local wp-cli.phar
        if os.path.exists('wp-cli.phar'):
            try:
                result = subprocess.run(['php', 'wp-cli.phar', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.wp_cli_path = 'php wp-cli.phar'
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        
        return False
    
    def install_wp_cli(self) -> bool:
        """Install WP-CLI if not available"""
        print("Installing WP-CLI...")
        try:
            # Download WP-CLI
            response = requests.get('https://raw.githubusercontent.com/wp-cli/wp-cli/gh-pages/phar/wp-cli.phar')
            response.raise_for_status()
            
            with open('wp-cli.phar', 'wb') as f:
                f.write(response.content)
            
            # Make it executable
            os.chmod('wp-cli.phar', 0o755)
            
            # Test installation
            result = subprocess.run(['php', 'wp-cli.phar', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.wp_cli_path = 'php wp-cli.phar'
                print("WP-CLI installed successfully!")
                return True
        except Exception as e:
            print(f"Failed to install WP-CLI: {e}")
        
        return False
    
    def download_wordpress(self, target_dir: str, version: str = "latest") -> bool:
        """Download WordPress to target directory"""
        print(f"Downloading WordPress {version}...")
        
        try:
            if version == "latest":
                download_url = "https://wordpress.org/latest.zip"
            else:
                download_url = f"https://wordpress.org/wordpress-{version}.zip"
            
            # Download WordPress
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name
            
            # Extract WordPress
            with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
            
            # Move WordPress files from wordpress/ subdirectory
            wordpress_dir = os.path.join(target_dir, 'wordpress')
            if os.path.exists(wordpress_dir):
                for item in os.listdir(wordpress_dir):
                    src = os.path.join(wordpress_dir, item)
                    dst = os.path.join(target_dir, item)
                    if os.path.isdir(src):
                        if os.path.exists(dst):
                            import shutil
                            shutil.rmtree(dst)
                        os.rename(src, dst)
                    else:
                        if os.path.exists(dst):
                            os.remove(dst)
                        os.rename(src, dst)
                
                # Remove empty wordpress directory
                os.rmdir(wordpress_dir)
            
            # Clean up
            os.unlink(tmp_file_path)
            
            print("WordPress downloaded successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to download WordPress: {e}")
            return False
    
    def create_wp_config(self, config: Dict[str, str], target_dir: str) -> bool:
        """Create wp-config.php file"""
        print("Creating wp-config.php...")
        
        try:
            config_content = f"""<?php
/**
 * WordPress configuration file
 * Generated by WordPress Installer Tool
 */

// ** Database settings ** //
define('DB_NAME', '{config['db_name']}');
define('DB_USER', '{config['db_user']}');
define('DB_PASSWORD', '{config['db_pass']}');
define('DB_HOST', '{config['db_host']}');
define('DB_CHARSET', 'utf8');
define('DB_COLLATE', '');

// ** Authentication Unique Keys and Salts ** //
define('AUTH_KEY',         '{self.generate_salt()}');
define('SECURE_AUTH_KEY',  '{self.generate_salt()}');
define('LOGGED_IN_KEY',    '{self.generate_salt()}');
define('NONCE_KEY',        '{self.generate_salt()}');
define('AUTH_SALT',        '{self.generate_salt()}');
define('SECURE_AUTH_SALT', '{self.generate_salt()}');
define('LOGGED_IN_SALT',   '{self.generate_salt()}');
define('NONCE_SALT',       '{self.generate_salt()}');

// ** WordPress Database Table prefix ** //
$table_prefix = '{config['table_prefix']}';

// ** For developers: WordPress debugging mode ** //
define('WP_DEBUG', false);
define('WP_DEBUG_LOG', false);
define('WP_DEBUG_DISPLAY', false);
define('SCRIPT_DEBUG', false);

// ** Absolute path to the WordPress directory ** //
if (!defined('ABSPATH')) {{
    define('ABSPATH', __DIR__ . '/');
}}

// ** Sets up WordPress vars and included files ** //
require_once ABSPATH . 'wp-settings.php';
"""
            
            config_path = os.path.join(target_dir, 'wp-config.php')
            with open(config_path, 'w') as f:
                f.write(config_content)
            
            print("wp-config.php created successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to create wp-config.php: {e}")
            return False
    
    def generate_salt(self) -> str:
        """Generate a random salt string"""
        import secrets
        import string
        
        chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
        return ''.join(secrets.choice(chars) for _ in range(64))
    
    def install_wordpress(self, config: Dict[str, str], target_dir: str) -> bool:
        """Install WordPress using WP-CLI"""
        if not self.check_wp_cli():
            if not self.install_wp_cli():
                print("WP-CLI is required for WordPress installation")
                return False
        
        print("Installing WordPress...")
        
        try:
            # Change to target directory
            original_dir = os.getcwd()
            os.chdir(target_dir)
            
            # Install WordPress
            cmd = f"{self.wp_cli_path} core install --url={config['site_url']} " \
                  f"--title='{config['site_title']}' " \
                  f"--admin_user={config['admin_user']} " \
                  f"--admin_password={config['admin_pass']} " \
                  f"--admin_email={config['admin_email']} " \
                  f"--skip-email"
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("WordPress installed successfully!")
                print(f"Admin URL: {config['site_url']}/wp-admin/")
                print(f"Admin Username: {config['admin_user']}")
                print(f"Admin Password: {config['admin_pass']}")
                return True
            else:
                print(f"WordPress installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Failed to install WordPress: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def install_plugins(self, plugins: List[str], target_dir: str) -> bool:
        """Install WordPress plugins"""
        if not self.wp_cli_path:
            print("WP-CLI is required for plugin installation")
            return False
        
        print(f"Installing plugins: {', '.join(plugins)}")
        
        try:
            original_dir = os.getcwd()
            os.chdir(target_dir)
            
            for plugin in plugins:
                cmd = f"{self.wp_cli_path} plugin install {plugin} --activate"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"Plugin '{plugin}' installed successfully!")
                else:
                    print(f"Failed to install plugin '{plugin}': {result.stderr}")
            
            return True
            
        except Exception as e:
            print(f"Failed to install plugins: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def install_themes(self, themes: List[str], target_dir: str) -> bool:
        """Install WordPress themes"""
        if not self.wp_cli_path:
            print("WP-CLI is required for theme installation")
            return False
        
        print(f"Installing themes: {', '.join(themes)}")
        
        try:
            original_dir = os.getcwd()
            os.chdir(target_dir)
            
            for theme in themes:
                cmd = f"{self.wp_cli_path} theme install {theme}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"Theme '{theme}' installed successfully!")
                else:
                    print(f"Failed to install theme '{theme}': {result.stderr}")
            
            return True
            
        except Exception as e:
            print(f"Failed to install themes: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def setup_database(self, config: Dict[str, str]) -> bool:
        """Setup database for WordPress"""
        print("Setting up database...")
        
        try:
            if config['db_host'] == 'localhost' and not config['db_pass']:
                # Try SQLite for local development
                return self.setup_sqlite_database(config)
            else:
                # Use MySQL/MariaDB
                return self.setup_mysql_database(config)
                
        except Exception as e:
            print(f"Failed to setup database: {e}")
            return False
    
    def setup_sqlite_database(self, config: Dict[str, str]) -> bool:
        """Setup SQLite database for local development"""
        print("Setting up SQLite database...")
        
        try:
            db_path = f"{config['db_name']}.db"
            
            # Create SQLite database
            conn = sqlite3.connect(db_path)
            conn.close()
            
            # Update config for SQLite
            config['db_host'] = f"localhost:{db_path}"
            
            print("SQLite database created successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to create SQLite database: {e}")
            return False
    
    def setup_mysql_database(self, config: Dict[str, str]) -> bool:
        """Setup MySQL database"""
        print("Setting up MySQL database...")
        
        try:
            import mysql.connector
            
            # Connect to MySQL server
            conn = mysql.connector.connect(
                host=config['db_host'],
                user=config['db_user'],
                password=config['db_pass']
            )
            
            cursor = conn.cursor()
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['db_name']}")
            
            cursor.close()
            conn.close()
            
            print("MySQL database created successfully!")
            return True
            
        except ImportError:
            print("mysql-connector-python is required for MySQL support")
            print("Install it with: pip install mysql-connector-python")
            return False
        except Exception as e:
            print(f"Failed to create MySQL database: {e}")
            return False
    
    def full_install(self, target_dir: str, config: Optional[Dict[str, str]] = None, 
                    plugins: Optional[List[str]] = None, themes: Optional[List[str]] = None) -> bool:
        """Perform a complete WordPress installation"""
        if config is None:
            config = self.default_config.copy()
        
        if plugins is None:
            plugins = ['classic-editor', 'yoast-seo']
        
        if themes is None:
            themes = ['twentytwentythree']
        
        print("Starting WordPress installation...")
        print(f"Target directory: {target_dir}")
        
        # Create target directory
        os.makedirs(target_dir, exist_ok=True)
        
        # Download WordPress
        if not self.download_wordpress(target_dir, self.wordpress_version):
            return False
        
        # Setup database
        if not self.setup_database(config):
            return False
        
        # Create wp-config.php
        if not self.create_wp_config(config, target_dir):
            return False
        
        # Install WordPress
        if not self.install_wordpress(config, target_dir):
            return False
        
        # Install plugins
        if plugins:
            if not self.install_plugins(plugins, target_dir):
                print("Plugin installation failed, but WordPress is installed")
        
        # Install themes
        if themes:
            if not self.install_themes(themes, target_dir):
                print("Theme installation failed, but WordPress is installed")
        
        print("\n🎉 WordPress installation completed successfully!")
        print(f"Site URL: {config['site_url']}")
        print(f"Admin URL: {config['site_url']}/wp-admin/")
        print(f"Admin Username: {config['admin_user']}")
        print(f"Admin Password: {config['admin_pass']}")
        
        return True

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='WordPress Installer Tool')
    parser.add_argument('target_dir', help='Target directory for WordPress installation')
    parser.add_argument('--version', default='latest', help='WordPress version to install')
    parser.add_argument('--site-url', default='http://localhost', help='Site URL')
    parser.add_argument('--site-title', default='My WordPress Site', help='Site title')
    parser.add_argument('--admin-user', default='admin', help='Admin username')
    parser.add_argument('--admin-pass', default='admin', help='Admin password')
    parser.add_argument('--admin-email', default='admin@example.com', help='Admin email')
    parser.add_argument('--db-host', default='localhost', help='Database host')
    parser.add_argument('--db-name', default='wordpress', help='Database name')
    parser.add_argument('--db-user', default='root', help='Database user')
    parser.add_argument('--db-pass', default='', help='Database password')
    parser.add_argument('--plugins', nargs='*', help='Plugins to install')
    parser.add_argument('--themes', nargs='*', help='Themes to install')
    
    args = parser.parse_args()
    
    installer = WordPressInstaller()
    installer.wordpress_version = args.version
    
    config = {
        'db_host': args.db_host,
        'db_name': args.db_name,
        'db_user': args.db_user,
        'db_pass': args.db_pass,
        'site_url': args.site_url,
        'admin_user': args.admin_user,
        'admin_pass': args.admin_pass,
        'admin_email': args.admin_email,
        'site_title': args.site_title
    }
    
    success = installer.full_install(
        target_dir=args.target_dir,
        config=config,
        plugins=args.plugins,
        themes=args.themes
    )
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
