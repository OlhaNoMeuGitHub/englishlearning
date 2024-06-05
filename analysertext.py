import nltk
from typing import List, Dict, Any
from loadfile import WordsTranscription, Transcript, Results, Item, Alternative

# Certifique-se de que os pacotes necessários estão baixados
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Função para classificar gramaticalmente as palavras de um texto
def classify_words(text: str) -> List[Dict[str, Any]]:
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    return pos_tags

# Função para processar cada transcrição
def process_transcript(transcript: Transcript) -> Transcript:
    classified_words = classify_words(transcript.transcript)
    gramaticalclass = [{'word': word, 'class': pos} for word, pos in classified_words]
    # Adicionando o campo gramaticalclass ao transcript
    return {
        "transcript": transcript.transcript,
        "gramaticalclass": gramaticalclass
    }

# Função para analisar o objeto WordsTranscription e adicionar a classificação gramatical
def analyze_transcription(words_transcription: WordsTranscription) -> WordsTranscription:
    new_transcripts = [process_transcript(transcript) for transcript in words_transcription.results.transcripts]
    new_results = Results(transcripts=new_transcripts, items=words_transcription.results.items)
    return WordsTranscription(
        jobName=words_transcription.jobName,
        accountId=words_transcription.accountId,
        status=words_transcription.status,
        results=new_results
    )

# Exemplo de uso
if __name__ == "__main__":
    from loadfile import load_words_transcription_from_file

    # Carregar o objeto WordsTranscription a partir do arquivo JSON
    file_path = '/mnt/data/asrOutput(2).json'
    words_transcription = load_words_transcription_from_file(file_path)

    # Analisar a transcrição e adicionar a classificação gramatical
    analyzed_transcription = analyze_transcription(words_transcription)

    # Exibir o objeto para verificar se está correto
    print(analyzed_transcription)
