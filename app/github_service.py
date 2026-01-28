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
    def get_repo_languages(cls, repo_url):
        """
        Obtiene todos los lenguajes de un repositorio y sus porcentajes.
        
        Retorna:
            dict: {language: percentage} o {}
        """
        try:
            # Construir URL para obtener idiomas
            languages_url = f"{repo_url}/languages"
            response = requests.get(languages_url, timeout=5)
            
            if response.status_code == 200:
                languages_data = response.json()
                
                if not languages_data:
                    return {}
                
                # Calcular total de bytes
                total_bytes = sum(languages_data.values())
                
                # Calcular porcentajes
                language_percentages = {}
                for lang, bytes_count in languages_data.items():
                    percentage = round((bytes_count / total_bytes) * 100, 1)
                    language_percentages[lang] = percentage
                
                return language_percentages
            else:
                return {}
                
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo lenguajes de {repo_url}: {e}")
            return {}
    
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
                    # Obtener todos los lenguajes del repositorio
                    languages = cls.get_repo_languages(repo['url'])
                    
                    # El lenguaje principal es el primero o "No especificado"
                    primary_language = repo['language'] or 'No especificado'
                    
                    # Obtener lista de todos los lenguajes
                    all_languages = list(languages.keys()) if languages else [primary_language]
                    
                    formatted_repo = {
                        'id': repo['id'],
                        'name': repo['name'],
                        'description': repo['description'] or 'Sin descripción',
                        'url': repo['html_url'],
                        'language': primary_language,
                        'languages': languages,  # Todos los lenguajes con porcentajes
                        'all_languages_list': all_languages,  # Lista de todos los lenguajes
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
