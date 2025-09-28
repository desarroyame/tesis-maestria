# Makefile for LaTeX thesis compilation
# Output directory (consistent with .latexmkrc)
OUT_DIR = docs

LATEXMK := $(shell which latexmk 2>/dev/null)

# Export TEXINPUTS so latexmk & pdflatex find local mapping .lbx
export TEXINPUTS := $(CURDIR)//:$(TEXINPUTS)

PDFLATEX_FLAGS = -interaction=nonstopmode -file-line-error
LATEXMK_FLAGS = -pdf -pdflatex='pdflatex $(PDFLATEX_FLAGS) %O %S'

all: main

main:
ifdef LATEXMK
	latexmk $(LATEXMK_FLAGS) main.tex
else
	@echo "latexmk not found, using manual compilation method"
	$(MAKE) manual
endif

paper:
ifdef LATEXMK
	latexmk $(LATEXMK_FLAGS) paper.tex
else
	@echo "latexmk not found, using manual compilation method for paper"
	pdflatex -output-directory=$(OUT_DIR) $(PDFLATEX_FLAGS) paper.tex || true
	biber $(OUT_DIR)/paper || true
	pdflatex -output-directory=$(OUT_DIR) $(PDFLATEX_FLAGS) paper.tex || true
	pdflatex -output-directory=$(OUT_DIR) $(PDFLATEX_FLAGS) paper.tex || true
endif

# Manual fallback (not usually needed)
manual: $(OUT_DIR)
	pdflatex -output-directory=$(OUT_DIR) $(PDFLATEX_FLAGS) main.tex || true
	biber $(OUT_DIR)/main || true
	pdflatex -output-directory=$(OUT_DIR) $(PDFLATEX_FLAGS) main.tex || true
	pdflatex -output-directory=$(OUT_DIR) $(PDFLATEX_FLAGS) main.tex || true

clean:
	latexmk -C main.tex || true
	latexmk -C paper.tex || true
	# Borrar residuos adicionales en OUT_DIR
	rm -f $(OUT_DIR)/*.run.xml $(OUT_DIR)/*.bcf $(OUT_DIR)/*.bbl-SAVE-ERROR

cleanall: clean
	rm -f $(OUT_DIR)/*.pdf

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

rebuild: clean main

.PHONY: all main paper manual clean cleanall rebuild