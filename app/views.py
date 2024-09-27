from flask import Blueprint, render_template, request, jsonify
from .apis.apicaixa import get_api_data
from .apis.apiextra import get_api_data_extra
from .functions.caixa import process_data
from .functions.movextra import movextra_data
from .functions.entes import get_ufs_cidades
from .functions.periodo import get_anos_meses
import requests

main = Blueprint('main', __name__)

# Rota principal que renderiza a página com os totais
@main.route('/')
def index():
    # Inicialmente, os valores de total_sum e total_extra são zero
    total_sum = 0
    total_extra = 0
    ufs, cidades = get_ufs_cidades()
    anos, meses = get_anos_meses()  # Chama a função para obter anos e meses

    return render_template('index.html', 
                           total_sum=format_currency(total_sum), 
                           total_extra=format_currency(total_extra), 
                           ufs=ufs, 
                           cidades=cidades,
                           anos=anos,
                           meses=meses)

def format_currency(value):
    # Formata o valor para moeda brasileira
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Rota que recebe os parâmetros do formulário e chama as APIs
@main.route('/enviar_parans', methods=['POST'])
def enviar_parans():
    # Captura os parâmetros enviados pelo formulário
    id_ente = request.form['id_ente']
    an_referencia = request.form['an_referencia']
    me_referencia = request.form['me_referencia']

    # Obter os dados da API Caixa com os parâmetros
    data_caixa = get_api_data(id_ente, an_referencia, me_referencia)
    
    # Processar os dados Caixa
    resultado = process_data(data_caixa)

    # Obter os dados da API Extra com os parâmetros
    data_extra = get_api_data_extra(id_ente, an_referencia, me_referencia)
    
    # Processar os dados Extra
    resultadoextra = movextra_data(data_extra)

    # Obter novamente os dados de ufs, cidades, anos e meses para exibir no template
    ufs, cidades = get_ufs_cidades()
    anos, meses = get_anos_meses()  # Obtenha anos e meses novamente

    # Renderizar a página novamente com os novos valores
    return render_template('index.html', 
                           total_sum=format_currency(resultado), 
                           total_extra=format_currency(resultadoextra), 
                           ufs=ufs, 
                           cidades=cidades,
                           anos=anos,        # Passar anos para o template
                           meses=meses,      # Passar meses para o template
                           me_referencia='',  # Limpar o campo de mês
                           an_referencia='',  # Limpar o campo de exercício
                           id_ente='')       # Limpar o campo de id_ente

# Rota que retorna as cidades baseadas na UF
@main.route('/get_cidades/<uf>', methods=['GET'])
def get_cidades(uf):
    response = requests.get('https://apidatalake.tesouro.gov.br/ords/siconfi/tt/entes')
    data = response.json()['items']
    
    cidades = [item for item in data if item['uf'] == uf]
    return jsonify(cidades)
