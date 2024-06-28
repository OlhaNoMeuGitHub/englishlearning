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


def save_results_to_csv(file_name: str, words_items_df: pd.DataFrame, unique_contents: int, unique_phrasalverbs: int, average_confidence: float, ):
    # Salvar o DataFrame principal
    words_items_df.to_csv(f'{file_name}_words_items.csv', index=False)
    
    # Salvar as métricas em um DataFrame separado
    metrics_df = pd.DataFrame({
        'Metric': ['Unique Contents', 'Unique Phrasal Verbs', 'Average Confidence'],
        'Value': [unique_contents, unique_phrasalverbs, average_confidence]
    })
    metrics_df.to_csv(f'{file_name}_metrics.csv', index=False)
    
    # Salvar os erros gramaticais em um DataFrame separado
    # grammar_errors_df = pd.DataFrame(grammar_errors)
    # grammar_errors_df.to_csv(f'{file_name}_grammar_errors.csv', index=False)
# Exemplo de uso
if __name__ == "__main__":
    try:
        data = read_csv_to_array('fillerwords.csv')
        print(data)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
