.PHONY: demo test eval

demo:
	PYTHONPATH=src python3 -m agentic_rag.demo

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

eval:
	PYTHONPATH=src python3 evals/run.py

