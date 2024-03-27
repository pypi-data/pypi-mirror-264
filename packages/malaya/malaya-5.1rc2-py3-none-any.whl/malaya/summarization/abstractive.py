from malaya.supervised.huggingface import load
from malaya.torch_model.huggingface import Summarization

available_huggingface = {
    'mesolitica/finetune-summarization-t5-small-standard-bahasa-cased': {
        'Size (MB)': 242,
        'ROUGE-1': 0.75721802,
        'ROUGE-2': 0.496729027,
        'ROUGE-L': 0.304021823,
        'Suggested length': 1024,
    },
    'mesolitica/finetune-summarization-t5-base-standard-bahasa-cased': {
        'Size (MB)': 892,
        'ROUGE-1': 0.7132268255,
        'ROUGE-2': 0.470135011,
        'ROUGE-L': 0.366797009,
        'Suggested length': 1024,
    },
    'mesolitica/finetune-summarization-ms-t5-small-standard-bahasa-cased': {
        'Size (MB)': 242,
        'ROUGE-1': 0.742572468,
        'ROUGE-2': 0.50196339,
        'ROUGE-L': 0.3741226432,
        'Suggested length': 1024,
    },
    'mesolitica/finetune-summarization-ms-t5-base-standard-bahasa-cased': {
        'Size (MB)': 892,
        'ROUGE-1': 0.728116529,
        'ROUGE-2': 0.49656772621,
        'ROUGE-L': 0.376577199,
        'Suggested length': 1024,
    },
}

info = """
tested on translated validation set CNN Daily Mail, https://huggingface.co/datasets/mesolitica/translated-cnn-dailymail
tested on translated test set Xwikis, https://huggingface.co/datasets/mesolitica/translated-xwikis
""".strip()


def huggingface(
    model: str = 'mesolitica/finetune-summarization-t5-small-standard-bahasa-cased',
    force_check: bool = True,
    **kwargs,
):
    """
    Load HuggingFace model to abstractive summarization.

    Parameters
    ----------
    model: str, optional (default='mesolitica/finetune-summarization-t5-small-standard-bahasa-cased')
        Check available models at `malaya.summarization.abstractive.available_huggingface`.
    force_check: bool, optional (default=True)
        Force check model one of malaya model.
        Set to False if you have your own huggingface model.

    Returns
    -------
    result: malaya.torch_model.huggingface.Summarization
    """

    if model not in available_huggingface and force_check:
        raise ValueError(
            'model not supported, please check supported models from `malaya.summarization.abstractive.available_huggingface`.'
        )
    return load(
        model=model,
        class_model=Summarization,
        available_huggingface=available_huggingface,
        force_check=force_check,
        path=__name__,
        **kwargs,
    )
