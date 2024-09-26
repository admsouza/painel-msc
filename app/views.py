from flask import Blueprint, render_template, request
from .apis.apicaixa import get_api_data
from .apis.apiextra import get_api_data_extra
from .functions.caixa import process_data
from .functions.movextra import movextra_data

main = Blueprint('main', __name__)

# Rota principal que renderiza a página com os totais
@main.route('/')
def index():
    # Inicialmente, os valores de total_sum e total_extra são zero
    total_sum = 0
    total_extra = 0

    return render_template('index.html', 
                           total_sum=format_currency(total_sum), 
                           total_extra=format_currency(total_extra)), 200

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

    # Renderizar a página novamente com os novos valores
    return render_template('index.html', 
                           total_sum=format_currency(resultado), 
                           total_extra=format_currency(resultadoextra)), 200
