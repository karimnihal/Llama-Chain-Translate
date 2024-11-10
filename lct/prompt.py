import re
from termcolor import colored
from collections import defaultdict

def apply_template(template, data):
    if isinstance(template, str):
        return template.format(**data)
    elif isinstance(template, list):
        prompt = []
        for conversation_turn in template:
            p = conversation_turn.copy()
            p['content'] = p['content'].format(**data)
            prompt.append(p)
        return prompt
    else:
        raise ValueError(f"Unknown template type {type(template)}")

def parse_translation(text):
    match = re.search(r'Improved Translation:(.*)', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return text #if it's not in the format return the whole thing


prompts = {
    "evaluations": {
        "prompt": 'Consider yourself to be a human evaluator who is well versed in the {source_lang} language and the {target_lang} language.\nEvaluate the given translation for adequacy and fluency and explain why those scores were given\n{source_lang} segment: {source_seg}\n{target_lang} translation: {target_seg}',
        "validate_answer": lambda x: x
    },
    "translations": {
        "prompt": 'Consider yourself to be a human translator who is well versed in the {source_lang} language and the {target_lang} language. An expert evaluator has previously given the following evaluation on this translation -\n{source_lang} segment: {source_seg}\n{target_lang} translation: {target_seg}\nEvaluation: {evaluation}\nBased on this evaluation give an improved translation. Output nothing but the improved translation.\nImproved Translation: ',
        "validate_answer": lambda x: parse_translation(x)
    }
}
