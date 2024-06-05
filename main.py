from loadfile import load_words_transcription_from_file
from analysertext import analyze_transcription


# Caminho do arquivo JSON
file_path = 'asrOutput(2).json'

# Carregar o objeto WordsTranscription a partir do arquivo JSON
words_transcription = load_words_transcription_from_file(file_path)
# Analisar a transcrição e adicionar a classificação gramatical
analyzed_transcription = analyze_transcription(words_transcription)

# Exibir o objeto para verificar se está correto
print(analyzed_transcription.results.items[0])
