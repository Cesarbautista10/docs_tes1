#!/bin/bash

# Script de gestión del sistema de documentación LaTeX
# Facilita tareas comunes como compilación, limpieza y gestión de idiomas

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$SCRIPT_DIR/docs"
IMAGES_DIR="$SCRIPT_DIR/images"

# Funciones de utilidad
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para mostrar ayuda
show_help() {
    cat << EOF
Sistema de Generación de Documentación LaTeX

USAGE:
    $0 [COMMAND] [OPTIONS]

COMMANDS:
    build               Generar documentación para todos los idiomas
    build-lang LANG     Generar documentación para idioma específico
    clean              Limpiar archivos temporales
    clean-all          Limpiar todos los archivos generados
    setup              Configurar entorno inicial
    check              Verificar dependencias
    watch LANG         Monitorear cambios y regenerar automáticamente
    new-lang LANG      Crear estructura para nuevo idioma
    list-langs         Listar idiomas disponibles
    
OPTIONS:
    -h, --help         Mostrar esta ayuda
    -v, --verbose      Modo verbose
    
EXAMPLES:
    $0 build                    # Generar todos los idiomas
    $0 build-lang es           # Generar solo español
    $0 clean                   # Limpiar temporales
    $0 new-lang fr             # Crear estructura para francés
    $0 watch en                # Monitorear cambios en inglés

EOF
}

# Verificar dependencias
check_dependencies() {
    log_info "Verificando dependencias..."
    
    # Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 no encontrado"
        exit 1
    fi
    
    # LaTeX
    if ! command -v pdflatex &> /dev/null; then
        log_error "pdflatex no encontrado. Instalar texlive-full"
        exit 1
    fi
    
    # PyYAML
    if ! python3 -c "import yaml" 2>/dev/null; then
        log_warning "PyYAML no encontrado. Instalando..."
        pip3 install PyYAML
    fi
    
    log_success "Todas las dependencias están disponibles"
}

# Configurar entorno inicial
setup_environment() {
    log_info "Configurando entorno inicial..."
    
    # Crear directorios
    mkdir -p "$DOCS_DIR"
    mkdir -p "$IMAGES_DIR"
    
    # Hacer ejecutable el script de Python
    chmod +x "$SCRIPT_DIR/generate_docs.py"
    
    # Crear archivo .gitignore si no existe
    if [[ ! -f "$SCRIPT_DIR/.gitignore" ]]; then
        cat > "$SCRIPT_DIR/.gitignore" << EOF
# Archivos LaTeX temporales
*.aux
*.log
*.out
*.toc
*.lof
*.lot
*.synctex.gz

# Archivos de respaldo
*.bak
*~

# Directorios de build
build/
temp/

# Archivos del sistema
.DS_Store
Thumbs.db
EOF
        log_success "Archivo .gitignore creado"
    fi
    
    log_success "Entorno configurado correctamente"
}

# Generar documentación
build_docs() {
    local lang=$1
    
    log_info "Generando documentación..."
    
    if [[ -n "$lang" ]]; then
        log_info "Idioma específico: $lang"
        python3 "$SCRIPT_DIR/generate_docs.py" --lang "$lang"
    else
        log_info "Todos los idiomas"
        python3 "$SCRIPT_DIR/generate_docs.py"
    fi
    
    log_success "Documentación generada"
}

# Limpiar archivos
clean_files() {
    local clean_all=$1
    
    log_info "Limpiando archivos..."
    
    # Limpiar temporales de LaTeX
    find "$DOCS_DIR" -name "*.aux" -delete 2>/dev/null || true
    find "$DOCS_DIR" -name "*.log" -delete 2>/dev/null || true
    find "$DOCS_DIR" -name "*.out" -delete 2>/dev/null || true
    find "$DOCS_DIR" -name "*.toc" -delete 2>/dev/null || true
    find "$DOCS_DIR" -name "*.lof" -delete 2>/dev/null || true
    find "$DOCS_DIR" -name "*.lot" -delete 2>/dev/null || true
    find "$DOCS_DIR" -name "*.synctex.gz" -delete 2>/dev/null || true
    
    if [[ "$clean_all" == "true" ]]; then
        log_warning "Eliminando TODOS los archivos generados..."
        find "$DOCS_DIR" -name "*.tex" -delete 2>/dev/null || true
        find "$DOCS_DIR" -name "*.pdf" -delete 2>/dev/null || true
        find "$DOCS_DIR" -name "*_*.png" -delete 2>/dev/null || true
        find "$DOCS_DIR" -name "*_*.jpg" -delete 2>/dev/null || true
    fi
    
    log_success "Limpieza completada"
}

# Crear estructura para nuevo idioma
create_new_language() {
    local lang=$1
    
    if [[ -z "$lang" ]]; then
        log_error "Debe especificar código de idioma"
        exit 1
    fi
    
    local lang_dir="$SCRIPT_DIR/$lang"
    
    if [[ -d "$lang_dir" ]]; then
        log_error "El directorio para idioma '$lang' ya existe"
        exit 1
    fi
    
    log_info "Creando estructura para idioma: $lang"
    
    mkdir -p "$lang_dir"
    
    # Crear metadata.yaml
    cat > "$lang_dir/metadata.yaml" << EOF
title: "Document Title"
subtitle: "Document Subtitle"
author: "Author Name"
date: "$(date +%Y-%m-%d)"
version: "v1.0"
organization: "Your Organization"
toc: true
lof: true
lot: true
EOF
    
    # Crear content.md básico
    cat > "$lang_dir/content.md" << EOF
# Document Title

## Introduction

This is a sample document for language code: $lang

## Features

- Feature 1
- Feature 2
- Feature 3

## Specifications

| Parameter | Value | Unit |
|-----------|-------|------|
| Parameter 1 | Value 1 | Unit 1 |
| Parameter 2 | Value 2 | Unit 2 |

![Sample Image](images/sample.png)

## Conclusion

Document conclusion here.
EOF
    
    log_success "Estructura creada para idioma '$lang'"
    log_info "Edita los archivos en '$lang_dir/' y luego ejecuta:"
    log_info "  $0 build-lang $lang"
}

# Listar idiomas disponibles
list_languages() {
    log_info "Idiomas disponibles:"
    
    for dir in "$SCRIPT_DIR"/*/; do
        if [[ -f "$dir/content.md" && -f "$dir/metadata.yaml" ]]; then
            lang=$(basename "$dir")
            echo "  - $lang"
        fi
    done
}

# Monitorear cambios (requiere inotify-tools)
watch_changes() {
    local lang=$1
    
    if [[ -z "$lang" ]]; then
        log_error "Debe especificar idioma para monitorear"
        exit 1
    fi
    
    if ! command -v inotifywait &> /dev/null; then
        log_error "inotifywait no encontrado. Instalar inotify-tools"
        exit 1
    fi
    
    local watch_dir="$SCRIPT_DIR/$lang"
    
    if [[ ! -d "$watch_dir" ]]; then
        log_error "Directorio de idioma '$lang' no existe"
        exit 1
    fi
    
    log_info "Monitoreando cambios en '$lang'..."
    log_info "Presiona Ctrl+C para detener"
    
    while inotifywait -e modify,create,delete -r "$watch_dir" "$IMAGES_DIR" 2>/dev/null; do
        log_info "Cambios detectados, regenerando..."
        sleep 1  # Evitar regeneraciones múltiples rápidas
        build_docs "$lang"
    done
}

# Procesamiento de argumentos
case "${1:-}" in
    "build")
        check_dependencies
        build_docs
        ;;
    "build-lang")
        if [[ -z "${2:-}" ]]; then
            log_error "Debe especificar idioma"
            show_help
            exit 1
        fi
        check_dependencies
        build_docs "$2"
        ;;
    "clean")
        clean_files false
        ;;
    "clean-all")
        clean_files true
        ;;
    "setup")
        check_dependencies
        setup_environment
        ;;
    "check")
        check_dependencies
        ;;
    "watch")
        if [[ -z "${2:-}" ]]; then
            log_error "Debe especificar idioma"
            show_help
            exit 1
        fi
        check_dependencies
        watch_changes "$2"
        ;;
    "new-lang")
        if [[ -z "${2:-}" ]]; then
            log_error "Debe especificar código de idioma"
            show_help
            exit 1
        fi
        create_new_language "$2"
        ;;
    "list-langs")
        list_languages
        ;;
    "-h"|"--help"|"help")
        show_help
        ;;
    "")
        log_error "Debe especificar un comando"
        show_help
        exit 1
        ;;
    *)
        log_error "Comando desconocido: $1"
        show_help
        exit 1
        ;;
esac
