import requests
import json
from typing import Optional, Dict, Any

class APIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None, auth_required: bool = True) -> Dict[str, Any]:
        """Make HTTP request to API"""
        url = f"{self.base_url}{endpoint}"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        if auth_required and self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=json.dumps(data) if data else None)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, data=json.dumps(data) if data else None)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                return {'error': 'Invalid HTTP method'}
            
            if response.status_code == 200 or response.status_code == 201:
                return response.json()
            else:
                try:
                    error_data = response.json()
                    return {'error': error_data.get('error', 'Request failed')}
                except:
                    return {'error': f'Request failed with status {response.status_code}'}
                    
        except requests.exceptions.ConnectionError:
            return {'error': 'Cannot connect to server. Make sure Django server is running.'}
        except Exception as e:
            return {'error': f'Request failed: {str(e)}'}
    
    def register(self, email: str, username: str, password: str) -> Dict[str, Any]:
        """Register new user"""
        data = {
            'email': email,
            'username': username,
            'password': password
        }
        
        result = self._make_request('POST', '/auth/register/', data, auth_required=False)
        
        if 'tokens' in result:
            self.access_token = result['tokens']['access']
            self.refresh_token = result['tokens']['refresh']
        
        return result
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login user"""
        data = {
            'email': email,
            'password': password
        }
        
        result = self._make_request('POST', '/auth/login/', data, auth_required=False)
        
        if 'tokens' in result:
            self.access_token = result['tokens']['access']
            self.refresh_token = result['tokens']['refresh']
        
        return result
    
    def get_passwords(self) -> Dict[str, Any]:
        """Get user's passwords"""
        return self._make_request('GET', '/passwords/')
    
    def create_password(self, site_name: str, username: str, password: str, site_url: str = '', notes: str = '') -> Dict[str, Any]:
        """Create new password entry"""
        data = {
            'site_name': site_name,
            'username': username,
            'password': password,
            'site_url': site_url,
            'notes': notes
        }
        
        return self._make_request('POST', '/passwords/', data)
    
    def update_password(self, password_id: int, site_name: str = None, username: str = None, 
                       password: str = None, site_url: str = None, notes: str = None) -> Dict[str, Any]:
        """Update password entry"""
        data = {}
        if site_name is not None:
            data['site_name'] = site_name
        if username is not None:
            data['username'] = username
        if password is not None:
            data['password'] = password
        if site_url is not None:
            data['site_url'] = site_url
        if notes is not None:
            data['notes'] = notes
        
        return self._make_request('PUT', f'/passwords/{password_id}/', data)
    
    def delete_password(self, password_id: int) -> Dict[str, Any]:
        """Delete password entry"""
        return self._make_request('DELETE', f'/passwords/{password_id}/')
    
    def logout(self):
        """Clear tokens"""
        self.access_token = None
        self.refresh_token = None