import json
from typing import List, Dict, Any

# Definindo as classes para refletir o schema JSON
class Alternative:
    def __init__(self, confidence: str, content: str):
        self.confidence = confidence
        self.content = content

    def __repr__(self):
        return f'Alternative(confidence={self.confidence}, content={self.content})'

class Item:
    def __init__(self, type: str, alternatives: List[Alternative], start_time: str, end_time: str):
        self.type = type
        self.alternatives = alternatives
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f'Item(type={self.type}, alternatives={self.alternatives}, start_time={self.start_time}, end_time={self.end_time})'

class Transcript:
    def __init__(self, transcript: str):
        self.transcript = transcript

    def __repr__(self):
        return f'Transcript(transcript={self.transcript})'

class Results:
    def __init__(self, transcripts: List[Transcript], items: List[Item]):
        self.transcripts = transcripts
        self.items = items

    def __repr__(self):
        return f'Results(transcripts={self.transcripts}, items={self.items})'

class WordsTranscription:
    def __init__(self, jobName: str, accountId: str, status: str, results: Results):
        self.jobName = jobName
        self.accountId = accountId
        self.status = status
        self.results = results

    def __repr__(self):
        return f'WordsTranscription(jobName={self.jobName}, accountId={self.accountId}, status={self.status}, results={self.results})'

# Função para criar um objeto WordsTranscription a partir de um dicionário
def create_words_transcription(data: Dict[str, Any]) -> WordsTranscription:
    transcripts = [Transcript(**transcript) for transcript in data['results']['transcripts']]
    items = [Item(
        type=item['type'],
        alternatives=[Alternative(**alternative) for alternative in item['alternatives']],
        start_time=item.get('start_time', ''),
        end_time=item.get('end_time', '')
    ) for item in data['results']['items']]
    results = Results(transcripts=transcripts, items=items)
    return WordsTranscription(
        jobName=data['jobName'],
        accountId=data['accountId'],
        status=data['status'],
        results=results
    )

# Função para carregar o JSON de um arquivo e criar o objeto WordsTranscription
def load_words_transcription_from_file(file_path: str) -> WordsTranscription:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return create_words_transcription(data)