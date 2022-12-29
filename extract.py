import re
import pandas as pd
from pathlib import Path
whatsapp_file = Path("data/20220926_whatsapp_export.txt")
sms_file = Path("data/20220926_dmddjl_sms_output.txt")

"""
wordle_score_regex = re.compile(r'Wordle\s\#{0,1}(?P<puzzle_number>\d+)\s(?P<score>\d|X)/\d')
wordle_replay_regex = re.compile(r'Wordle:\s\#(?P<puzzle_number>\d+)')
test_string = "[5/1/22 10:12 AM] Doug Burgess: Wordle 316 4/6\n"
sender_regex = re.compile(r'(-|])\s(?P<name>\w+).*:')
found_sender = sender_regex.search(test_string)
print(found_sender.groupdict())
import pdb; pdb.set_trace()
"""

class WordleReader():
    wordle_normal_score_regex = re.compile(r'Wordle\s(?P<puzzle_number>\d+)\s(?P<score>\d|X)/\d')
    wordle_replay_score_regex = re.compile(r'Wordle:\s\#(?P<puzzle_number>\d+)')
    sender_regex = re.compile(r'(-|])\s(?P<name>\w+).*:')

    def __init__(self, file_path):
        self._file_path = file_path
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

    """
    def extract_wordle_score(self, line):
        found_wordle_score = self.wordle_normal_score_regex.search(line)
        if not found_wordle_score:
            found_wordle_replay_score = self.wordle_replay_score_regex.search(line)
            if found_wordle_replay_score:


            else:

            return False

        found_scores_dict = found_wordle_score.groupdict()
        found_scores_dict["name"] = self._last_sender
        return found_scores_dict
    """

    def extract_scores(self):
        found_wordle_scores = []
        with open(self._file_path) as f:
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

# wordle_reader = WordleReader(whatsapp_file)
sms_reader = WordleReader(sms_file)
whatsapp_reader = WordleReader(whatsapp_file)
whatsapp_scores = whatsapp_reader.extract_scores()
sms_scores = sms_reader.extract_scores()

total_scores = whatsapp_scores + sms_scores
scores_df = pd.DataFrame(total_scores)
scores_df.to_csv("wordle_scores.csv", index=False)
