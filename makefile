run:
	poetry run python main.py
install:
	poetry install
	pnpm i
remove:
	poetry env remove --all
schedule:
	ts-node schedule.ts