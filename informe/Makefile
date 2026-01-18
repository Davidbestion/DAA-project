# Makefile para compilar el informe LaTeX

# Nombre del archivo principal (sin extensión)
MAIN = report

# Compilador LaTeX
LATEX = pdflatex

# Opciones del compilador
LATEXOPTS = -interaction=nonstopmode -halt-on-error

# Archivos generados
PDF = $(MAIN).pdf
AUX = $(MAIN).aux
LOG = $(MAIN).log
OUT = $(MAIN).out
TOC = $(MAIN).toc
BBL = $(MAIN).bbl
BLG = $(MAIN).blg

# Target principal: generar el PDF
all: $(PDF)

# Compilar el documento (dos pasadas para referencias)
$(PDF): $(MAIN).tex
	@echo "Compilando documento LaTeX..."
	$(LATEX) $(LATEXOPTS) $(MAIN).tex
	@echo "Segunda pasada para referencias..."
	$(LATEX) $(LATEXOPTS) $(MAIN).tex
	@echo "Compilación completada: $(PDF)"

# Limpiar archivos auxiliares
clean:
	@echo "Limpiando archivos auxiliares..."
	rm -f $(AUX) $(LOG) $(OUT) $(TOC) $(BBL) $(BLG)
	rm -f *.aux *.log *.out *.toc *.bbl *.blg
	@echo "Limpieza completada."

# Limpiar todo incluyendo el PDF
cleanall: clean
	@echo "Eliminando PDF generado..."
	rm -f $(PDF)
	@echo "Limpieza total completada."

# Abrir el PDF generado
view: $(PDF)
	@echo "Abriendo PDF..."
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(PDF); \
	elif command -v evince > /dev/null; then \
		evince $(PDF); \
	elif command -v okular > /dev/null; then \
		okular $(PDF); \
	else \
		echo "No se encontró un visor de PDF. Abra manualmente $(PDF)"; \
	fi

# Recompilar desde cero
rebuild: cleanall all

# Ayuda
help:
	@echo "Targets disponibles:"
	@echo "  all       - Compila el documento (default)"
	@echo "  clean     - Elimina archivos auxiliares"
	@echo "  cleanall  - Elimina archivos auxiliares y PDF"
	@echo "  view      - Abre el PDF generado"
	@echo "  rebuild   - Limpia y recompila desde cero"
	@echo "  help      - Muestra esta ayuda"

.PHONY: all clean cleanall view rebuild help
