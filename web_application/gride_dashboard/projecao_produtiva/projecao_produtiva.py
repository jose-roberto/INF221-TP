class ProjecaoProdutiva:
    def __init__(self, _crescimento):
        self.crescimento = _crescimento
        self.meses = {
            '01': 'Janeiro',
            '02': 'Fevereiro',
            '03': 'Março',
            '04': 'Abril',
            '05': 'Maio',
            '06': 'Junho',
            '07': 'Julho',
            '08': 'Agosto',
            '09': 'Setembro',
            '10': 'Outubro',
            '11': 'Novembro',
            '12': 'Dezembro'
        }

    def projecao_produtiva(self, data):
        info_meses = {}

        for item in data:
            mes = item[0][3:5]

            if mes not in info_meses:
                info_meses[mes] = {
                    'total_producao_energetica': 0,
                    'total_consumo_energetico': 0,
                    'total_kw': 0,
                    'total_valor': 0
                }
                    
            value = (item[1] - item[2])
            info_meses[mes]['total_producao_energetica'] += item[1]
            info_meses[mes]['total_consumo_energetico'] += item[2]
            info_meses[mes]['total_kw'] += value
            info_meses[mes]['total_valor'] += item[3] * value
            
        projection = []
        for mes in info_meses:
            value = (info_meses[mes]['total_producao_energetica'] - info_meses[mes]['total_consumo_energetico']) * (1 + self.crescimento)
            projection.append([
                self.meses[mes], 
                round(info_meses[mes]['total_producao_energetica'] * (1 + self.crescimento), 2), 
                round(info_meses[mes]['total_consumo_energetico'] * (1 + self.crescimento), 2),
                round(info_meses[mes]['total_kw'] * (1 + self.crescimento), 2),
                round(info_meses[mes]['total_valor'] * (1 + self.crescimento), 2)
            ])

        return projection