import pandas as pd
import os

def read_csv_to_array(file_name: str) -> list:
    # Caminho completo para o arquivo CSV na pasta assets
    file_path = os.path.join('assets', file_name)
    
    # Verifica se o arquivo existe
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"O arquivo {file_path} não foi encontrado.")
    
    # Lê o arquivo CSV
    df = pd.read_csv(file_path, header=None)
    
    # Converte o DataFrame em uma lista de strings
    data_array = df[0].astype(str).tolist()
    
    return data_array

# Exemplo de uso
if __name__ == "__main__":
    try:
        data = read_csv_to_array('fillerwords.csv')
        print(data)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
