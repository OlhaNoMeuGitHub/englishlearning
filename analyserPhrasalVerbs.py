import nltk
from typing import List, Dict, Any
import re
import pandas as pd


# Certifique-se de que os pacotes necessários estão baixados
nltk.download('wordnet')
nltk.download('omw-1.4')

# Função para obter phrasal verbs do wordnet
def get_phrasal_verbs_from_wordnet() -> List[str]:
    phrasal_verbs = set()
    for synset in list(nltk.corpus.wordnet.all_synsets('v')):
        for lemma in synset.lemmas():
            if '_' in lemma.name():  # Considera verbos compostos que têm um sublinhado
                phrasal_verbs.add(lemma.name().replace('_', ' '))
    return list(phrasal_verbs)

# Função para encontrar phrasal verbs em um texto
def find_phrasal_verbs(text: str, phrasal_verbs: List[str]) -> List[str]:
    found_phrasal_verbs = []
    for phrasal_verb in phrasal_verbs:
        if re.search(r'\b' + re.escape(phrasal_verb) + r'\b', text):
            found_phrasal_verbs.append(phrasal_verb)
    return found_phrasal_verbs

# Função para analisar a transcrição e retornar os phrasal verbs encontrados e a quantidade total
def analyze_phrasal_verbs(transcripts: List[Dict[str, Any]]) -> Dict[str, Any]:
    all_phrasal_verbs = get_phrasal_verbs_from_wordnet()
    found_phrasal_verbs = []
    for transcript in transcripts:
        text = transcript['transcript']
        phrasal_verbs_in_text = find_phrasal_verbs(text, all_phrasal_verbs)
        found_phrasal_verbs.extend(phrasal_verbs_in_text)
    
    phrasal_verbs_count = len(found_phrasal_verbs)
    unique_phrasal_verbs = list(set(found_phrasal_verbs))
    
    return {
        "phrasal_verbs": unique_phrasal_verbs,
        "total_count": phrasal_verbs_count
    }


def phrasal_verbs_analysis_to_dataframe(analysis: Dict[str, Any]) -> pd.DataFrame:
    df = pd.DataFrame({
        "Phrasal Verb": analysis["phrasal_verbs"],
        "Count": [1] * len(analysis["phrasal_verbs"])
    })
    df = df.groupby("Phrasal Verb").sum().reset_index()
    return df

def mark_phrasal_verbs_in_dataframe(phrasal_verbs_df: pd.DataFrame, items_df: pd.DataFrame) -> pd.DataFrame:
    # Adiciona a coluna 'PhrasalVerb' inicializada com False
    items_df['PhrasalVerb'] = False
    
    new_rows = []
    
    # Itera sobre cada phrasal verb
    for phrasal_verb in phrasal_verbs_df['Phrasal Verb']:
        words = phrasal_verb.split()
        if len(words) < 2:
            continue
        
        # Itera sobre o DataFrame para encontrar combinações de phrasal verbs
        for i in range(len(items_df) - 1):
            current_word = items_df.iloc[i]
            next_word = items_df.iloc[i + 1]
            
            # Verifica se as palavras concatenadas formam o phrasal verb
            if current_word['content'] == words[0] and next_word['content'] == words[1]:
                items_df.at[i, 'PhrasalVerb'] = True
                items_df.at[i + 1, 'PhrasalVerb'] = True
                
                # Concatenar as palavras e ajustar os campos
                combined_row = {
                    'type': 'verb',
                    'start_time': min(current_word['start_time'], next_word['start_time']),
                    'end_time': max(current_word['end_time'], next_word['end_time']),
                    'confidence': (current_word['confidence'] + next_word['confidence']) / 2,
                    'content': phrasal_verb,
                    'discard': current_word['discard'] or next_word['discard'],
                    'PhrasalVerb': True
                }
                
                # Adicionar a nova linha à lista de novas linhas
                new_rows.append(combined_row)
                
                # Marcar as linhas originais como descartadas
                items_df.at[i, 'discard'] = True
                items_df.at[i + 1, 'discard'] = True

    # Criar DataFrame das novas linhas e concatenar com o DataFrame original
    new_rows_df = pd.DataFrame(new_rows)
    items_df = pd.concat([items_df, new_rows_df], ignore_index=True)
    
    # Filtrar linhas onde 'discard' é False
    items_df = items_df[items_df['discard'] == False]
    
    return items_df


# Exemplo de uso
if __name__ == "__main__":
    from loadfile import load_words_transcription_from_file
    from analysertext import analyze_transcription

    # Carregar o objeto WordsTranscription a partir do arquivo JSON
    file_path = '/mnt/data/asrOutput(2).json'
    words_transcription = load_words_transcription_from_file(file_path)

    # Analisar a transcrição e adicionar a classificação gramatical
    analyzed_transcription = analyze_transcription(words_transcription)

    # Analisar a transcrição para encontrar phrasal verbs
    phrasal_verbs_analysis = analyze_phrasal_verbs(analyzed_transcription.results.transcripts)

    # Converter análise de phrasal verbs para DataFrame
    phrasal_verbs_df = phrasal_verbs_analysis_to_dataframe(phrasal_verbs_analysis)

    # Exibir os resultados
    print(phrasal_verbs_analysis)
