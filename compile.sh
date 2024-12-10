#!/bin/bash

# Compilar el documento LaTeX y generar el PDF en la carpeta ./build
pdflatex -output-directory=./docs main.tex
biber ./docs/main
pdflatex -output-directory=./docs main.tex
pdflatex -output-directory=./docs main.tex