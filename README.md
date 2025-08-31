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

## Breves notas técnicas para LaTeX

- El proyecto usa `main.tex` como archivo de entrada principal; allí se incluyen todos los capítulos, apéndices y bibliografía.
- Es recomendable utilizar `latexmk` para compilar el proyecto de forma automática y gestionar referencias actualizadas.
- Para compilar:  
  ```bash
  latexmk -pdf main.tex
  ```
- Si realizas cambios en cualquier capítulo, apéndice, imagen o archivo de bibliografía, vuelve a ejecutar la instrucción anterior para generar el PDF actualizado.

---

**Autor:** Juan Carlos Arroyo Sosa  
**Maestría:** Diseño y Creación Interactiva  
**Universidad:** [Información institucional aquí]