import xml.etree.ElementTree as ET
import pandas as pd
import requests
from io import StringIO
import os

def download_kml(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.content.decode('utf-8')
    else:
        return None

def extract_kml_data(url_or_path: str):
    
    if url_or_path.startswith('https://') or url_or_path.startswith('http://'):
        response = requests.get(url_or_path)
        if response.status_code == 200:
            tree = ET.parse(StringIO(response.content.decode('utf-8')))
        else:
            raise ValueError(f'Erro na tentativa de baixar o arquivo através do link: {url_or_path}')

    elif os.path.exists(url_or_path):
        tree = ET.parse(url_or_path)

    else:
        raise ValueError(f'Entrada inválida! Não foi possível encontrar o arquivo kml: {url_or_path}')
    
    root = tree.getroot()
    namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
    placemarks = root.findall('.//kml:Placemark', namespaces)

    data_list = []

    for placemark in placemarks:
        data = {}

        for simple_data in placemark.findall('.//kml:SimpleData', namespaces):
            name = simple_data.get('name')
            if name:
                data[name] = simple_data.text

        data_list.append(data)

    return data_list

data_list = extract_kml_data('https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/localidades/cadastro_de_localidades_selecionadas_2010/Google_KML/BR_Localidades_2010_v1.kml')

df = pd.DataFrame(data_list)