#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# =====================================================================
# MONKEY-PATCHES PARA PYTHON 3.14 (Ejecutados antes de arrancar Django)
# =====================================================================
if 'test' in sys.argv:
    # 1. Evitar la comprobación estricta de versión de MariaDB/MySQL
    from django.db.backends.base.base import BaseDatabaseWrapper
    BaseDatabaseWrapper.check_database_version_supported = lambda self: None

    # 2. Corregir el fallo de super().__copy__() en Context para Python 3.14
    try:
        from django.template import context
        
        def safe_context_copy(self):
            # Creamos una instancia limpia de la clase sin invocar super().__copy__()
            duplicate = self.__class__.__new__(self.__class__)
            # Copiamos manualmente el stack de diccionarios del contexto de Django
            duplicate.dicts = self.dicts[:]
            return duplicate
            
        # Sobrescribimos el método defectuoso en memoria
        context.Context.__copy__ = safe_context_copy
    except Exception:
        pass
# =====================================================================

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LuxyFashion.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a variable environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()