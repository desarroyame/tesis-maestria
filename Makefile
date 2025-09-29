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

# Instala dependencias LaTeX mínimas en sistemas Debian/Ubuntu.
# Uso: make deps (requiere permisos de sudo si no es root)
deps:
	@if command -v apt-get >/dev/null 2>&1; then \
		 echo "Instalando paquetes LaTeX (esto puede tardar)..."; \
		 (which sudo >/dev/null 2>&1 && sudo apt-get update || apt-get update); \
		 (which sudo >/dev/null 2>&1 && sudo apt-get install -y --no-install-recommends texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-lang-spanish texlive-bibtex-extra biber latexmk || apt-get install -y --no-install-recommends texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended texlive-lang-spanish texlive-bibtex-extra biber latexmk); \
		 echo "Dependencias instaladas."; \
	else \
		 echo "apt-get no disponible. Instala manualmente TeX Live y biber."; \
	fi

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