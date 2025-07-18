#!/usr/bin/env python3
"""
Generador simplificado de documentación LaTeX desde archivos README
"""

import os
import re
import yaml
import shutil
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List

class SimpleLatexGenerator:
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
    
    def convert_markdown_to_latex(self, content: str, lang_dir: str) -> str:
        """Convierte markdown a LaTeX de forma simple y robusta"""
        
        # Procesar headers PRIMERO antes de escapar #
        content = re.sub(r'^# (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', content, flags=re.MULTILINE)
        
        # Procesar negrita e itálica
        content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
        content = re.sub(r'\*(.*?)\*', r'\\textit{\1}', content)
        
        # Procesar código inline
        content = re.sub(r'`([^`]+)`', r'\\texttt{\1}', content)
        
        # Procesar listas
        content = self.process_simple_lists(content)
        
        # Procesar tablas
        content = self.process_simple_tables(content)
        
        # Procesar imágenes
        content = self.process_simple_images(content, lang_dir)
        
        # Procesar enlaces
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', content)
        
        # Escapar caracteres especiales AL FINAL
        content = self.escape_special_chars_final(content)
        
        return content
    
    def escape_special_chars_final(self, text: str) -> str:
        """Escapa caracteres especiales AL FINAL del procesamiento"""
        lines = text.split('\n')
        processed_lines = []
        in_table = False
        
        for line in lines:
            # Detectar si estamos en una tabla
            if 'begin{table}' in line or 'begin{tabular}' in line:
                in_table = True
                processed_lines.append(line)
                continue
            elif 'end{table}' in line or 'end{tabular}' in line:
                in_table = False
                processed_lines.append(line)
                continue
            
            # Si estamos en tabla o es comando LaTeX, no escapar
            if (in_table or 
                line.strip().startswith('\\') or 
                'begin{' in line or 'end{' in line):
                processed_lines.append(line)
            else:
                # Escapar caracteres especiales solo en texto normal
                escape_chars = {
                    '%': '\\%',
                    '$': '\\$',
                    '&': '\\&',
                    '#': '\\#',
                    '^': '\\textasciicircum{}',
                    '_': '\\_',
                    '~': '\\textasciitilde{}',
                }
                
                for char, replacement in escape_chars.items():
                    line = line.replace(char, replacement)
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def process_simple_lists(self, content: str) -> str:
        """Procesa listas de forma simple"""
        lines = content.split('\n')
        result = []
        in_list = False
        
        for line in lines:
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                if not in_list:
                    result.append('\\begin{itemize}')
                    in_list = True
                item = line.strip()[2:].strip()
                result.append(f'\\item {item}')
            elif re.match(r'^\s*\d+\.\s', line):
                if not in_list:
                    result.append('\\begin{enumerate}')
                    in_list = True
                item = re.sub(r'^\s*\d+\.\s*', '', line)
                result.append(f'\\item {item}')
            else:
                if in_list:
                    result.append('\\end{itemize}')
                    in_list = False
                result.append(line)
        
        if in_list:
            result.append('\\end{itemize}')
        
        return '\n'.join(result)
    
    def process_simple_tables(self, content: str) -> str:
        """Procesa tablas de forma simple"""
        lines = content.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            if '|' in line and i + 1 < len(lines) and '|' in lines[i + 1]:
                # Posible inicio de tabla
                table_lines = [line]
                j = i + 1
                
                # Recoger todas las líneas de la tabla
                while j < len(lines) and '|' in lines[j]:
                    table_lines.append(lines[j])
                    j += 1
                
                if len(table_lines) >= 3:  # Header + separator + at least one data row
                    latex_table = self.convert_simple_table(table_lines)
                    result.append(latex_table)
                    i = j
                else:
                    result.append(line)
                    i += 1
            else:
                result.append(line)
                i += 1
        
        return '\n'.join(result)
    
    def convert_simple_table(self, table_lines: List[str]) -> str:
        """Convierte tabla simple"""
        if len(table_lines) < 3:
            return '\n'.join(table_lines)
        
        # Header
        header_parts = [cell.strip() for cell in table_lines[0].split('|') if cell.strip()]
        num_cols = len(header_parts)
        
        # Data rows (skip separator line)
        data_rows = []
        for line in table_lines[2:]:
            parts = [cell.strip() for cell in line.split('|') if cell.strip()]
            if parts:
                # Ajustar número de columnas
                while len(parts) < num_cols:
                    parts.append('')
                data_rows.append(parts[:num_cols])
        
        if not data_rows or num_cols == 0:
            return '\n'.join(table_lines)
        
        # Generar LaTeX
        col_spec = '|' + 'c|' * num_cols
        latex = f'\\begin{{table}}[htbp]\n\\centering\n\\begin{{tabular}}{{{col_spec}}}\n\\hline\n'
        latex += ' & '.join(header_parts) + ' \\\\\n\\hline\n'
        
        for row in data_rows:
            latex += ' & '.join(row) + ' \\\\\n'
        
        latex += '\\hline\n\\end{tabular}\n\\caption{Tabla}\n\\end{table}\n\n'
        
        return latex
    
    def process_simple_images(self, content: str, lang_dir: str) -> str:
        """Procesa imágenes de forma simple"""
        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Si la imagen está en el directorio raíz, copiarla a docs
            if image_path.startswith('images/'):
                source_path = self.base_dir / image_path
                if source_path.exists():
                    dest_filename = f"{lang_dir}_{source_path.name}"
                    dest_path = self.docs_dir / dest_filename
                    shutil.copy2(source_path, dest_path)
                    
                    return f'''\\begin{{figure}}[htbp]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{dest_filename}}}
\\caption{{{alt_text}}}
\\end{{figure}}'''
            
            return f"[Imagen: {alt_text}]"
        
        return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, content)
    
    def escape_special_chars(self, text: str) -> str:
        """Escapa caracteres especiales de LaTeX de forma segura"""
        # Escapar caracteres especiales directamente sin protección compleja
        escape_chars = {
            '%': '\\%',
            '$': '\\$',
            '&': '\\&',
            '#': '\\#',
            '^': '\\textasciicircum{}',
            '_': '\\_',
            '~': '\\textasciitilde{}',
        }
        
        # Procesar línea por línea para evitar problemas con comandos LaTeX
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            # No escapar líneas que ya son comandos LaTeX
            if line.strip().startswith('\\'):
                processed_lines.append(line)
            else:
                # Escapar caracteres especiales solo en texto normal
                for char, replacement in escape_chars.items():
                    line = line.replace(char, replacement)
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def process_template(self, template: str, metadata: Dict) -> str:
        """Procesa template de forma simple"""
        # Reemplazar variables
        for key, value in metadata.items():
            template = template.replace(f'${key}$', str(value))
        
        # Limpiar condicionales no usados
        template = re.sub(r'\$if\([^)]+\)\$.*?\$endif\$', '', template, flags=re.DOTALL)
        
        # Limpiar variables no definidas
        template = re.sub(r'\$[a-zA-Z_][a-zA-Z0-9_]*\$', '', template)
        
        return template
    
    def generate_document(self, lang_dir: str) -> str:
        """Genera documento completo"""
        # Cargar metadatos
        metadata = self.load_metadata(lang_dir)
        
        # Leer contenido
        content_file = self.base_dir / lang_dir / "content.md"
        with open(content_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convertir a LaTeX
        latex_content = self.convert_markdown_to_latex(markdown_content, lang_dir)
        
        # Añadir a metadatos
        metadata['body'] = latex_content
        
        # Leer y procesar template
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        return self.process_template(template, metadata)
    
    def compile_pdf(self, tex_file: Path) -> bool:
        """Compila PDF"""
        try:
            original_dir = os.getcwd()
            os.chdir(self.docs_dir)
            
            # Compilar dos veces
            for i in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_file.name],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
                # Mostrar warnings solo en modo verbose
                if "Error" in result.stdout or result.returncode != 0:
                    if "Fatal error" in result.stdout:
                        print(f"Error fatal LaTeX: {result.stdout[-500:]}")
                        return False
            
            # Verificar que el PDF fue creado
            pdf_file = tex_file.with_suffix('.pdf')
            if pdf_file.exists() and pdf_file.stat().st_size > 0:
                # Limpiar archivos auxiliares
                for ext in ['.aux', '.log', '.out', '.toc', '.lof', '.lot']:
                    aux_file = tex_file.with_suffix(ext)
                    if aux_file.exists():
                        aux_file.unlink()
                return True
            else:
                print("PDF no fue generado correctamente")
                return False
                
        except Exception as e:
            print(f"Error compilación: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def generate_all(self):
        """Genera documentación para todos los idiomas"""
        langs = self.find_language_dirs()
        
        for lang in langs:
            print(f"Procesando {lang}...")
            
            try:
                # Generar LaTeX
                latex_doc = self.generate_document(lang)
                
                # Guardar archivo
                tex_file = self.docs_dir / f"datasheet_{lang}.tex"
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_doc)
                
                print(f"✓ LaTeX generado: {tex_file}")
                
                # Compilar PDF
                if self.compile_pdf(tex_file):
                    print(f"✓ PDF generado: {tex_file.with_suffix('.pdf')}")
                else:
                    print(f"✗ Error compilando PDF para {lang}")
                    
            except Exception as e:
                print(f"✗ Error procesando {lang}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generador LaTeX simplificado")
    parser.add_argument('--lang', help='Idioma específico')
    parser.add_argument('--dir', default='.', help='Directorio base')
    
    args = parser.parse_args()
    
    generator = SimpleLatexGenerator(args.dir)
    
    if args.lang:
        print(f"Generando para {args.lang}...")
        try:
            latex_doc = generator.generate_document(args.lang)
            tex_file = generator.docs_dir / f"datasheet_{args.lang}.tex"
            
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_doc)
            
            print(f"✓ LaTeX generado: {tex_file}")
            
            if generator.compile_pdf(tex_file):
                print(f"✓ PDF generado: {tex_file.with_suffix('.pdf')}")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        generator.generate_all()

if __name__ == "__main__":
    main()
