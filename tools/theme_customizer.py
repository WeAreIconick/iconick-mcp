#!/usr/bin/env python3
"""
WordPress Theme Customizer Tool
A comprehensive tool for managing WordPress themes and customizations
"""

import os
import sys
import subprocess
import json
import requests
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import argparse
from datetime import datetime

class ThemeCustomizer:
    """WordPress theme management and customization tool"""
    
    def __init__(self, wp_path: str = None):
        self.wp_path = wp_path or os.getcwd()
        self.wp_cli_path = None
        self.themes_dir = os.path.join(self.wp_path, 'wp-content', 'themes')
        self.customizer_cache = {}
        self.cache_file = os.path.join(self.wp_path, '.theme_cache.json')
        
        # Load customizer cache
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
        """Load customizer cache from file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self.customizer_cache = json.load(f)
        except Exception:
            self.customizer_cache = {}
    
    def save_cache(self):
        """Save customizer cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.customizer_cache, f, indent=2)
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
    
    def list_themes(self, status: str = 'all') -> List[Dict[str, Any]]:
        """List WordPress themes"""
        print(f"Listing {status} themes...")
        
        success, output, error = self.run_wp_cli(f"theme list --status={status} --format=json")
        
        if not success:
            print(f"Failed to list themes: {error}")
            return []
        
        try:
            themes = json.loads(output)
            return themes
        except json.JSONDecodeError:
            print("Failed to parse theme list")
            return []
    
    def get_current_theme(self) -> Optional[str]:
        """Get the currently active theme"""
        print("Getting current theme...")
        
        success, output, error = self.run_wp_cli("theme list --status=active --format=json")
        
        if not success:
            print(f"Failed to get current theme: {error}")
            return None
        
        try:
            themes = json.loads(output)
            if themes:
                return themes[0]['name']
            return None
        except json.JSONDecodeError:
            print("Failed to parse current theme")
            return None
    
    def activate_theme(self, theme_name: str) -> bool:
        """Activate a WordPress theme"""
        print(f"Activating theme: {theme_name}")
        
        success, output, error = self.run_wp_cli(f"theme activate {theme_name}")
        
        if success:
            print(f"Theme '{theme_name}' activated successfully!")
        else:
            print(f"Failed to activate theme '{theme_name}': {error}")
        
        return success
    
    def install_theme(self, theme_slug: str) -> bool:
        """Install a WordPress theme"""
        print(f"Installing theme: {theme_slug}")
        
        success, output, error = self.run_wp_cli(f"theme install {theme_slug}")
        
        if success:
            print(f"Theme '{theme_slug}' installed successfully!")
        else:
            print(f"Failed to install theme '{theme_slug}': {error}")
        
        return success
    
    def delete_theme(self, theme_name: str) -> bool:
        """Delete a WordPress theme"""
        print(f"Deleting theme: {theme_name}")
        
        success, output, error = self.run_wp_cli(f"theme delete {theme_name}")
        
        if success:
            print(f"Theme '{theme_name}' deleted successfully!")
        else:
            print(f"Failed to delete theme '{theme_name}': {error}")
        
        return success
    
    def update_theme(self, theme_name: str = None) -> bool:
        """Update a specific theme or all themes"""
        if theme_name:
            print(f"Updating theme: {theme_name}")
            command = f"theme update {theme_name}"
        else:
            print("Updating all themes...")
            command = "theme update --all"
        
        success, output, error = self.run_wp_cli(command)
        
        if success:
            if theme_name:
                print(f"Theme '{theme_name}' updated successfully!")
            else:
                print("All themes updated successfully!")
        else:
            print(f"Failed to update themes: {error}")
        
        return success
    
    def search_themes(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for themes in WordPress repository"""
        print(f"Searching themes for: {query}")
        
        success, output, error = self.run_wp_cli(f"theme search {query} --format=json --per-page={limit}")
        
        if not success:
            print(f"Failed to search themes: {error}")
            return []
        
        try:
            themes = json.loads(output)
            return themes
        except json.JSONDecodeError:
            print("Failed to parse search results")
            return []
    
    def create_child_theme(self, parent_theme: str, child_name: str, child_slug: str = None) -> bool:
        """Create a child theme"""
        if not child_slug:
            child_slug = child_name.lower().replace(' ', '-')
        
        print(f"Creating child theme '{child_name}' for parent '{parent_theme}'...")
        
        child_theme_dir = os.path.join(self.themes_dir, child_slug)
        
        # Check if child theme already exists
        if os.path.exists(child_theme_dir):
            print(f"Child theme directory already exists: {child_theme_dir}")
            return False
        
        try:
            # Create child theme directory
            os.makedirs(child_theme_dir, exist_ok=True)
            
            # Create style.css
            style_content = f"""/*
Theme Name: {child_name}
Template: {parent_theme}
Description: Child theme of {parent_theme}
Version: 1.0.0
*/

/* Import parent theme styles */
@import url("../{parent_theme}/style.css");

/* Add your custom styles below */
"""
            
            style_path = os.path.join(child_theme_dir, 'style.css')
            with open(style_path, 'w') as f:
                f.write(style_content)
            
            # Create functions.php
            functions_content = f"""<?php
/**
 * {child_name} functions and definitions
 *
 * @package {child_name}
 */

// Prevent direct access
if (!defined('ABSPATH')) {{
    exit;
}}

/**
 * Enqueue parent theme styles
 */
function {child_slug}_enqueue_styles() {{
    wp_enqueue_style('{parent_theme}-style', get_template_directory_uri() . '/style.css');
    wp_enqueue_style('{child_slug}-style', get_stylesheet_uri(), array('{parent_theme}-style'));
}}
add_action('wp_enqueue_scripts', '{child_slug}_enqueue_styles');

/**
 * Add your custom functions below
 */
"""
            
            functions_path = os.path.join(child_theme_dir, 'functions.php')
            with open(functions_path, 'w') as f:
                f.write(functions_content)
            
            # Create index.php if parent theme has one
            parent_index = os.path.join(self.themes_dir, parent_theme, 'index.php')
            if os.path.exists(parent_index):
                shutil.copy2(parent_index, os.path.join(child_theme_dir, 'index.php'))
            
            print(f"Child theme '{child_name}' created successfully!")
            print(f"Directory: {child_theme_dir}")
            
            return True
            
        except Exception as e:
            print(f"Failed to create child theme: {e}")
            return False
    
    def customize_theme_file(self, theme_name: str, file_path: str, content: str, backup: bool = True) -> bool:
        """Customize a theme file"""
        print(f"Customizing {file_path} in theme '{theme_name}'...")
        
        theme_dir = os.path.join(self.themes_dir, theme_name)
        full_file_path = os.path.join(theme_dir, file_path)
        
        if not os.path.exists(full_file_path):
            print(f"File not found: {full_file_path}")
            return False
        
        try:
            # Create backup if requested
            if backup:
                backup_path = f"{full_file_path}.backup.{int(datetime.now().timestamp())}"
                shutil.copy2(full_file_path, backup_path)
                print(f"Backup created: {backup_path}")
            
            # Write new content
            with open(full_file_path, 'w') as f:
                f.write(content)
            
            print(f"File '{file_path}' customized successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to customize file: {e}")
            return False
    
    def get_theme_customizations(self, theme_name: str) -> Dict[str, Any]:
        """Get theme customizations from customizer"""
        print(f"Getting customizations for theme '{theme_name}'...")
        
        success, output, error = self.run_wp_cli(f"theme get {theme_name} --format=json")
        
        if not success:
            print(f"Failed to get theme customizations: {error}")
            return {}
        
        try:
            customizations = json.loads(output)
            return customizations
        except json.JSONDecodeError:
            print("Failed to parse customizations")
            return {}
    
    def set_theme_mod(self, key: str, value: str) -> bool:
        """Set a theme modification"""
        print(f"Setting theme mod '{key}' to '{value}'...")
        
        success, output, error = self.run_wp_cli(f"theme mod set {key} '{value}'")
        
        if success:
            print(f"Theme mod '{key}' set successfully!")
        else:
            print(f"Failed to set theme mod '{key}': {error}")
        
        return success
    
    def get_theme_mod(self, key: str) -> Optional[str]:
        """Get a theme modification"""
        print(f"Getting theme mod '{key}'...")
        
        success, output, error = self.run_wp_cli(f"theme mod get {key}")
        
        if success:
            return output.strip()
        else:
            print(f"Failed to get theme mod '{key}': {error}")
            return None
    
    def list_theme_mods(self) -> Dict[str, str]:
        """List all theme modifications"""
        print("Listing theme modifications...")
        
        success, output, error = self.run_wp_cli("theme mod list --format=json")
        
        if not success:
            print(f"Failed to list theme mods: {error}")
            return {}
        
        try:
            mods = json.loads(output)
            return mods
        except json.JSONDecodeError:
            print("Failed to parse theme mods")
            return {}
    
    def install_from_zip(self, zip_path: str) -> bool:
        """Install a theme from a ZIP file"""
        print(f"Installing theme from ZIP: {zip_path}")
        
        if not os.path.exists(zip_path):
            print(f"ZIP file not found: {zip_path}")
            return False
        
        success, output, error = self.run_wp_cli(f"theme install {zip_path}")
        
        if success:
            print("Theme installed from ZIP successfully!")
        else:
            print(f"Failed to install theme from ZIP: {error}")
        
        return success
    
    def install_from_url(self, url: str) -> bool:
        """Install a theme from a URL"""
        print(f"Installing theme from URL: {url}")
        
        success, output, error = self.run_wp_cli(f"theme install {url}")
        
        if success:
            print("Theme installed from URL successfully!")
        else:
            print(f"Failed to install theme from URL: {error}")
        
        return success
    
    def export_theme_config(self, theme_name: str, output_file: str) -> bool:
        """Export theme configuration"""
        print(f"Exporting theme configuration for '{theme_name}'...")
        
        try:
            # Get theme info
            themes = self.list_themes('all')
            theme_info = next((t for t in themes if t['name'] == theme_name), None)
            
            if not theme_info:
                print(f"Theme '{theme_name}' not found")
                return False
            
            # Get theme mods
            theme_mods = self.list_theme_mods()
            
            # Get customizer settings
            customizations = self.get_theme_customizations(theme_name)
            
            config = {
                'theme_name': theme_name,
                'theme_info': theme_info,
                'theme_mods': theme_mods,
                'customizations': customizations,
                'exported_at': datetime.now().isoformat()
            }
            
            with open(output_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"Theme configuration exported to: {output_file}")
            return True
            
        except Exception as e:
            print(f"Failed to export theme configuration: {e}")
            return False
    
    def import_theme_config(self, config_file: str) -> bool:
        """Import theme configuration"""
        print(f"Importing theme configuration from: {config_file}")
        
        if not os.path.exists(config_file):
            print(f"Configuration file not found: {config_file}")
            return False
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Activate theme if specified
            if 'theme_name' in config:
                if not self.activate_theme(config['theme_name']):
                    print(f"Failed to activate theme: {config['theme_name']}")
                    return False
            
            # Apply theme mods
            if 'theme_mods' in config:
                for key, value in config['theme_mods'].items():
                    if not self.set_theme_mod(key, str(value)):
                        print(f"Failed to set theme mod: {key}")
            
            print("Theme configuration imported successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to import theme configuration: {e}")
            return False
    
    def create_custom_css(self, css_content: str, output_file: str = None) -> bool:
        """Create custom CSS file"""
        if not output_file:
            output_file = os.path.join(self.wp_path, 'wp-content', 'custom.css')
        
        print(f"Creating custom CSS file: {output_file}")
        
        try:
            with open(output_file, 'w') as f:
                f.write(css_content)
            
            print("Custom CSS file created successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to create custom CSS: {e}")
            return False
    
    def get_theme_health(self) -> Dict[str, Any]:
        """Get theme health information"""
        print("Checking theme health...")
        
        all_themes = self.list_themes('all')
        active_theme = self.get_current_theme()
        updates_available = []
        
        # Check for updates
        for theme in all_themes:
            if theme.get('update'):
                updates_available.append(theme)
        
        health_info = {
            'total_themes': len(all_themes),
            'active_theme': active_theme,
            'updates_available': len(updates_available),
            'themes_needing_update': [t['name'] for t in updates_available],
            'last_checked': datetime.now().isoformat()
        }
        
        return health_info

def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='WordPress Theme Customizer Tool')
    parser.add_argument('--wp-path', default='.', help='WordPress installation path')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List themes
    list_parser = subparsers.add_parser('list', help='List themes')
    list_parser.add_argument('--status', choices=['all', 'active', 'inactive'], 
                           default='all', help='Filter by status')
    
    # Search themes
    search_parser = subparsers.add_parser('search', help='Search themes')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=10, help='Number of results')
    
    # Install theme
    install_parser = subparsers.add_parser('install', help='Install theme')
    install_parser.add_argument('theme', help='Theme slug or ZIP file path')
    install_parser.add_argument('--from-url', help='Install from URL')
    
    # Activate theme
    activate_parser = subparsers.add_parser('activate', help='Activate theme')
    activate_parser.add_argument('theme', help='Theme name')
    
    # Delete theme
    delete_parser = subparsers.add_parser('delete', help='Delete theme')
    delete_parser.add_argument('theme', help='Theme name')
    
    # Update themes
    update_parser = subparsers.add_parser('update', help='Update themes')
    update_parser.add_argument('theme', nargs='?', help='Specific theme to update')
    
    # Create child theme
    child_parser = subparsers.add_parser('child', help='Create child theme')
    child_parser.add_argument('parent', help='Parent theme name')
    child_parser.add_argument('child_name', help='Child theme name')
    child_parser.add_argument('--slug', help='Child theme slug')
    
    # Theme mods
    mod_parser = subparsers.add_parser('mod', help='Manage theme mods')
    mod_subparsers = mod_parser.add_subparsers(dest='mod_action', help='Theme mod actions')
    
    mod_set_parser = mod_subparsers.add_parser('set', help='Set theme mod')
    mod_set_parser.add_argument('key', help='Mod key')
    mod_set_parser.add_argument('value', help='Mod value')
    
    mod_get_parser = mod_subparsers.add_parser('get', help='Get theme mod')
    mod_get_parser.add_argument('key', help='Mod key')
    
    mod_list_parser = mod_subparsers.add_parser('list', help='List theme mods')
    
    # Export/Import
    export_parser = subparsers.add_parser('export', help='Export theme config')
    export_parser.add_argument('theme', help='Theme name')
    export_parser.add_argument('output', help='Output file path')
    
    import_parser = subparsers.add_parser('import', help='Import theme config')
    import_parser.add_argument('config', help='Configuration file path')
    
    # Custom CSS
    css_parser = subparsers.add_parser('css', help='Create custom CSS')
    css_parser.add_argument('content', help='CSS content')
    css_parser.add_argument('--output', help='Output file path')
    
    # Health check
    health_parser = subparsers.add_parser('health', help='Check theme health')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    customizer = ThemeCustomizer(args.wp_path)
    
    if args.command == 'list':
        themes = customizer.list_themes(args.status)
        for theme in themes:
            print(f"{theme['name']} - {theme['status']} - {theme['version']}")
    
    elif args.command == 'search':
        themes = customizer.search_themes(args.query, args.limit)
        for theme in themes:
            print(f"{theme['name']} - {theme['version']} - {theme['description'][:100]}...")
    
    elif args.command == 'install':
        if args.from_url:
            success = customizer.install_from_url(args.from_url)
        elif args.theme.endswith('.zip'):
            success = customizer.install_from_zip(args.theme)
        else:
            success = customizer.install_theme(args.theme)
        
        sys.exit(0 if success else 1)
    
    elif args.command == 'activate':
        success = customizer.activate_theme(args.theme)
        sys.exit(0 if success else 1)
    
    elif args.command == 'delete':
        success = customizer.delete_theme(args.theme)
        sys.exit(0 if success else 1)
    
    elif args.command == 'update':
        success = customizer.update_theme(args.theme)
        sys.exit(0 if success else 1)
    
    elif args.command == 'child':
        success = customizer.create_child_theme(args.parent, args.child_name, args.slug)
        sys.exit(0 if success else 1)
    
    elif args.command == 'mod':
        if args.mod_action == 'set':
            success = customizer.set_theme_mod(args.key, args.value)
            sys.exit(0 if success else 1)
        elif args.mod_action == 'get':
            value = customizer.get_theme_mod(args.key)
            if value is not None:
                print(value)
                sys.exit(0)
            else:
                sys.exit(1)
        elif args.mod_action == 'list':
            mods = customizer.list_theme_mods()
            for key, value in mods.items():
                print(f"{key}: {value}")
    
    elif args.command == 'export':
        success = customizer.export_theme_config(args.theme, args.output)
        sys.exit(0 if success else 1)
    
    elif args.command == 'import':
        success = customizer.import_theme_config(args.config)
        sys.exit(0 if success else 1)
    
    elif args.command == 'css':
        success = customizer.create_custom_css(args.content, args.output)
        sys.exit(0 if success else 1)
    
    elif args.command == 'health':
        health = customizer.get_theme_health()
        print(json.dumps(health, indent=2))

if __name__ == '__main__':
    main()
