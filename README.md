# Tesis de Maestría  
*Hospital San Juan de Dios y la imagen-síntoma*

## Estructura jerárquica del proyecto

```
tesis-maestria/
│
├── main.tex           # Archivo principal de compilación
├── paper.tex          # Artículo resumido
├── .latexmkrc         # Configuración para Latexmk
├── .gitignore
├── LICENSE
├── Makefile
├── README.md          # Este documento
│
├── core/              # Archivos fundamentales (portada, resumen, ética, licencia, dedicatoria)
│   ├── titlepage.tex
│   ├── abstract.tex
│   ├── dedication.tex
│   ├── ethics_statement.tex
│   └── license.tex
│
├── chapters/          # Capítulos principales de la tesis
│   ├── chapter_1.tex
│   ├── chapter_2.tex
│   ├── chapter_3.tex
│   ├── chapter_4.tex
│   ├── chapter_5.tex
│   └── chapter_6.tex
│
├── appendices/        # Material complementario
│   ├── appendix_A.tex
│   └── appendix_B.tex
│
├── images/            # Imágenes y recursos gráficos
│
├── references/        # Bibliografía y videografía
│   ├── bibliography.bib
│   └── videography.bib
│
├── build/             # Archivos generados en la compilación
├── docs/              # Documentación auxiliar (si aplica)
└── tools/             # Utilidades para el proyecto
```

---

## Capítulos y descripción breve

| Capítulo              | Descripción                                                                                                                                |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| **Capítulo 1**        | Introducción al fenómeno de la crisis del HSJD, dinámica social e institucional. Concepto de "imagen-síntoma".                            |
| **Capítulo 2**        | Desarrollo del marco teórico, fundamentos visuales y diálogo con autores clave; criterios para análisis de imágenes.                      |
| **Capítulo 3**        | Lógica y metodología de lectura de imágenes, método del montaje, interpretación visual y social.                                          |
| **Capítulo 4**        | Contexto social y visual del HSJD, entrevistas, corpus documental y artístico en la resistencia institucional.                            |
| **Capítulo 5**        | Metodología analítica: estructura dialógica y categorización de escenas, signos y símbolos. Ética y subjetividad en el análisis.          |
| **Capítulo 6**        | Conclusiones sobre el montaje, escenificación, anacronismos y aportes metodológicos para el análisis visual y sociocomunicativo.          |

## Compilación del Proyecto

El sistema utiliza Make para automatizar la compilación y gestión de archivos PDF en el directorio `docs/`. Las funciones disponibles y el funcionamiento son:

- **Compilar la tesis principal:**
  ```bash
  make main
  ```
- **Compilar el artículo académico:**
  ```bash
  make paper
  ```
- **Compilar ambos (tesis y artículo):**
  ```bash
  make all
  ```
- **Limpieza básica (archivos temporales):**
  ```bash
  make clean
  ```
- **Limpieza avanzada (todos los archivos generados):**
  ```bash
  make cleanall
  ```

Si `latexmk` está disponible en tu sistema, este se encargará automáticamente de la compilación y actualización de referencias. Si no, el Makefile usará el método manual con `pdflatex` y `biber` ¡no olvides revisar la carpeta `docs/` para tus PDF generados y finales!
