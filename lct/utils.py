import ipdb
import pandas as pd
import diskcache as dc

from lct.together_api import TogetherApi
from lct.prompt import prompts, parse_translation, apply_template


def get_evaluations(source, hypothesis, source_lang, target_lang, model):
    df = pd.DataFrame({'source_seg': source, 'target_seg': hypothesis})
    df['source_lang'] = source_lang
    df['target_lang'] = target_lang

    cache = dc.Cache(f'cache/{model}_{"evaluations"}', expire=None, size_limit=int(10e10), cull_limit=0, eviction_policy='none')
    togetherapi = TogetherApi()

    df["prompt"] = df.apply(lambda x: apply_template(prompts["evaluations"]['prompt'], x), axis=1)
    parse_answer = prompts["evaluations"]["validate_answer"]
    answers = togetherapi.bulk_request(df, model, parse_answer, cache=cache, max_tokens=500)

    return list(pd.DataFrame(answers)['answer'])

def get_translations(evaluations, source, hypothesis, source_lang, target_lang, model):
    df = pd.DataFrame({'evaluation': evaluations,'source_seg': source, 'target_seg': hypothesis})
    df['source_lang'] = source_lang
    df['target_lang'] = target_lang

    cache = dc.Cache(f'cache/{model}_{"translations"}', expire=None, size_limit=int(10e10), cull_limit=0, eviction_policy='none')
    togetherapi = TogetherApi()

    df["prompt"] = df.apply(lambda x: apply_template(prompts["translations"]['prompt'], x), axis=1)
    parse_answer = prompts["translations"]["validate_answer"]
    answers = togetherapi.bulk_request(df, model, parse_answer, cache=cache, max_tokens=500)

    return list(pd.DataFrame(answers)['answer'])
