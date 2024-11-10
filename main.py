import os
import sys
import ipdb
import pandas as pd
import diskcache as dc
from absl import app, flags
from lct.utils import get_evaluations, get_translations

flags.DEFINE_string('eval_model', None, 'Select Evaluation Model')
flags.DEFINE_string('translate_model', None, 'Select Translation Model')
flags.DEFINE_string('source', None, 'Filepath to the source file.')
flags.DEFINE_string('hypothesis', None, 'Filepath to the translation file.')
flags.DEFINE_string('source_lang', None, 'Source language name.')
flags.DEFINE_string('target_lang', None, 'Target language name.')


def main(argv):
    FLAGS = flags.FLAGS
    assert FLAGS.source is not None, "Source file must be provided."
    assert FLAGS.hypothesis is not None, "Hypothesis file must be provided."

    # check that source and hypothesis files exists
    if not os.path.isfile(FLAGS.source):
        print(f"Source file {FLAGS.source} does not exist.")
        sys.exit(1)
    if not os.path.isfile(FLAGS.hypothesis):
        print(f"Hypothesis file {FLAGS.hypothesis} does not exist.")
        sys.exit(1)

    assert FLAGS.source_lang is not None, "Source language name must be provided."
    assert FLAGS.target_lang is not None, "Target language name must be provided."

    # load both files and strip them
    with open(FLAGS.source, 'r') as f:
        source = f.readlines()
    source = [x.strip() for x in source]
    with open(FLAGS.hypothesis, 'r') as f:
        hypothesis = f.readlines()
    hypothesis = [x.strip() for x in hypothesis]

    assert len(source) == len(hypothesis), "Source and hypothesis files must have the same number of lines."

    evaluations = get_evaluations(source, hypothesis, FLAGS.source_lang, FLAGS.target_lang, FLAGS.eval_model)

    improved_translations = get_translations(evaluations, source, hypothesis, FLAGS.source_lang, FLAGS.target_lang, FLAGS.translate_model)

    file_path = "improved_translations.txt"

    # Check if the file exists
    if os.path.exists(file_path):
        # Ask the user what to do if the file exists
        action = input(f"The file {file_path} already exists. Do you want to (o)verwrite, (a)ppend, or (b)ackup it? ")

        if action == "o":
            # Overwrite the file
            mode = "w"
        elif action == "a":
            # Append to the file
            mode = "a"
        elif action == "b":
            # Backup the file and append
            import shutil
            shutil.copy(file_path, f"{file_path}.bak")
            print(f"Backup created as {file_path}.bak")
            mode = "w"
        else:
            print("Invalid option, defaulting to append.")
            mode = "a"
    else:
        # If the file doesn't exist, simply append
        mode = "a"

    # Append or overwrite based on the user's choice
    with open(file_path, mode) as file:
        for translation in improved_translations:
            file.write(translation + '\n')

if __name__ == "__main__":
    app.run(main)