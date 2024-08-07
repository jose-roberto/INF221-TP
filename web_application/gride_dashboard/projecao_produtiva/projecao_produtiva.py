import pandas as pd
from django.db import connection
from django.http import JsonResponse

def projecao_produtiva(request):
    # Extrair dados de produção
    query = """
    SELECT producao_energetica, consumo_energetico, valor_kwh, lucro, prejuizo, margem, tempo_de_operacao, tempo_de_parada
    FROM gride_dashboard_dados_desempenho WHERE usuario_id = 1 and data = '24/07/2002';
    """
    
    # Executar a consulta e obter os dados
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
    # Verificar se a consulta retornou resultados
    if not rows:
        print("Nenhum dado retornado do banco de dados.")
        data = {"error": "No data available"}
        return JsonResponse(data, safe=False)
    
    # Converter os dados para um DataFrame do Pandas
    columns = ['producao_energetica', 'consumo_energetico', 'valor_kwh', 'lucro', 'prejuizo', 'margem', 'tempo_de_operacao', 'tempo_de_parada']
    df = pd.DataFrame(rows, columns=columns)

    # Inspecionar os dados antes da conversão
    print("Dados antes da conversão:")
    print(df.head())

    # Verificar se o DataFrame está vazio após a conversão
    if df.empty:
        return JsonResponse({"error": "No data available after conversion"}, status=400)

    # Calcular estatísticas básicas
    stats = {
        'mean': df.mean().to_dict(),
        'median': df.median().to_dict(),
        'std': df.std().to_dict(),
        'min': df.min().to_dict(),
        'max': df.max().to_dict()
    }

    # Retornar os dados como JsonResponse
    return JsonResponse(stats, safe=False)