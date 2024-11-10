# LLAMMA CHAIN TRANSLATE

The work in this repo is largely based on the work done in the GEMBA Repository. Acknowledgements below.

Currently this application utilizes models hosted through Together.ai and their API.

This application attempts chain of thought techniques to improve on existing machine translations It first assigns and LLM as an evaluator to evaluate a set of existing source and hypothesis translation. It then assigns a separate LLM model as a translator, and uses the previous evaluation to output an improved translation.

Install required packages with python >= 3.8 

```
pip install -r requirements.txt
```

Set up secrets either for Together AI API: 

```
export TOGETHER_API_KEY=
```


It assumes two files with the same number of lines. It prints new lines to a file improved_translations.txt for each line pair:

Example usage utilizing LLama-3.2-3B as both the evaluator and translator models for Assamese Translations:
```
python main.py --source=source.txt --hypothesis=hypothesis.txt --source_lang=Assamese --target_lang=English  --eval_model="meta-llama/LLama-3.2-3B-Instruct-Turbo" --translate_model="meta-llama/LLama-3.2-3B-Instruct-Turbo"
```

## Acknowledgments

This project is an extension on the GEMBA work.

- **[GEMBA Repository](https://github.com/MicrosoftTranslator/GEMBA/)** 

Special thanks to the authors for their contributions and efforts.

If you use this repository, please consider citing their work:

### GEMBA-MQM 

    @inproceedings{kocmi-federmann-2023-gemba-mqm,
        title = {GEMBA-MQM: Detecting Translation Quality Error Spans with GPT-4},
        author = {Kocmi, Tom  and Federmann, Christian},
        booktitle = "Proceedings of the Eighth Conference on Machine Translation",
        month = dec,
        year = "2023",
        address = "Singapore",
        publisher = "Association for Computational Linguistics",
    }

### GEMBA-DA

    @inproceedings{kocmi-federmann-2023-large,
        title = "Large Language Models Are State-of-the-Art Evaluators of Translation Quality",
        author = "Kocmi, Tom and Federmann, Christian",
        booktitle = "Proceedings of the 24th Annual Conference of the European Association for Machine Translation",
        month = jun,
        year = "2023",
        address = "Tampere, Finland",
        publisher = "European Association for Machine Translation",
        url = "https://aclanthology.org/2023.eamt-1.19",
        pages = "193--203",
    }
