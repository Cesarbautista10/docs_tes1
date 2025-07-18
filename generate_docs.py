#!/usr/bin/env python3
"""
Generador automático de documentación LaTeX desde archivos README
Soporta múltiples idiomas, imágenes, tablas y control de saltos de página
"""

import os
import re
import yaml
import shutil
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

class LaTeXDocumentGenerator:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.docs_dir = self.base_dir / "docs"
        self.images_dir = self.base_dir / "images"
        self.template_file = self.base_dir / "template.tex"
        
        # Crear directorios si no existen
        self.docs_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        
    def find_language_dirs(self) -> List[str]:
        """Encuentra todos los directorios de idiomas con content.md"""
        lang_dirs = []
        for item in self.base_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                if (item / "content.md").exists() and (item / "metadata.yaml").exists():
                    lang_dirs.append(item.name)
        return sorted(lang_dirs)
    
    def load_metadata(self, lang_dir: str) -> Dict:
        """Carga metadatos desde metadata.yaml"""
        metadata_file = self.base_dir / lang_dir / "metadata.yaml"
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error cargando metadatos para {lang_dir}: {e}")
            return {}
    
    def process_markdown_content(self, content: str, lang_dir: str) -> str:
        """Procesa contenido markdown y lo convierte a LaTeX"""
        
        # Procesar headers ANTES de escapar caracteres especiales
        content = self.process_headers(content)
        
        # Procesar imágenes
        content = self.process_images(content, lang_dir)
        
        # Procesar tablas ANTES de escapar caracteres especiales
        content = self.process_tables(content)
        
        # Procesar listas
        content = self.process_lists(content)
        
        # Procesar texto en negrita e itálica
        content = self.process_text_formatting(content)
        
        # Procesar enlaces
        content = self.process_links(content)
        
        # Procesar código
        content = self.process_code_blocks(content)
        
        # FINALMENTE escapar caracteres especiales (excepto en código)
        content = self.escape_latex_chars(content)
        
        # Añadir control de saltos de página
        content = self.add_page_break_control(content)
        
        return content
    
    def escape_latex_chars(self, text: str) -> str:
        """Escapa caracteres especiales de LaTeX manteniendo comandos LaTeX válidos"""
        import re
        
        # Proteger comandos LaTeX existentes
        latex_commands = []
        
        # Encontrar y proteger comandos LaTeX como \section{}, \begin{}, etc.
        latex_pattern = r'\\[a-zA-Z]+(?:\[[^\]]*\])?(?:\{[^}]*\})*'
        for match in re.finditer(latex_pattern, text):
            placeholder = f"__LATEX_CMD_{len(latex_commands)}__"
            latex_commands.append(match.group(0))
            text = text.replace(match.group(0), placeholder, 1)
        
        # Proteger bloques de código ```
        code_blocks = []
        code_pattern = r'```[^`]*?```'
        for match in re.finditer(code_pattern, text, re.DOTALL):
            placeholder = f"__CODE_BLOCK_{len(code_blocks)}__"
            code_blocks.append(match.group(0))
            text = text.replace(match.group(0), placeholder, 1)
        
        # Proteger código inline `
        inline_code = []
        inline_pattern = r'`[^`]+`'
        for match in re.finditer(inline_pattern, text):
            placeholder = f"__INLINE_CODE_{len(inline_code)}__"
            inline_code.append(match.group(0))
            text = text.replace(match.group(0), placeholder, 1)
        
        # Ahora escapar caracteres especiales SOLO en texto normal
        replacements = {
            '{': r'\{',
            '}': r'\}',
            '$': r'\$',
            '&': r'\&',
            '%': r'\%',
            '#': r'\#',
            '^': r'\textasciicircum{}',
            '_': r'\_',
            '~': r'\textasciitilde{}',
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        # Restaurar comandos LaTeX
        for i, cmd in enumerate(latex_commands):
            placeholder = f"__LATEX_CMD_{i}__"
            text = text.replace(placeholder, cmd)
        
        # Restaurar bloques de código
        for i, code_block in enumerate(code_blocks):
            placeholder = f"__CODE_BLOCK_{i}__"
            text = text.replace(placeholder, code_block)
        
        for i, inline in enumerate(inline_code):
            placeholder = f"__INLINE_CODE_{i}__"
            text = text.replace(placeholder, inline)
        
        return text
    
    def process_headers(self, content: str) -> str:
        """Convierte headers markdown a secciones LaTeX"""
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            # Headers de nivel 1 (capítulos)
            if line.startswith('# '):
                title = line[2:].strip()
                processed_lines.append(f'\\section{{{title}}}')
                processed_lines.append('\\label{sec:' + title.lower().replace(' ', '-') + '}')
            # Headers de nivel 2 (secciones)
            elif line.startswith('## '):
                title = line[3:].strip()
                processed_lines.append(f'\\subsection{{{title}}}')
                processed_lines.append('\\label{subsec:' + title.lower().replace(' ', '-') + '}')
            # Headers de nivel 3 (subsecciones)
            elif line.startswith('### '):
                title = line[4:].strip()
                processed_lines.append(f'\\subsubsection{{{title}}}')
                processed_lines.append('\\label{subsubsec:' + title.lower().replace(' ', '-') + '}')
            # Headers de nivel 4 (párrafos)
            elif line.startswith('#### '):
                title = line[5:].strip()
                processed_lines.append(f'\\paragraph{{{title}}}')
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def process_images(self, content: str, lang_dir: str) -> str:
        """Procesa imágenes y las copia al directorio docs"""
        # Patrón para imágenes markdown: ![alt](path)
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        
        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Si la imagen está en el directorio raíz, copiarla a docs
            source_path = self.base_dir / image_path
            if source_path.exists():
                dest_filename = f"{lang_dir}_{source_path.name}"
                dest_path = self.docs_dir / dest_filename
                shutil.copy2(source_path, dest_path)
                
                # Generar código LaTeX para la imagen
                return f'''\\begin{{figure}}[htbp]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{dest_filename}}}
\\caption{{{alt_text}}}
\\label{{fig:{dest_filename.replace('.', '-')}}}
\\end{{figure}}'''
            else:
                return f"[Imagen no encontrada: {image_path}]"
        
        return re.sub(pattern, replace_image, content)
    
    def process_tables(self, content: str) -> str:
        """Convierte tablas markdown a formato LaTeX"""
        lines = content.split('\n')
        processed_lines = []
        in_table = False
        table_lines = []
        
        for line in lines:
            # Detectar inicio de tabla
            if '|' in line and not in_table:
                in_table = True
                table_lines = [line]
            elif '|' in line and in_table:
                table_lines.append(line)
            elif in_table and '|' not in line:
                # Fin de tabla
                processed_lines.append(self.convert_table_to_latex(table_lines))
                processed_lines.append(line)
                in_table = False
                table_lines = []
            else:
                processed_lines.append(line)
        
        # Si la tabla está al final del archivo
        if in_table:
            processed_lines.append(self.convert_table_to_latex(table_lines))
        
        return '\n'.join(processed_lines)
    
    def convert_table_to_latex(self, table_lines: List[str]) -> str:
        """Convierte una tabla markdown a LaTeX"""
        if len(table_lines) < 2:
            return '\n'.join(table_lines)
        
        # Procesar header
        header = table_lines[0].split('|')
        # Remover elementos vacíos y limpiar espacios
        header = [cell.strip() for cell in header if cell.strip()]
        
        # Procesar filas de datos (saltar la línea de separación)
        data_rows = []
        for line in table_lines[2:]:
            if '|' in line:
                row = line.split('|')
                row = [cell.strip() for cell in row if cell.strip()]
                if row:  # Solo añadir filas no vacías
                    data_rows.append(row)
        
        if not data_rows or not header:
            return '\n'.join(table_lines)
        
        # Determinar número de columnas basado en el header
        num_cols = len(header)
        col_spec = '|' + 'l|' * num_cols
        
        # Generar LaTeX
        latex_table = f'''\\begin{{table}}[htbp]
\\centering
\\begin{{tabular}}{{{col_spec}}}
\\hline
{' & '.join(header)} \\\\
\\hline
'''
        
        for row in data_rows:
            # Asegurarse de que la fila tenga el número correcto de columnas
            while len(row) < num_cols:
                row.append('')
            # Tomar solo las primeras num_cols columnas
            row = row[:num_cols]
            latex_table += ' & '.join(row) + ' \\\\\n'
        
        latex_table += '''\\hline
\\end{tabular}
\\caption{Tabla de datos}
\\end{table}

'''
        
        return latex_table
    
    def process_lists(self, content: str) -> str:
        """Procesa listas markdown a LaTeX"""
        lines = content.split('\n')
        processed_lines = []
        in_list = False
        list_type = None
        
        for line in lines:
            # Lista no ordenada
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                if not in_list:
                    processed_lines.append('\\begin{itemize}')
                    in_list = True
                    list_type = 'itemize'
                item = line.strip()[2:].strip()
                processed_lines.append(f'\\item {item}')
            # Lista ordenada
            elif re.match(r'^\s*\d+\.\s', line):
                if not in_list:
                    processed_lines.append('\\begin{enumerate}')
                    in_list = True
                    list_type = 'enumerate'
                item = re.sub(r'^\s*\d+\.\s*', '', line)
                processed_lines.append(f'\\item {item}')
            else:
                if in_list:
                    processed_lines.append(f'\\end{{{list_type}}}')
                    in_list = False
                    list_type = None
                processed_lines.append(line)
        
        # Si la lista está al final
        if in_list:
            processed_lines.append(f'\\end{{{list_type}}}')
        
        return '\n'.join(processed_lines)
    
    def process_text_formatting(self, content: str) -> str:
        """Procesa formato de texto (negrita, itálica)"""
        # Negrita
        content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
        content = re.sub(r'__(.*?)__', r'\\textbf{\1}', content)
        
        # Itálica
        content = re.sub(r'\*(.*?)\*', r'\\textit{\1}', content)
        content = re.sub(r'_(.*?)_', r'\\textit{\1}', content)
        
        return content
    
    def process_links(self, content: str) -> str:
        """Procesa enlaces markdown"""
        # Enlaces [texto](url)
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', content)
        return content
    
    def process_code_blocks(self, content: str) -> str:
        """Procesa bloques de código"""
        # Código inline
        content = re.sub(r'`([^`]+)`', r'\\texttt{\1}', content)
        
        # Bloques de código
        content = re.sub(
            r'```(\w+)?\n(.*?)\n```',
            r'\\begin{verbatim}\n\2\n\\end{verbatim}',
            content,
            flags=re.DOTALL
        )
        
        return content
    
    def add_page_break_control(self, content: str) -> str:
        """Añade control de saltos de página"""
        lines = content.split('\n')
        processed_lines = []
        
        for i, line in enumerate(lines):
            processed_lines.append(line)
            
            # Evitar salto de página después de títulos
            if line.startswith('\\section') or line.startswith('\\subsection'):
                processed_lines.append('\\nopagebreak[4]')
            
            # Añadir espacio flexible antes de nuevas secciones
            if i < len(lines) - 1 and lines[i+1].startswith('\\section'):
                processed_lines.append('\\vfill')
                processed_lines.append('\\pagebreak')
        
        return '\n'.join(processed_lines)
    
    def process_template(self, template: str, metadata: Dict) -> str:
        """Procesa template con soporte para condicionales"""
        import re
        
        # Procesar condicionales $if(var)$...$endif$
        def process_conditional(match):
            var_name = match.group(1)
            content = match.group(2)
            
            if var_name in metadata and metadata[var_name]:
                # Reemplazar variables dentro del bloque
                for key, value in metadata.items():
                    content = content.replace(f'${key}$', str(value))
                return content
            else:
                return ''
        
        # Procesar condicionales
        template = re.sub(r'\$if\(([^)]+)\)\$(.*?)\$endif\$', process_conditional, template, flags=re.DOTALL)
        
        # Reemplazar variables restantes
        for key, value in metadata.items():
            template = template.replace(f'${key}$', str(value))
        
        # Limpiar variables no definidas
        template = re.sub(r'\$[a-zA-Z_][a-zA-Z0-9_]*\$', '', template)
        
        return template
    
    def generate_latex_document(self, lang_dir: str) -> str:
        """Genera documento LaTeX completo para un idioma"""
        # Cargar metadatos
        metadata = self.load_metadata(lang_dir)
        
        # Leer contenido markdown
        content_file = self.base_dir / lang_dir / "content.md"
        with open(content_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Procesar contenido
        latex_content = self.process_markdown_content(markdown_content, lang_dir)
        
        # Añadir contenido a metadatos
        metadata['body'] = latex_content
        
        # Leer template
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Procesar template con metadatos
        document = self.process_template(template, metadata)
        
        return document
    
    def compile_latex_to_pdf(self, tex_file: Path) -> bool:
        """Compila archivo LaTeX a PDF"""
        try:
            # Cambiar al directorio docs para compilación
            original_dir = os.getcwd()
            os.chdir(self.docs_dir)
            
            # Ejecutar pdflatex dos veces para referencias
            for i in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_file.name],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                if result.returncode != 0:
                    print(f"Error compilando LaTeX: {result.stdout}")
                    return False
            
            # Limpiar archivos auxiliares
            for ext in ['.aux', '.log', '.out', '.toc', '.lof', '.lot']:
                aux_file = tex_file.with_suffix(ext)
                if aux_file.exists():
                    aux_file.unlink()
            
            return True
        
        except Exception as e:
            print(f"Error durante compilación: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def generate_all_docs(self):
        """Genera documentación para todos los idiomas"""
        lang_dirs = self.find_language_dirs()
        
        if not lang_dirs:
            print("No se encontraron directorios de idiomas válidos")
            return
        
        print(f"Generando documentación para idiomas: {', '.join(lang_dirs)}")
        
        for lang in lang_dirs:
            print(f"\nProcesando idioma: {lang}")
            
            try:
                # Generar documento LaTeX
                latex_doc = self.generate_latex_document(lang)
                
                # Guardar archivo .tex
                tex_filename = f"datasheet_{lang}.tex"
                tex_path = self.docs_dir / tex_filename
                
                with open(tex_path, 'w', encoding='utf-8') as f:
                    f.write(latex_doc)
                
                print(f"✓ Archivo LaTeX generado: {tex_path}")
                
                # Compilar a PDF
                if self.compile_latex_to_pdf(tex_path):
                    pdf_path = tex_path.with_suffix('.pdf')
                    print(f"✓ PDF generado: {pdf_path}")
                else:
                    print(f"✗ Error compilando PDF para {lang}")
                    
            except Exception as e:
                print(f"✗ Error procesando {lang}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Generador automático de documentación LaTeX"
    )
    parser.add_argument(
        '--dir', 
        default='.',
        help='Directorio base del proyecto (default: directorio actual)'
    )
    parser.add_argument(
        '--lang',
        help='Generar solo para un idioma específico'
    )
    
    args = parser.parse_args()
    
    generator = LaTeXDocumentGenerator(args.dir)
    
    if args.lang:
        # Generar para un idioma específico
        print(f"Generando documentación para idioma: {args.lang}")
        try:
            latex_doc = generator.generate_latex_document(args.lang)
            tex_filename = f"datasheet_{args.lang}.tex"
            tex_path = generator.docs_dir / tex_filename
            
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(latex_doc)
            
            print(f"✓ Archivo LaTeX generado: {tex_path}")
            
            if generator.compile_latex_to_pdf(tex_path):
                pdf_path = tex_path.with_suffix('.pdf')
                print(f"✓ PDF generado: {pdf_path}")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        # Generar para todos los idiomas
        generator.generate_all_docs()


if __name__ == "__main__":
    main()
