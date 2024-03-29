template_alpaca = {
    'description': 'Template used by Alpaca-LoRA.',
    'prompt_input': 'Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Input:\n{input}\n\n### Response:\n',
    'prompt_no_input': 'Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response:\n',
    'response_split': '### Response:',
}

template_malaya = {
    'description': 'Template used by Malaya.',
    'prompt_input': 'Di bawah ialah arahan yang menerangkan tugasan, termasuk dengan input yang menyediakan konteks lanjut. Tulis jawapan yang sesuai dengan arahan tersebut.\n\n### Arahan:\n{instruction}\n\n### Input:\n{input}\n\n### Jawapan:\n',
    'prompt_no_input': 'Di bawah ialah arahan yang menerangkan tugasan. Tulis jawapan yang sesuai dengan arahan tersebut.\n\n### Arahan:\n{instruction}\n\n### Jawapan:\n',
    'response_split': '### Jawapan:',
}


prompt = {
    'constituency': 'tukar ayat ini kepada constituency parsing: {sentence}',
    'generator': 'bina {{style}} dari: {sentence}',
    'abstractive-qa': 'paragraph `{paragraph}`, jawab soalan {sentence}',
    'extractive-qa': 'paragraph `{paragraph}`, ekstrak substring untuk soalan {sentence}',
    'similarity': 'ayat1: `{sentence1}`, ayat2: `{sentence2}`, ayat1 sama dengan ayat2',
    'summarization': 'ringkaskan ayat ini: {sentence}`',
    'text-to-kg': 'tukar teks ke grafik pengetahuan: {sentence}',
    'zeroshot-classification': 'kategorikan ayat ini dengan label {labels}: {sentence}',
    'zeroshot-ner': 'ekstrak entiti {entity} dari `{sentence}`',
    'dependency': 'tukar ayat ini kepada dependency parsing: {sentence}',
    'emotion-analysis': "kategorikan ayat ini dengan label ['anger', 'fear', 'happy', 'love', 'sadness', 'surprise']: {sentence}",
    'ner': 'kategorikan setiap perkataan dalam ayat ini dengan label []: {sentence}',
    'jawi-rumi': 'tukar jawi ke rumi: {sentence}',
    'kg-to-text': 'tukar grafik pengetahuan ke teks: {sentence}',
    'language-detection': "kategorikan ayat ini dengan label ['anger', 'fear', 'happy', 'love', 'sadness', 'surprise']: {sentence}",
    'nsfw': "kategorikan ayat ini dengan label ['anger', 'fear', 'happy', 'love', 'sadness', 'surprise']: {sentence}",
    'paraphrase': 'parafrasa ayat ini: {sentence}',
    'phoneme-dbp': 'tukar ayat ini ke phoneme DBP: {sentence}',
    'phoneme-ipa': 'tukar ayat ini ke phoneme IPA: {sentence}',
    'pos': 'kategorikan setiap perkataan dalam ayat ini dengan label []: {sentence}',
    'relevancy-analysis': "kategorikan ayat ini dengan label ['anger', 'fear', 'happy', 'love', 'sadness', 'surprise']: {sentence}",
    'rumi-jawi': 'tukar rumi ke jawi: {sentence}',
    'segmentation': 'segmentasi ayat ini: {sentence}',
    'sentiment-analysis': "kategorikan ayat ini dengan label ['anger', 'fear', 'happy', 'love', 'sadness', 'surprise'] dan terangkan: {sentence}",
    'stemming': 'puncakan ayat ini: {sentence}',
    'subjectivity-analysis': "kategorikan ayat ini dengan label ['anger', 'fear', 'happy', 'love', 'sadness', 'surprise']: {sentence}",
    'syllable': 'suku kata ayat ini: {sentence}',
    'tatabahasa': 'betulkan tatabahasa ayat ini: {sentence}',
    'translation': 'terjemah ke {to_lang}: {sentence}',
    'true-case': 'kes benar ayat ini: {sentence}',
}
