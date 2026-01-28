import requests
from datetime import datetime, timedelta
import os

class GitHubService:
    """
    Servicio para obtener repositorios de GitHub.
    Usa caché para evitar saturar la API (60 requests/hora sin token).
    """
    
    # Variables de clase para cacheo
    _cached_repos = None
    _cache_time = None
    _cache_duration = timedelta(seconds=5)  # Cachea 5 segundos
    
    GITHUB_USERNAME = "NNorato123"  # Tu usuario de GitHub
    GITHUB_API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    
    @classmethod
    def get_repos(cls):
        """
        Obtiene los repositorios de GitHub con caché.
        
        Retorna:
            list: Lista de diccionarios con info de cada repo
        """
        # Si el caché está fresco, devolverlo
        if cls._cached_repos is not None and cls._cache_time is not None:
            if datetime.now() - cls._cache_time < cls._cache_duration:
                return cls._cached_repos
        
        # Si no, obtener de GitHub
        try:
            response = requests.get(
                cls.GITHUB_API_URL,
                params={
                    'sort': 'updated',  # Ordena por actualización (más recientes primero)
                    'per_page': 100,    # Obtiene hasta 100 repos
                    'type': 'owner'     # Solo repos que te pertenecen (no forks)
                },
                timeout=5
            )
            
            if response.status_code == 200:
                repos_data = response.json()
                
                # Formatear los repos
                formatted_repos = []
                for repo in repos_data:
                    formatted_repo = {
                        'id': repo['id'],
                        'name': repo['name'],
                        'description': repo['description'] or 'Sin descripción',
                        'url': repo['html_url'],
                        'language': repo['language'] or 'No especificado',
                        'stars': repo['stargazers_count'],
                        'updated_at': repo['updated_at'],
                        'image_url': None,  # GitHub no proporciona imagen
                        'github_url': repo['html_url'],
                        'featured': False,  # Podrías marcar algunos como destacados
                    }
                    formatted_repos.append(formatted_repo)
                
                # Guardar en caché
                cls._cached_repos = formatted_repos
                cls._cache_time = datetime.now()
                
                return formatted_repos
            else:
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Error conectando a GitHub API: {e}")
            # Si hay error, devolver caché anterior si existe
            return cls._cached_repos if cls._cached_repos else []
    
    @classmethod
    def clear_cache(cls):
        """Limpiar el caché manualmente (útil para desarrollo)"""
        cls._cached_repos = None
        cls._cache_time = None
