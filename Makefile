# Install the requirements locally
install:
	pip install -r requirements.txt

# Extract the wordle scores from the raw text transcripts
20220926_wordle_scores: extract_scores.py
	python extract_scores.py --raw_data data/20220926_dmddjl_sms_output.txt,data/20220926_whatsapp_export.txt --output wordle_scores

20230101_wordle_scores: extract_scores.py
	python extract_scores.py --raw_data data/20220926_dmddjl_sms_output.txt,data/20230101_whatsapp_export.txt --output wordle_scores

2022_wordle_summary: 20230101_wordle_scores
	jupyter nbconvert --to html --no-input wordle-golf-2022-summary.ipynb
