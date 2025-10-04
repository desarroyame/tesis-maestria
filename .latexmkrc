# Configuración para colocar todos los archivos temporales en docs/
$out_dir = 'docs';
$aux_dir = 'docs';

# Dejamos que latexmk detecte automáticamente que el backend es biber
# gracias a la línea \usepackage[backend=biber]{biblatex} en main.tex.

# Modo no interactivo y mejor reporte de líneas
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error -output-directory=docs';
$biber = 'biber --output-directory=docs';

# Limpiar archivos en el directorio raíz también
$clean_ext = 'bbl fls fdb_latexmk synctex.gz nav snm vrb figlist makefile pygtex pythontex pyg figlist upa upb';

# Asegurar que se cree el directorio de salida si no existe
ensure_path('TEXINPUTS', './docs//');
ensure_path('TEXINPUTS', './/');

# Función para crear directorio si no existe
sub ensure_dir_exists {
    my $dir = shift;
    if (!-d $dir) {
        system("mkdir -p '$dir'");
    }
}

# Crear directorio docs si no existe
ensure_dir_exists('docs');