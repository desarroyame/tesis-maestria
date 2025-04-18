# Makefile for LaTeX thesis compilation
# Output directory (consistent with .latexmkrc)
OUT_DIR = docs

# Main targets
all: main paper

main:
	latexmk -pdf main.tex

paper:
	latexmk -pdf paper.tex

# Manual compilation method (alternative to latexmk)
manual: 
	pdflatex -output-directory=$(OUT_DIR) main.tex
	biber $(OUT_DIR)/main
	pdflatex -output-directory=$(OUT_DIR) main.tex
	pdflatex -output-directory=$(OUT_DIR) main.tex

# Clean temporary LaTeX files
clean:
	rm -f $(OUT_DIR)/*.aux $(OUT_DIR)/*.log $(OUT_DIR)/*.bbl $(OUT_DIR)/*.blg \
		$(OUT_DIR)/*.out $(OUT_DIR)/*.toc $(OUT_DIR)/*.lof $(OUT_DIR)/*.lot \
		$(OUT_DIR)/*.fls $(OUT_DIR)/*.fdb_latexmk $(OUT_DIR)/*.run.xml \
		$(OUT_DIR)/*.bcf $(OUT_DIR)/*.synctex.gz $(OUT_DIR)/*.bbl-SAVE-ERROR

# Remove all files in the docs directory
cleanall:
	rm -rf $(OUT_DIR)/*

# Create output directory if it doesn't exist
$(OUT_DIR):
	mkdir -p $(OUT_DIR)

.PHONY: all main paper manual clean cleanall