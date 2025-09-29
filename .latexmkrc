# Nota: Re-activado out_dir para colocar artefactos en docs/
$out_dir = 'docs';

# Dejamos que latexmk detecte automáticamente que el backend es biber
# gracias a la línea \usepackage[backend=biber]{biblatex} en main.tex.
# (Eliminar el forzado previo evitó que biber se ejecutara fuera de orden.)

# Modo no interactivo y mejor reporte de líneas
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error';