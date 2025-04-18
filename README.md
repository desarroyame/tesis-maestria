# Thesis LaTeX Project

Este repositorio contiene la estructura de un proyecto de tesis escrito en LaTeX, con herramientas de compilación automática utilizando Make.

## Estructura del Proyecto

```
.
├── LICENSE                # Licencia del proyecto
├── main.tex               # Documento principal de la tesis
├── paper.tex              # Documento de artículo académico
├── Makefile               # Archivo para automatizar la compilación
├── appendices/            # Apéndices de la tesis
│   ├── appendix_A.tex
│   └── appendix_B.tex
├── build/                 # Archivos temporales de compilación
├── chapters/              # Capítulos de la tesis
│   ├── chapter_1.tex
│   ├── chapter_2.tex
│   ├── chapter_3.tex
│   ├── chapter_4.tex
│   ├── chapter_5.tex
│   └── chapter_6.tex
├── core/                  # Elementos estructurales del documento
│   ├── abstract.tex
│   ├── dedication.tex
│   ├── ethics_statement.tex
│   ├── license.tex
│   └── titlepage.tex
├── docs/                  # Documentos compilados en PDF
│   ├── main.pdf
│   └── paper.pdf
├── draft/                 # Borradores y herramientas de trabajo
├── images/                # Imágenes y figuras utilizadas en el documento
└── references/            # Referencias bibliográficas
    ├── bibliography.bib
    └── videography.bib
```

## Requisitos

Para compilar este proyecto se necesitan las siguientes herramientas:

* Sistema TeX completo (TeXLive recomendado)
* pdflatex
* biber (para referencias bibliográficas)
* latexmk (opcional pero recomendado)

En sistemas basados en Debian/Ubuntu, puede instalarlos con:

```bash
sudo apt update
sudo apt install texlive-full biber latexmk
```

Para una instalación más ligera:

```bash
sudo apt update
sudo apt install texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-bibtex-extra biber latexmk
```

## Compilación del Proyecto

El proyecto utiliza Make para automatizar la compilación. Los archivos PDF resultantes se generan en el directorio `docs/`.

### Comandos disponibles

* `make all`: Compila tanto la tesis completa (main.pdf) como el artículo académico (paper.pdf)
* `make main`: Compila solo el documento principal de la tesis
* `make paper`: Compila solo el artículo académico
* `make clean`: Elimina archivos temporales de compilación pero conserva los PDF generados
* `make cleanall`: Elimina todos los archivos generados, incluyendo los PDF

### Ejemplos de uso

Compilación completa:
```bash
make
```

Compilación de solo la tesis:
```bash
make main
```

Limpieza de archivos temporales:
```bash
make clean
```

## Archivos de salida

Después de una compilación exitosa, encontrará:

* `docs/main.pdf`: Documento completo de tesis
* `docs/paper.pdf`: Artículo académico

## Notas

* Si `latexmk` no está disponible, el sistema utilizará automáticamente el método de compilación manual con pdflatex y biber.
* Para incluir imágenes con nombres que contengan espacios o caracteres especiales, use comillas: `\includegraphics[width=\textwidth]{"Nombre con espacios.png"}`