# Configuración para colocar todos los archivos temporales en docs/
$out_dir = 'docs';
$aux_dir = 'docs';

# Comandos: deja que latexmk inserte -outdir/-auxdir y demás opciones
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error %O %S';
$biber    = 'biber %O %B';

# Limpiar archivos extra
$clean_ext = 'bbl fls fdb_latexmk synctex.gz nav snm vrb figlist makefile pygtex pythontex pyg figlist upa upb';

# Crear directorio docs si no existe
sub ensure_dir_exists {
    my $dir = shift;
    if (!-d $dir) {
        system("mkdir -p '$dir'");
    }
}
ensure_dir_exists('docs');