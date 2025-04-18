# Makefile for LaTeX thesis compilation
# Output directory (consistent with .latexmkrc)
OUT_DIR = docs

# Check if latexmk is available
LATEXMK := $(shell which latexmk 2>/dev/null)

# Main targets
all: main paper

main:
ifdef LATEXMK
	latexmk -pdf main.tex
else
	@echo "latexmk not found, using manual compilation method"
	$(MAKE) manual
endif

paper:
ifdef LATEXMK
	latexmk -pdf paper.tex
else
	@echo "latexmk not found, using manual compilation method for paper"
	pdflatex -output-directory=$(OUT_DIR) paper.tex
	biber $(OUT_DIR)/paper
	pdflatex -output-directory=$(OUT_DIR) paper.tex
	pdflatex -output-directory=$(OUT_DIR) paper.tex
endif

# Manual compilation method (alternative to latexmk)
manual: $(OUT_DIR)
	pdflatex -output-directory=$(OUT_DIR) main.tex
	biber $(OUT_DIR)/main
	pdflatex -output-directory=$(OUT_DIR) main.tex
	pdflatex -output-directory=$(OUT_DIR) main.tex

# Clean temporary LaTeX files
clean:
	rm -f $(OUT_DIR)/*.aux $(OUT_DIR)/*.log $(OUT_DIR)/*.bbl $(OUT_DIR)/*.blg \
		$(OUT_DIR)/*.out $(OUT_DIR)/*.toc $(OUT_DIR)/*.lof $(OUT_DIR)/*.lot \
		$(OUT_DIR)/*.fls $(OUT_DIR)/*.fdb_latexmk $(OUT_DIR)/*.run.xml \
		$(OUT_DIR)/*.bcf $(OUT_DIR)/*.synctex.gz $(OUT_DIR)/*.bbl-SAVE-ERROR \
		$(OUT_DIR)/._main.pdf

# Remove all files in the docs directory
cleanall:
	rm -rf $(OUT_DIR)/*
	find $(OUT_DIR) -type d -mindepth 1 -exec rm -rf {} +
	rm -f $(OUT_DIR)/._main.pdf

# Create output directory if it doesn't exist
$(OUT_DIR):
	mkdir -p $(OUT_DIR)

.PHONY: all main paper manual clean cleanall