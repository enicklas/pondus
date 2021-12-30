echo "==== black ===="
poetry run black . --check

echo "==== isort ===="
poetry run isort  .

echo "==== flake8 ===="
poetry run flake8 pondus

echo "==== bandit ===="
poetry run bandit -q -r pondus
