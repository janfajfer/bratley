solutions = "public/solutions/public_"
test = "public/instances/public_"

init:
	pip install -r requirements.txt

lint: main.py
	pylint main.py

run: main.py
	python3 main.py $(test)1.txt out

test:
	for i in 1 2 3 4 5; do python3 main.py $(test)$$i.txt out && cat out && echo "---" &&cat $(solutions)$$i.txt; echo ""; echo "------------------"; done




