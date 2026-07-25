.PHONY: demo test eval eval-live eval-live-canary eval-live-validate

TRIALS ?= 5
MAX_COST_USD ?= 25

demo:
	PYTHONPATH=src python3 -m agentic_rag.demo

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

eval:
	PYTHONPATH=src python3 evals/run.py

eval-live:
	PYTHONPATH=src python3 evals/live.py --provider "$(PROVIDER)" --model "$(MODEL)" --trials "$(TRIALS)" --max-cost-usd "$(MAX_COST_USD)"

eval-live-canary:
	PYTHONPATH=src python3 evals/live.py --provider "$(PROVIDER)" --model "$(MODEL)" --canary --max-cost-usd "$(MAX_COST_USD)"

eval-live-validate:
	PYTHONPATH=src python3 evals/live.py --validate-only
