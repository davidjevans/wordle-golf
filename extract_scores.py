"""
This file is tool to get our Wordle conversation transcripts into a python readable form.

Before reading this, there's a bit of domain knowledge about our family Wordle golf game that could be helpful:
    1. There are two transcript types: SMS and WhatsApp. For a while our family switched back and forth between sending our Wordle scores to an SMS chat and a WhatsApp chat. Since then, we have settled on WhatsApp, but we still have many scores recorded in our SMS chat. This doesn't actually have an effect on the code except for having the parse accept a list of paths, but still helpful to know!
    2. Our Wordle scores come in two formats: NYTimesWordle, WordleReplay. For the most part family members share their scores from the nytimes, but if someone misses a day, they sometimes use WordleReplay to catch up. These two sites share their scores in slighly different formats that need to be separately handled.
"""
import re
from pathlib import Path

import pandas as pd
from absl import app
from absl import flags


FLAGS = flags.FLAGS
flags.DEFINE_list('raw_data', None, 'A comma separated list of paths to the various WordleGolf chat transcripts.')
flags.mark_flag_as_required('raw_data')

flags.DEFINE_string('output', 'output.csv', 'The output file name of the csv file to save the results to.')



class WordleReader():
    """
    A parser class that can rip through transcripts of our Wordle chat and generate a Python interpretable list of Wordle scores.
    """
    wordle_normal_score_regex = re.compile(r'Wordle\s(?P<puzzle_number>\d+)\s(?P<score>\d|X)/\d')
    wordle_replay_score_regex = re.compile(r'Wordle:\s\#(?P<puzzle_number>\d+)')
    sender_regex = re.compile(r'(-|])\s(?P<name>\w+).*:')

    def __init__(self):
        self._last_sender = ""

    def update_last_sender(self, line):
        found_sender = self.sender_regex.search(line)
        if not found_sender:
            return False

        found_sender_name = found_sender.groupdict()["name"]
        if not found_sender_name:
            import pdb; pdb.set_trace()
        self._last_sender = found_sender_name.lower()
        return True


    def parse(self, file_path):
        found_wordle_scores = []
        with open(file_path) as f:
            for line in f:
                self.update_last_sender(line)

                if self.wordle_normal_score_regex.search(line):
                    extracted_wordle_score = self.wordle_normal_score_regex.search(line).groupdict()
                elif self.wordle_replay_score_regex.search(line):
                    extracted_wordle_score = self.wordle_replay_score_regex.search(line).groupdict()

                    next_line = f.readline()
                    extracted_wordle_score["score"] = re.search("(\d$)", next_line).group();
                else:
                    continue

                extracted_wordle_score["name"] = self._last_sender
                found_wordle_scores.append(extracted_wordle_score)

        return found_wordle_scores


def main(argv):
    total_scores = []
    for path in FLAGS.raw_data:
        wordle_reader = WordleReader()
        total_scores += wordle_reader.parse(path)

    scores_df = pd.DataFrame(total_scores)
    scores_df.to_csv(FLAGS.output, index=False)

if __name__ == '__main__':
  app.run(main)
