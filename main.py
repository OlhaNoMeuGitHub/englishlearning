from loadfile import load_words_transcription_from_file
from analysertext import analyze_transcription,calculate_average_pronunciation,items_to_dataframe,mark_items_to_discard
from analyserPhrasalVerbs import analyze_phrasal_verbs,phrasal_verbs_analysis_to_dataframe
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
    analyzed_transcription = calculate_average_pronunciation(words_transcription)


    words_to_mark = read_csv_to_array('fillerwords.csv')
    analyzed_transcription = mark_items_to_discard(analyzed_transcription, words_to_mark)
    words_items_df = items_to_dataframe(analyzed_transcription )
    print(words_items_df)


except Exception as e:
    print(f"Erro : {e}")


print(analyzed_transcription.results.average_pronunciation)