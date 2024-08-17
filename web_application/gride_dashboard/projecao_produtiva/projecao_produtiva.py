import pandas as pd
from django.db import connection
from django.http import JsonResponse

def projecao_produtiva(request, inicio, fim):
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
    #selecionar os dados que sejam dos mesmos meses do periodo especificado
    #ideia é observar a projecao produtiva de cada mes do periodo especificado
    #avaliar consumo e producao energetica, as suas medias, e influencias externas
    dados = [ ] #armazenar aq
    if dados.empty:
        return JsonResponse({"error": "No data avaliable for this period"})
    
    mes_i = inicio[3:5]
    mes_f = fim[3:5] 
    valor_kw = 0.70   
    info_meses = {}
    
    for i in range(mes_i, mes_f % 12 + 1):
        info_meses[i] = {
            'producao_energetica': dados['producao_energetica'].sum(),
            'media_producao': dados['producao_energetica'].mean(),
            'valor': dados['producao_energetica'].sum() * valor_kw
        }

    total_produzido = None
    for mes in info_meses:
        total_produzido += info_meses[mes]['producao_energetica']
        
    media_produtiva = total_produzido / len(info_meses)
    total_lucro = valor_kw * total_produzido
        
    #mostrar total produzido e o valor e a media

    # Retornar os dados como JsonResponse
    return JsonResponse(info_meses, safe=False)