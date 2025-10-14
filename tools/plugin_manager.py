#!/usr/bin/env python3
"""
WordPress Plugin Manager Tool
A comprehensive tool for managing WordPress plugins
"""

import os
import sys
import subprocess
import json
import requests
import zipfile
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import argparse
from datetime import datetime

class PluginManager:
    """WordPress plugin management tool"""
    
    def __init__(self, wp_path: str = None):
        self.wp_path = wp_path or os.getcwd()
        self.wp_cli_path = None
        self.plugin_cache = {}
        self.cache_file = os.path.join(self.wp_path, '.plugin_cache.json')
        
        # Load plugin cache
        self.load_cache()
    
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
    
    def load_cache(self):
        """Load plugin cache from file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self.plugin_cache = json.load(f)
        except Exception:
            self.plugin_cache = {}
    
    def save_cache(self):
        """Save plugin cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.plugin_cache, f, indent=2)
        except Exception as e:
            print(f"Failed to save cache: {e}")
    
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
    
    def list_plugins(self, status: str = 'all') -> List[Dict[str, Any]]:
        """List WordPress plugins"""
        print(f"Listing {status} plugins...")
        
        success, output, error = self.run_wp_cli(f"plugin list --status={status} --format=json")
        
        if not success:
            print(f"Failed to list plugins: {error}")
            return []
        
        try:
            plugins = json.loads(output)
            return plugins
        except json.JSONDecodeError:
            print("Failed to parse plugin list")
            return []
    
    def get_plugin_info(self, plugin_slug: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a plugin"""
        # Check cache first
        if plugin_slug in self.plugin_cache:
            cached_info = self.plugin_cache[plugin_slug]
            if datetime.now().timestamp() - cached_info['cached_at'] < 3600:  # 1 hour cache
                return cached_info['info']
        
        print(f"Getting plugin information for: {plugin_slug}")
        
        success, output, error = self.run_wp_cli(f"plugin get {plugin_slug} --format=json")
        
        if not success:
            print(f"Failed to get plugin info: {error}")
            return None
        
        try:
            plugin_info = json.loads(output)
            
            # Cache the information
            self.plugin_cache[plugin_slug] = {
                'info': plugin_info,
                'cached_at': datetime.now().timestamp()
            }
            self.save_cache()
            
            return plugin_info
        except json.JSONDecodeError:
            print("Failed to parse plugin information")
            return None
    
    def search_plugins(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for plugins in WordPress repository"""
        print(f"Searching plugins for: {query}")
        
        success, output, error = self.run_wp_cli(f"plugin search {query} --format=json --per-page={limit}")
        
        if not success:
            print(f"Failed to search plugins: {error}")
            return []
        
        try:
            plugins = json.loads(output)
            return plugins
        except json.JSONDecodeError:
            print("Failed to parse search results")
            return []
    
    def install_plugin(self, plugin_slug: str, activate: bool = False) -> bool:
        """Install a WordPress plugin"""
        print(f"Installing plugin: {plugin_slug}")
        
        command = f"plugin install {plugin_slug}"
        if activate:
            command += " --activate"
        
        success, output, error = self.run_wp_cli(command)
        
        if success:
            print(f"Plugin '{plugin_slug}' installed successfully!")
            if activate:
                print(f"Plugin '{plugin_slug}' activated!")
        else:
            print(f"Failed to install plugin '{plugin_slug}': {error}")
        
        return success
    
    def activate_plugin(self, plugin_slug: str) -> bool:
        """Activate a WordPress plugin"""
        print(f"Activating plugin: {plugin_slug}")
        
        success, output, error = self.run_wp_cli(f"plugin activate {plugin_slug}")
        
        if success:
            print(f"Plugin '{plugin_slug}' activated successfully!")
        else:
            print(f"Failed to activate plugin '{plugin_slug}': {error}")
        
        return success
    
    def deactivate_plugin(self, plugin_slug: str) -> bool:
        """Deactivate a WordPress plugin"""
        print(f"Deactivating plugin: {plugin_slug}")
        
        success, output, error = self.run_wp_cli(f"plugin deactivate {plugin_slug}")
        
        if success:
            print(f"Plugin '{plugin_slug}' deactivated successfully!")
        else:
            print(f"Failed to deactivate plugin '{plugin_slug}': {error}")
        
        return success
    
    def uninstall_plugin(self, plugin_slug: str) -> bool:
        """Uninstall a WordPress plugin"""
        print(f"Uninstalling plugin: {plugin_slug}")
        
        success, output, error = self.run_wp_cli(f"plugin uninstall {plugin_slug} --deactivate")
        
        if success:
            print(f"Plugin '{plugin_slug}' uninstalled successfully!")
        else:
            print(f"Failed to uninstall plugin '{plugin_slug}': {error}")
        
        return success
    
    def update_plugin(self, plugin_slug: str = None) -> bool:
        """Update a specific plugin or all plugins"""
        if plugin_slug:
            print(f"Updating plugin: {plugin_slug}")
            command = f"plugin update {plugin_slug}"
        else:
            print("Updating all plugins...")
            command = "plugin update --all"
        
        success, output, error = self.run_wp_cli(command)
        
        if success:
            if plugin_slug:
                print(f"Plugin '{plugin_slug}' updated successfully!")
            else:
                print("All plugins updated successfully!")
        else:
            print(f"Failed to update plugins: {error}")
        
        return success
    
    def install_from_zip(self, zip_path: str, activate: bool = False) -> bool:
        """Install a plugin from a ZIP file"""
        print(f"Installing plugin from ZIP: {zip_path}")
        
        if not os.path.exists(zip_path):
            print(f"ZIP file not found: {zip_path}")
            return False
        
        command = f"plugin install {zip_path} --activate" if activate else f"plugin install {zip_path}"
        
        success, output, error = self.run_wp_cli(command)
        
        if success:
            print(f"Plugin installed from ZIP successfully!")
            if activate:
                print("Plugin activated!")
        else:
            print(f"Failed to install plugin from ZIP: {error}")
        
        return success
    
    def install_from_url(self, url: str, activate: bool = False) -> bool:
        """Install a plugin from a URL"""
        print(f"Installing plugin from URL: {url}")
        
        command = f"plugin install {url} --activate" if activate else f"plugin install {url}"
        
        success, output, error = self.run_wp_cli(command)
        
        if success:
            print(f"Plugin installed from URL successfully!")
            if activate:
                print("Plugin activated!")
        else:
            print(f"Failed to install plugin from URL: {error}")
        
        return success
    
    def get_plugin_updates(self) -> List[Dict[str, Any]]:
        """Get list of plugins that need updates"""
        print("Checking for plugin updates...")
        
        success, output, error = self.run_wp_cli("plugin list --update=available --format=json")
        
        if not success:
            print(f"Failed to check for updates: {error}")
            return []
        
        try:
            updates = json.loads(output)
            return updates
        except json.JSONDecodeError:
            print("Failed to parse update information")
            return []
    
    def bulk_install_plugins(self, plugin_list: List[str], activate: bool = False) -> Dict[str, bool]:
        """Install multiple plugins at once"""
        print(f"Bulk installing {len(plugin_list)} plugins...")
        
        results = {}
        
        for plugin in plugin_list:
            results[plugin] = self.install_plugin(plugin, activate)
        
        successful = sum(1 for success in results.values() if success)
        print(f"Successfully installed {successful}/{len(plugin_list)} plugins")
        
        return results
    
    def bulk_activate_plugins(self, plugin_list: List[str]) -> Dict[str, bool]:
        """Activate multiple plugins at once"""
        print(f"Bulk activating {len(plugin_list)} plugins...")
        
        results = {}
        
        for plugin in plugin_list:
            results[plugin] = self.activate_plugin(plugin)
        
        successful = sum(1 for success in results.values() if success)
        print(f"Successfully activated {successful}/{len(plugin_list)} plugins")
        
        return results
    
    def bulk_deactivate_plugins(self, plugin_list: List[str]) -> Dict[str, bool]:
        """Deactivate multiple plugins at once"""
        print(f"Bulk deactivating {len(plugin_list)} plugins...")
        
        results = {}
        
        for plugin in plugin_list:
            results[plugin] = self.deactivate_plugin(plugin)
        
        successful = sum(1 for success in results.values() if success)
        print(f"Successfully deactivated {successful}/{len(plugin_list)} plugins")
        
        return results
    
    def export_plugin_list(self, output_file: str) -> bool:
        """Export list of installed plugins to a file"""
        print(f"Exporting plugin list to: {output_file}")
        
        plugins = self.list_plugins('active')
        
        if not plugins:
            print("No plugins found")
            return False
        
        try:
            with open(output_file, 'w') as f:
                json.dump(plugins, f, indent=2)
            
            print(f"Plugin list exported successfully to {output_file}")
            return True
            
        except Exception as e:
            print(f"Failed to export plugin list: {e}")
            return False
    
    def import_plugin_list(self, input_file: str, activate: bool = False) -> bool:
        """Import and install plugins from a file"""
        print(f"Importing plugin list from: {input_file}")
        
        if not os.path.exists(input_file):
            print(f"Input file not found: {input_file}")
            return False
        
        try:
            with open(input_file, 'r') as f:
                plugin_data = json.load(f)
            
            if isinstance(plugin_data, list):
                plugin_slugs = [plugin['name'] for plugin in plugin_data if 'name' in plugin]
            else:
                print("Invalid plugin list format")
                return False
            
            if not plugin_slugs:
                print("No plugins found in file")
                return False
            
            results = self.bulk_install_plugins(plugin_slugs, activate)
            successful = sum(1 for success in results.values() if success)
            
            print(f"Successfully imported {successful}/{len(plugin_slugs)} plugins")
            return successful > 0
            
        except Exception as e:
            print(f"Failed to import plugin list: {e}")
            return False
    
    def get_plugin_health(self) -> Dict[str, Any]:
        """Get plugin health information"""
        print("Checking plugin health...")
        
        all_plugins = self.list_plugins('all')
        active_plugins = [p for p in all_plugins if p.get('status') == 'active']
        inactive_plugins = [p for p in all_plugins if p.get('status') == 'inactive']
        updates_available = self.get_plugin_updates()
        
        health_info = {
            'total_plugins': len(all_plugins),
            'active_plugins': len(active_plugins),
            'inactive_plugins': len(inactive_plugins),
            'updates_available': len(updates_available),
            'last_checked': datetime.now().isoformat()
        }
        
        return health_info

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='WordPress Plugin Manager Tool')
    parser.add_argument('--wp-path', default='.', help='WordPress installation path')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List plugins
    list_parser = subparsers.add_parser('list', help='List plugins')
    list_parser.add_argument('--status', choices=['all', 'active', 'inactive'], 
                           default='all', help='Filter by status')
    
    # Search plugins
    search_parser = subparsers.add_parser('search', help='Search plugins')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=10, help='Number of results')
    
    # Install plugin
    install_parser = subparsers.add_parser('install', help='Install plugin')
    install_parser.add_argument('plugin', help='Plugin slug or ZIP file path')
    install_parser.add_argument('--activate', action='store_true', help='Activate after install')
    install_parser.add_argument('--from-url', help='Install from URL')
    
    # Activate plugin
    activate_parser = subparsers.add_parser('activate', help='Activate plugin')
    activate_parser.add_argument('plugin', help='Plugin slug')
    
    # Deactivate plugin
    deactivate_parser = subparsers.add_parser('deactivate', help='Deactivate plugin')
    deactivate_parser.add_argument('plugin', help='Plugin slug')
    
    # Uninstall plugin
    uninstall_parser = subparsers.add_parser('uninstall', help='Uninstall plugin')
    uninstall_parser.add_argument('plugin', help='Plugin slug')
    
    # Update plugins
    update_parser = subparsers.add_parser('update', help='Update plugins')
    update_parser.add_argument('plugin', nargs='?', help='Specific plugin to update')
    
    # Bulk operations
    bulk_parser = subparsers.add_parser('bulk', help='Bulk operations')
    bulk_parser.add_argument('action', choices=['install', 'activate', 'deactivate'], 
                           help='Bulk action')
    bulk_parser.add_argument('plugins', nargs='+', help='List of plugin slugs')
    bulk_parser.add_argument('--activate', action='store_true', help='Activate after install')
    
    # Import/Export
    export_parser = subparsers.add_parser('export', help='Export plugin list')
    export_parser.add_argument('output', help='Output file path')
    
    import_parser = subparsers.add_parser('import', help='Import plugin list')
    import_parser.add_argument('input', help='Input file path')
    import_parser.add_argument('--activate', action='store_true', help='Activate after install')
    
    # Health check
    health_parser = subparsers.add_parser('health', help='Check plugin health')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = PluginManager(args.wp_path)
    
    if args.command == 'list':
        plugins = manager.list_plugins(args.status)
        for plugin in plugins:
            print(f"{plugin['name']} - {plugin['status']} - {plugin['version']}")
    
    elif args.command == 'search':
        plugins = manager.search_plugins(args.query, args.limit)
        for plugin in plugins:
            print(f"{plugin['name']} - {plugin['version']} - {plugin['description'][:100]}...")
    
    elif args.command == 'install':
        if args.from_url:
            success = manager.install_from_url(args.from_url, args.activate)
        elif args.plugin.endswith('.zip'):
            success = manager.install_from_zip(args.plugin, args.activate)
        else:
            success = manager.install_plugin(args.plugin, args.activate)
        
        sys.exit(0 if success else 1)
    
    elif args.command == 'activate':
        success = manager.activate_plugin(args.plugin)
        sys.exit(0 if success else 1)
    
    elif args.command == 'deactivate':
        success = manager.deactivate_plugin(args.plugin)
        sys.exit(0 if success else 1)
    
    elif args.command == 'uninstall':
        success = manager.uninstall_plugin(args.plugin)
        sys.exit(0 if success else 1)
    
    elif args.command == 'update':
        success = manager.update_plugin(args.plugin)
        sys.exit(0 if success else 1)
    
    elif args.command == 'bulk':
        if args.action == 'install':
            results = manager.bulk_install_plugins(args.plugins, args.activate)
        elif args.action == 'activate':
            results = manager.bulk_activate_plugins(args.plugins)
        elif args.action == 'deactivate':
            results = manager.bulk_deactivate_plugins(args.plugins)
        
        failed = [plugin for plugin, success in results.items() if not success]
        if failed:
            print(f"Failed plugins: {', '.join(failed)}")
            sys.exit(1)
    
    elif args.command == 'export':
        success = manager.export_plugin_list(args.output)
        sys.exit(0 if success else 1)
    
    elif args.command == 'import':
        success = manager.import_plugin_list(args.input, args.activate)
        sys.exit(0 if success else 1)
    
    elif args.command == 'health':
        health = manager.get_plugin_health()
        print(json.dumps(health, indent=2))

if __name__ == '__main__':
    main()
