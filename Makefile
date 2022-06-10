clean:
	find . -name "*.ipynb" | xargs jupyter nbconvert --clear-output --inplace
