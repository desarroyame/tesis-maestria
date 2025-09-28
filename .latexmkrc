# Nota: Re-activado out_dir para colocar artefactos en docs/
$out_dir = 'docs';

# Forzar uso de biber (biblatex backend)
$bibtex = 'biber';
$bibtex_use = 2;  # 2 = always run biber when bib files change

# Modo no interactivo y mejor reporte de líneas
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error';