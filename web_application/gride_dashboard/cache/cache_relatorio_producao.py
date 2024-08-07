from django.db import connection

def clean_expired_cache_relatorio_producao():
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM gride_dashboard_cache_relatorio_producao
            WHERE data < datetime('now', '-7 days');
        """)