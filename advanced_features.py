"""
Advanced Features for WordPress MCP Server
- Rate limiting and usage analytics
- Resource search functionality
- Resource versioning and update notifications
- Performance monitoring and metrics
"""

import time
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class UsageRecord:
    """Record of resource usage"""
    timestamp: str
    client_id: str
    resource_uri: str
    response_time: float
    success: bool
    error_message: Optional[str] = None

@dataclass
class RateLimitInfo:
    """Rate limiting information"""
    client_id: str
    requests_count: int
    window_start: float
    limit: int
    window_duration: int

class AdvancedRateLimiter:
    """Advanced rate limiting with multiple tiers and analytics"""
    
    def __init__(self):
        self.rate_limits = {
            'free': {'requests': 100, 'window': 3600},      # 100/hour
            'basic': {'requests': 500, 'window': 3600},     # 500/hour
            'premium': {'requests': 2000, 'window': 3600},  # 2000/hour
            'enterprise': {'requests': 10000, 'window': 3600} # 10000/hour
        }
        self.client_tiers = {}  # client_id -> tier
        self.request_history = defaultdict(lambda: deque(maxlen=1000))
        self.blocked_clients = set()
        self.suspicious_clients = set()
        
    def get_client_tier(self, client_id: str) -> str:
        """Get client tier (default to free)"""
        return self.client_tiers.get(client_id, 'free')
    
    def set_client_tier(self, client_id: str, tier: str):
        """Set client tier"""
        if tier in self.rate_limits:
            self.client_tiers[client_id] = tier
            logger.info(f"Client {client_id} tier set to {tier}")
    
    def check_rate_limit(self, client_id: str) -> tuple[bool, RateLimitInfo]:
        """Check if client is within rate limits"""
        if client_id in self.blocked_clients:
            return False, RateLimitInfo(client_id, 0, 0, 0, 0)
        
        tier = self.get_client_tier(client_id)
        limit_config = self.rate_limits[tier]
        
        current_time = time.time()
        window_start = current_time - limit_config['window']
        
        # Clean old requests
        client_requests = self.request_history[client_id]
        while client_requests and client_requests[0] < window_start:
            client_requests.popleft()
        
        # Check if within limit
        requests_count = len(client_requests)
        within_limit = requests_count < limit_config['requests']
        
        rate_info = RateLimitInfo(
            client_id=client_id,
            requests_count=requests_count,
            window_start=window_start,
            limit=limit_config['requests'],
            window_duration=limit_config['window']
        )
        
        if not within_limit:
            # Mark as suspicious if repeatedly hitting limits
            if requests_count > limit_config['requests'] * 1.5:
                self.suspicious_clients.add(client_id)
                logger.warning(f"Client {client_id} marked as suspicious")
        
        return within_limit, rate_info
    
    def record_request(self, client_id: str):
        """Record a request for rate limiting"""
        current_time = time.time()
        self.request_history[client_id].append(current_time)
    
    def block_client(self, client_id: str, reason: str):
        """Block a client"""
        self.blocked_clients.add(client_id)
        logger.warning(f"Client {client_id} blocked: {reason}")
    
    def unblock_client(self, client_id: str):
        """Unblock a client"""
        self.blocked_clients.discard(client_id)
        logger.info(f"Client {client_id} unblocked")

class UsageAnalytics:
    """Comprehensive usage analytics and monitoring"""
    
    def __init__(self):
        self.usage_records = deque(maxlen=10000)  # Keep last 10k records
        self.resource_stats = defaultdict(lambda: {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'avg_response_time': 0,
            'last_accessed': None,
            'popularity_score': 0
        })
        self.client_stats = defaultdict(lambda: {
            'total_requests': 0,
            'unique_resources': set(),
            'last_activity': None,
            'avg_response_time': 0,
            'error_rate': 0
        })
        self.hourly_stats = defaultdict(lambda: defaultdict(int))
        
    def record_usage(self, record: UsageRecord):
        """Record usage analytics"""
        self.usage_records.append(record)
        
        # Update resource stats
        resource_uri = record.resource_uri
        stats = self.resource_stats[resource_uri]
        stats['total_requests'] += 1
        stats['last_accessed'] = record.timestamp
        
        if record.success:
            stats['successful_requests'] += 1
        else:
            stats['failed_requests'] += 1
        
        # Update average response time
        total_successful = stats['successful_requests']
        if total_successful > 0:
            current_avg = stats['avg_response_time']
            stats['avg_response_time'] = (
                (current_avg * (total_successful - 1) + record.response_time) / total_successful
            )
        
        # Update client stats
        client_id = record.client_id
        client_stats = self.client_stats[client_id]
        client_stats['total_requests'] += 1
        client_stats['unique_resources'].add(resource_uri)
        client_stats['last_activity'] = record.timestamp
        
        # Update hourly stats
        hour_key = datetime.now().strftime('%Y-%m-%d-%H')
        self.hourly_stats[hour_key]['total_requests'] += 1
        self.hourly_stats[hour_key][f'resource_{resource_uri}'] += 1
        
    def get_popular_resources(self, limit: int = 10) -> List[Dict]:
        """Get most popular resources"""
        # Calculate popularity score (requests * recency factor)
        current_time = time.time()
        popular = []
        
        for resource_uri, stats in self.resource_stats.items():
            if stats['total_requests'] == 0:
                continue
                
            # Recency factor (more recent = higher score)
            last_accessed = stats['last_accessed']
            if last_accessed:
                last_time = datetime.fromisoformat(last_accessed).timestamp()
                hours_ago = (current_time - last_time) / 3600
                recency_factor = max(0.1, 1 - (hours_ago / 24))  # Decay over 24 hours
            else:
                recency_factor = 0.1
            
            popularity_score = stats['total_requests'] * recency_factor
            stats['popularity_score'] = popularity_score
            
            popular.append({
                'resource_uri': resource_uri,
                'total_requests': stats['total_requests'],
                'success_rate': stats['successful_requests'] / stats['total_requests'],
                'avg_response_time': stats['avg_response_time'],
                'popularity_score': popularity_score,
                'last_accessed': stats['last_accessed']
            })
        
        return sorted(popular, key=lambda x: x['popularity_score'], reverse=True)[:limit]
    
    def get_client_analytics(self, client_id: str) -> Dict:
        """Get analytics for a specific client"""
        if client_id not in self.client_stats:
            return {}
        
        stats = self.client_stats[client_id]
        return {
            'total_requests': stats['total_requests'],
            'unique_resources_accessed': len(stats['unique_resources']),
            'last_activity': stats['last_activity'],
            'avg_response_time': stats['avg_response_time'],
            'error_rate': stats['error_rate'],
            'resources_accessed': list(stats['unique_resources'])
        }
    
    def get_hourly_analytics(self, hours: int = 24) -> List[Dict]:
        """Get hourly analytics for the last N hours"""
        current_time = datetime.now()
        hourly_data = []
        
        for i in range(hours):
            hour_time = current_time - timedelta(hours=i)
            hour_key = hour_time.strftime('%Y-%m-%d-%H')
            
            data = {
                'hour': hour_key,
                'timestamp': hour_time.isoformat(),
                'total_requests': self.hourly_stats[hour_key]['total_requests']
            }
            
            # Add resource breakdown
            resource_requests = {}
            for key, value in self.hourly_stats[hour_key].items():
                if key.startswith('resource_'):
                    resource_uri = key.replace('resource_', '')
                    resource_requests[resource_uri] = value
            
            data['resource_breakdown'] = resource_requests
            hourly_data.append(data)
        
        return hourly_data

class ResourceSearchEngine:
    """Full-text search engine for WordPress resources"""
    
    def __init__(self):
        self.resource_index = {}
        self.search_index = defaultdict(list)  # term -> [resource_uris]
        self.tags_index = defaultdict(list)    # tag -> [resource_uris]
        self.categories_index = defaultdict(list)  # category -> [resource_uris]
        
    def index_resource(self, resource_uri: str, title: str, description: str, 
                      content: str, tags: List[str] = None, category: str = None):
        """Index a resource for search"""
        # Store resource metadata
        self.resource_index[resource_uri] = {
            'uri': resource_uri,
            'title': title,
            'description': description,
            'tags': tags or [],
            'category': category,
            'indexed_at': datetime.now().isoformat()
        }
        
        # Create search terms
        search_text = f"{title} {description} {content}".lower()
        terms = self._extract_terms(search_text)
        
        # Index terms
        for term in terms:
            if term not in self.search_index:
                self.search_index[term] = []
            if resource_uri not in self.search_index[term]:
                self.search_index[term].append(resource_uri)
        
        # Index tags
        if tags:
            for tag in tags:
                if resource_uri not in self.tags_index[tag]:
                    self.tags_index[tag].append(resource_uri)
        
        # Index category
        if category:
            if resource_uri not in self.categories_index[category]:
                self.categories_index[category].append(resource_uri)
    
    def _extract_terms(self, text: str) -> List[str]:
        """Extract searchable terms from text"""
        import re
        
        # Remove special characters and split into words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Remove common stop words
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'among', 'wordpress', 'php',
            'html', 'css', 'js', 'javascript', 'api', 'code', 'function'
        }
        
        return [word for word in words if word not in stop_words]
    
    def search(self, query: str, category: str = None, tags: List[str] = None, 
               limit: int = 20) -> List[Dict]:
        """Search for resources"""
        query_terms = self._extract_terms(query.lower())
        
        if not query_terms:
            return []
        
        # Find resources matching query terms
        matching_resources = set()
        for term in query_terms:
            if term in self.search_index:
                matching_resources.update(self.search_index[term])
        
        # Filter by category
        if category:
            category_resources = set(self.categories_index.get(category, []))
            matching_resources = matching_resources.intersection(category_resources)
        
        # Filter by tags
        if tags:
            for tag in tags:
                tag_resources = set(self.tags_index.get(tag, []))
                matching_resources = matching_resources.intersection(tag_resources)
        
        # Score and rank results
        scored_results = []
        for resource_uri in matching_resources:
            if resource_uri not in self.resource_index:
                continue
                
            resource_data = self.resource_index[resource_uri]
            score = self._calculate_relevance_score(resource_uri, query_terms)
            
            scored_results.append({
                'resource_uri': resource_uri,
                'title': resource_data['title'],
                'description': resource_data['description'],
                'category': resource_data['category'],
                'tags': resource_data['tags'],
                'relevance_score': score
            })
        
        # Sort by relevance score and return top results
        scored_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return scored_results[:limit]
    
    def _calculate_relevance_score(self, resource_uri: str, query_terms: List[str]) -> float:
        """Calculate relevance score for a resource"""
        score = 0.0
        
        for term in query_terms:
            # Term frequency in resource
            term_count = self.search_index.get(term, []).count(resource_uri)
            if term_count > 0:
                score += term_count
                
                # Boost score for title matches
                resource_data = self.resource_index.get(resource_uri, {})
                title = resource_data.get('title', '').lower()
                if term in title:
                    score += 2.0  # Title matches are more important
        
        return score
    
    def get_suggestions(self, partial_query: str, limit: int = 10) -> List[str]:
        """Get search suggestions based on partial query"""
        suggestions = set()
        partial_lower = partial_query.lower()
        
        # Find terms that start with the partial query
        for term in self.search_index.keys():
            if term.startswith(partial_lower) and len(term) > len(partial_lower):
                suggestions.add(term)
        
        # Also suggest resource titles
        for resource_data in self.resource_index.values():
            title_words = self._extract_terms(resource_data['title'])
            for word in title_words:
                if word.startswith(partial_lower):
                    suggestions.add(word)
        
        return sorted(list(suggestions))[:limit]

class ResourceVersioning:
    """Resource versioning and update notification system"""
    
    def __init__(self):
        self.resource_versions = {}
        self.update_log = deque(maxlen=1000)
        self.subscribers = defaultdict(set)  # resource_uri -> {client_ids}
        
    def get_resource_version(self, resource_uri: str) -> str:
        """Get current version of a resource"""
        if resource_uri not in self.resource_versions:
            # Generate initial version hash
            version_hash = self._generate_version_hash(resource_uri)
            self.resource_versions[resource_uri] = version_hash
        
        return self.resource_versions[resource_uri]
    
    def _generate_version_hash(self, resource_uri: str) -> str:
        """Generate version hash for resource"""
        # This would typically hash the actual content
        # For now, we'll use a timestamp-based hash
        timestamp = datetime.now().isoformat()
        content = f"{resource_uri}:{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def update_resource(self, resource_uri: str, content: str) -> str:
        """Update resource and return new version"""
        old_version = self.resource_versions.get(resource_uri)
        new_version = self._generate_version_hash(resource_uri)
        
        self.resource_versions[resource_uri] = new_version
        
        # Log the update
        update_record = {
            'timestamp': datetime.now().isoformat(),
            'resource_uri': resource_uri,
            'old_version': old_version,
            'new_version': new_version,
            'subscriber_count': len(self.subscribers[resource_uri])
        }
        
        self.update_log.append(update_record)
        
        # Notify subscribers (in a real implementation, this would send notifications)
        logger.info(f"Resource {resource_uri} updated from {old_version} to {new_version}")
        
        return new_version
    
    def subscribe_to_updates(self, client_id: str, resource_uri: str):
        """Subscribe client to resource updates"""
        self.subscribers[resource_uri].add(client_id)
        logger.info(f"Client {client_id} subscribed to {resource_uri} updates")
    
    def unsubscribe_from_updates(self, client_id: str, resource_uri: str):
        """Unsubscribe client from resource updates"""
        self.subscribers[resource_uri].discard(client_id)
        logger.info(f"Client {client_id} unsubscribed from {resource_uri} updates")
    
    def get_update_history(self, resource_uri: str = None, limit: int = 50) -> List[Dict]:
        """Get update history for resources"""
        if resource_uri:
            # Filter by specific resource
            filtered_updates = [
                update for update in self.update_log
                if update['resource_uri'] == resource_uri
            ]
        else:
            # All updates
            filtered_updates = list(self.update_log)
        
        return filtered_updates[-limit:]  # Return most recent updates
    
    def get_version_info(self, resource_uri: str) -> Dict:
        """Get detailed version information for a resource"""
        current_version = self.resource_versions.get(resource_uri)
        if not current_version:
            return {}
        
        # Get recent updates for this resource
        recent_updates = [
            update for update in self.update_log
            if update['resource_uri'] == resource_uri
        ][-5:]  # Last 5 updates
        
        return {
            'resource_uri': resource_uri,
            'current_version': current_version,
            'subscriber_count': len(self.subscribers[resource_uri]),
            'recent_updates': recent_updates,
            'total_updates': len(recent_updates)
        }

# Global instances
rate_limiter = AdvancedRateLimiter()
usage_analytics = UsageAnalytics()
search_engine = ResourceSearchEngine()
resource_versioning = ResourceVersioning()

def get_client_id(request) -> str:
    """Extract client ID from request"""
    # In a real implementation, this might use API keys, IP addresses, etc.
    # For now, we'll use a simple hash of the request
    client_info = f"{request.client.host}:{request.headers.get('user-agent', 'unknown')}"
    return hashlib.md5(client_info.encode()).hexdigest()[:16]

def record_request_analytics(client_id: str, resource_uri: str, 
                           response_time: float, success: bool, error_message: str = None):
    """Record request analytics"""
    record = UsageRecord(
        timestamp=datetime.now().isoformat(),
        client_id=client_id,
        resource_uri=resource_uri,
        response_time=response_time,
        success=success,
        error_message=error_message
    )
    usage_analytics.record_usage(record)

class AutoUpdateSystem:
    """Automatic resource update system with scheduling and notifications"""
    
    def __init__(self):
        self.update_schedules = {}  # resource_uri -> schedule_config
        self.update_sources = {}    # resource_uri -> source_config
        self.update_queue = deque()
        self.update_history = deque(maxlen=1000)
        self.is_running = False
        self.update_interval = 3600  # Check every hour
        
    def add_update_source(self, resource_uri: str, source_type: str, 
                         source_config: Dict[str, Any]):
        """Add an update source for a resource"""
        self.update_sources[resource_uri] = {
            'type': source_type,  # 'file', 'url', 'git', 'api'
            'config': source_config,
            'last_check': None,
            'last_update': None
        }
        logger.info(f"Added update source for {resource_uri}: {source_type}")
    
    def schedule_updates(self, resource_uri: str, schedule_config: Dict[str, Any]):
        """Schedule automatic updates for a resource"""
        self.update_schedules[resource_uri] = {
            'interval': schedule_config.get('interval', 3600),  # seconds
            'enabled': schedule_config.get('enabled', True),
            'next_update': time.time() + schedule_config.get('interval', 3600),
            'max_failures': schedule_config.get('max_failures', 3),
            'failure_count': 0
        }
        logger.info(f"Scheduled updates for {resource_uri}: every {schedule_config.get('interval', 3600)} seconds")
    
    def start_auto_updates(self):
        """Start the automatic update system"""
        if self.is_running:
            logger.warning("Auto-update system is already running")
            return
        
        self.is_running = True
        logger.info("Auto-update system started")
        
        # In a real implementation, this would run in a separate thread
        # For now, we'll simulate the functionality
        self._process_update_queue()
    
    def stop_auto_updates(self):
        """Stop the automatic update system"""
        self.is_running = False
        logger.info("Auto-update system stopped")
    
    def _process_update_queue(self):
        """Process the update queue"""
        current_time = time.time()
        
        for resource_uri, schedule in self.update_schedules.items():
            if not schedule['enabled']:
                continue
                
            if current_time >= schedule['next_update']:
                # Add to update queue
                self.update_queue.append({
                    'resource_uri': resource_uri,
                    'scheduled_time': current_time,
                    'retry_count': 0
                })
                
                # Schedule next update
                schedule['next_update'] = current_time + schedule['interval']
        
        # Process queued updates
        while self.update_queue:
            update_item = self.update_queue.popleft()
            self._execute_update(update_item)
    
    def _execute_update(self, update_item: Dict):
        """Execute a resource update"""
        resource_uri = update_item['resource_uri']
        retry_count = update_item['retry_count']
        
        try:
            # Check if resource needs updating
            needs_update = self._check_for_updates(resource_uri)
            
            if needs_update:
                # Perform the update
                update_result = self._perform_update(resource_uri)
                
                # Record the update
                update_record = {
                    'timestamp': datetime.now().isoformat(),
                    'resource_uri': resource_uri,
                    'success': update_result['success'],
                    'old_version': update_result.get('old_version'),
                    'new_version': update_result.get('new_version'),
                    'source_type': update_result.get('source_type'),
                    'changes_detected': update_result.get('changes_detected', False)
                }
                
                self.update_history.append(update_record)
                
                # Reset failure count on success
                if update_result['success']:
                    self.update_schedules[resource_uri]['failure_count'] = 0
                else:
                    self.update_schedules[resource_uri]['failure_count'] += 1
                    
                logger.info(f"Update executed for {resource_uri}: {update_result['success']}")
            else:
                logger.debug(f"No updates needed for {resource_uri}")
                
        except Exception as e:
            logger.error(f"Update failed for {resource_uri}: {str(e)}")
            
            # Handle retries
            max_retries = 3
            if retry_count < max_retries:
                update_item['retry_count'] += 1
                self.update_queue.append(update_item)  # Retry later
            else:
                self.update_schedules[resource_uri]['failure_count'] += 1
    
    def _check_for_updates(self, resource_uri: str) -> bool:
        """Check if a resource needs updating"""
        if resource_uri not in self.update_sources:
            return False
        
        source_info = self.update_sources[resource_uri]
        source_type = source_info['type']
        config = source_info['config']
        
        try:
            if source_type == 'file':
                return self._check_file_updates(resource_uri, config)
            elif source_type == 'url':
                return self._check_url_updates(resource_uri, config)
            elif source_type == 'git':
                return self._check_git_updates(resource_uri, config)
            elif source_type == 'api':
                return self._check_api_updates(resource_uri, config)
            else:
                logger.warning(f"Unknown source type: {source_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error checking updates for {resource_uri}: {str(e)}")
            return False
    
    def _check_file_updates(self, resource_uri: str, config: Dict) -> bool:
        """Check for file-based updates"""
        file_path = Path(config['path'])
        
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return False
        
        # Check file modification time
        file_mtime = file_path.stat().st_mtime
        last_check = self.update_sources[resource_uri].get('last_check')
        
        if last_check is None or file_mtime > last_check:
            self.update_sources[resource_uri]['last_check'] = time.time()
            return True
        
        return False
    
    def _check_url_updates(self, resource_uri: str, config: Dict) -> bool:
        """Check for URL-based updates"""
        import requests
        
        url = config['url']
        headers = config.get('headers', {})
        
        try:
            # Get last modified header or use ETag
            response = requests.head(url, headers=headers, timeout=30)
            
            last_modified = response.headers.get('last-modified')
            etag = response.headers.get('etag')
            
            source_info = self.update_sources[resource_uri]
            
            # Check if content has changed
            if last_modified:
                if source_info.get('last_modified') != last_modified:
                    source_info['last_modified'] = last_modified
                    return True
            
            if etag:
                if source_info.get('etag') != etag:
                    source_info['etag'] = etag
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking URL updates: {str(e)}")
            return False
    
    def _check_git_updates(self, resource_uri: str, config: Dict) -> bool:
        """Check for Git-based updates"""
        import subprocess
        
        repo_path = config['repo_path']
        branch = config.get('branch', 'main')
        
        try:
            # Check if there are new commits
            result = subprocess.run([
                'git', 'fetch', 'origin', branch
            ], cwd=repo_path, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Git fetch failed: {result.stderr}")
                return False
            
            # Check if local branch is behind
            result = subprocess.run([
                'git', 'rev-list', '--count', f'HEAD..origin/{branch}'
            ], cwd=repo_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                commits_behind = int(result.stdout.strip())
                return commits_behind > 0
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking Git updates: {str(e)}")
            return False
    
    def _check_api_updates(self, resource_uri: str, config: Dict) -> bool:
        """Check for API-based updates"""
        import requests
        
        api_url = config['api_url']
        headers = config.get('headers', {})
        params = config.get('params', {})
        
        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            # Check if response indicates updates are available
            data = response.json()
            
            # This is a generic check - specific APIs would need custom logic
            update_available = data.get('update_available', False)
            version = data.get('version')
            
            source_info = self.update_sources[resource_uri]
            last_version = source_info.get('last_version')
            
            if version and version != last_version:
                source_info['last_version'] = version
                return True
            
            return update_available
            
        except Exception as e:
            logger.error(f"Error checking API updates: {str(e)}")
            return False
    
    def _perform_update(self, resource_uri: str) -> Dict:
        """Perform the actual resource update"""
        source_info = self.update_sources[resource_uri]
        source_type = source_info['type']
        config = source_info['config']
        
        old_version = resource_versioning.get_resource_version(resource_uri)
        
        try:
            if source_type == 'file':
                success = self._update_from_file(resource_uri, config)
            elif source_type == 'url':
                success = self._update_from_url(resource_uri, config)
            elif source_type == 'git':
                success = self._update_from_git(resource_uri, config)
            elif source_type == 'api':
                success = self._update_from_api(resource_uri, config)
            else:
                success = False
            
            if success:
                new_version = resource_versioning.update_resource(resource_uri, "")
                source_info['last_update'] = time.time()
                
                return {
                    'success': True,
                    'old_version': old_version,
                    'new_version': new_version,
                    'source_type': source_type,
                    'changes_detected': True
                }
            else:
                return {
                    'success': False,
                    'source_type': source_type,
                    'changes_detected': False
                }
                
        except Exception as e:
            logger.error(f"Error performing update: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'source_type': source_type,
                'changes_detected': False
            }
    
    def _update_from_file(self, resource_uri: str, config: Dict) -> bool:
        """Update resource from file"""
        file_path = Path(config['path'])
        
        if not file_path.exists():
            return False
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the resource (this would integrate with your MCP server)
        # For now, we'll just log the update
        logger.info(f"Updated {resource_uri} from file {file_path}")
        return True
    
    def _update_from_url(self, resource_uri: str, config: Dict) -> bool:
        """Update resource from URL"""
        import requests
        
        url = config['url']
        headers = config.get('headers', {})
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            content = response.text
            
            # Update the resource
            logger.info(f"Updated {resource_uri} from URL {url}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating from URL: {str(e)}")
            return False
    
    def _update_from_git(self, resource_uri: str, config: Dict) -> bool:
        """Update resource from Git repository"""
        import subprocess
        
        repo_path = config['repo_path']
        branch = config.get('branch', 'main')
        
        try:
            # Pull latest changes
            result = subprocess.run([
                'git', 'pull', 'origin', branch
            ], cwd=repo_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Updated {resource_uri} from Git repository")
                return True
            else:
                logger.error(f"Git pull failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating from Git: {str(e)}")
            return False
    
    def _update_from_api(self, resource_uri: str, config: Dict) -> bool:
        """Update resource from API"""
        import requests
        
        api_url = config['api_url']
        headers = config.get('headers', {})
        params = config.get('params', {})
        
        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract content from API response
            content = data.get('content', '')
            
            # Update the resource
            logger.info(f"Updated {resource_uri} from API {api_url}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating from API: {str(e)}")
            return False
    
    def get_update_status(self, resource_uri: str = None) -> Dict:
        """Get update status for resources"""
        if resource_uri:
            # Status for specific resource
            schedule = self.update_schedules.get(resource_uri)
            source = self.update_sources.get(resource_uri)
            
            if not schedule and not source:
                return {}
            
            return {
                'resource_uri': resource_uri,
                'scheduled': bool(schedule),
                'enabled': schedule.get('enabled', False) if schedule else False,
                'next_update': schedule.get('next_update') if schedule else None,
                'failure_count': schedule.get('failure_count', 0) if schedule else 0,
                'has_source': bool(source),
                'source_type': source.get('type') if source else None,
                'last_check': source.get('last_check') if source else None,
                'last_update': source.get('last_update') if source else None
            }
        else:
            # Status for all resources
            return {
                'total_resources': len(self.update_schedules),
                'enabled_resources': sum(1 for s in self.update_schedules.values() if s.get('enabled', False)),
                'sources_configured': len(self.update_sources),
                'system_running': self.is_running,
                'pending_updates': len(self.update_queue),
                'recent_updates': len([u for u in self.update_history if u['success']])
            }
    
    def get_update_history(self, resource_uri: str = None, limit: int = 50) -> List[Dict]:
        """Get update history"""
        if resource_uri:
            filtered_updates = [
                update for update in self.update_history
                if update['resource_uri'] == resource_uri
            ]
        else:
            filtered_updates = list(self.update_history)
        
        return filtered_updates[-limit:]

# Global auto-update system instance
auto_update_system = AutoUpdateSystem()

# Example configuration for different update sources
def setup_example_update_sources():
    """Set up example update sources for WordPress resources"""
    
    # File-based updates for local resources
    auto_update_system.add_update_source(
        'wordpress://core/database',
        'file',
        {'path': 'resources/core/database.md'}
    )
    
    # URL-based updates for external resources
    auto_update_system.add_update_source(
        'wordpress://security/data-validation',
        'url',
        {
            'url': 'https://developer.wordpress.org/themes/basics/theme-functions/',
            'headers': {'User-Agent': 'WordPress-MCP-Server/2.0'}
        }
    )
    
    # Git-based updates for version-controlled resources
    auto_update_system.add_update_source(
        'wordpress://advanced/custom-post-types',
        'git',
        {
            'repo_path': '/path/to/wordpress-docs',
            'branch': 'main'
        }
    )
    
    # API-based updates for dynamic content
    auto_update_system.add_update_source(
        'wordpress://system/performance-stats',
        'api',
        {
            'api_url': 'https://api.wordpress.org/core/version-check/1.7/',
            'headers': {'Accept': 'application/json'}
        }
    )
    
    # Schedule updates for different resources
    auto_update_system.schedule_updates(
        'wordpress://core/database',
        {'interval': 3600, 'enabled': True}  # Every hour
    )
    
    auto_update_system.schedule_updates(
        'wordpress://security/data-validation',
        {'interval': 7200, 'enabled': True}  # Every 2 hours
    )
    
    auto_update_system.schedule_updates(
        'wordpress://advanced/custom-post-types',
        {'interval': 86400, 'enabled': True}  # Daily
    )
    
    auto_update_system.schedule_updates(
        'wordpress://system/performance-stats',
        {'interval': 300, 'enabled': True}  # Every 5 minutes
    )

# Initialize example sources
setup_example_update_sources()

