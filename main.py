from loadfile import load_words_transcription_from_file
from analysertext import analyze_transcription,items_to_dataframe,mark_items_to_discard,check_grammar_and_agreement_errors
from analyserPhrasalVerbs import analyze_phrasal_verbs,phrasal_verbs_analysis_to_dataframe,mark_phrasal_verbs_in_dataframe
from service import read_csv_to_array


# Exemplo de uso da função read_csv_to_array
try:
    # Caminho do arquivo JSON
    file_path = 'asrOutput(2).json'

    # Carregar o objeto WordsTranscription a partir do arquivo JSON
    words_transcription = load_words_transcription_from_file(file_path)
    # Analisar a transcrição e adicionar a classificação gramatical
    analyzed_transcription = analyze_transcription(words_transcription)

    # Exibir o objeto para verificar se está correto
    #print(analyzed_transcription.results.items[0])

    # Analisar a transcrição para encontrar phrasal verbs
    phrasal_verbs_analysis = analyze_phrasal_verbs(analyzed_transcription.results.transcripts)

    # Converter análise de phrasal verbs para DataFrame
    phrasal_verbs_df = phrasal_verbs_analysis_to_dataframe(phrasal_verbs_analysis)



    words_to_mark = read_csv_to_array('fillerwords.csv')
    analyzed_transcription = mark_items_to_discard(analyzed_transcription, words_to_mark)
    words_items_df = items_to_dataframe(analyzed_transcription )
    words_items_df = mark_phrasal_verbs_in_dataframe(phrasal_verbs_df, words_items_df)
    # Contar quantas strings diferentes existem no campo 'content' com 'discard' igual a False
    unique_contents = words_items_df[words_items_df['discard'] == False]['content'].nunique()
    # Contar quantas strings diferentes existem no campo 'content' com 'discard' igual a False e 'PhrasalVerb' igual a True
    unique_phrasalverbs = words_items_df[(words_items_df['discard'] == False) & (words_items_df['PhrasalVerb'] == True)]['content'].nunique()
    # Calcular a média de 'confidence' onde 'discard' é igual a False
    average_confidence = words_items_df[words_items_df['discard'] == False]['confidence'].mean()
      # Verificar erros gramaticais e de concordância
    grammar_errors = check_grammar_and_agreement_errors(words_transcription.results.transcripts)
    print(grammar_errors)
    print(words_items_df[words_items_df['PhrasalVerb'] == True])
    # print(words_items_df)
    print(unique_contents)
    print(unique_phrasalverbs)
    print(average_confidence)

    #mostre apenas onde o dataframe tem o campo PhrasalVerb igual a True

except Exception as e:
    print(f"Erro : {e}")


