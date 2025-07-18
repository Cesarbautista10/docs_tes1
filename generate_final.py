#!/usr/bin/env python3
"""
Generador LaTeX Final - Versión corregida y optimizada
"""

import os
import re
import yaml
import shutil
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List

class LatexDocGenerator:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.docs_dir = self.base_dir / "docs"
        self.images_dir = self.base_dir / "images"
        self.template_file = self.base_dir / "template.tex"
        
        # Crear directorios
        self.docs_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
    
    def find_language_dirs(self) -> List[str]:
        """Encuentra directorios de idiomas"""
        lang_dirs = []
        for item in self.base_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                if (item / "content.md").exists() and (item / "metadata.yaml").exists():
                    lang_dirs.append(item.name)
        return sorted(lang_dirs)
    
    def load_metadata(self, lang_dir: str) -> Dict:
        """Carga metadatos"""
        metadata_file = self.base_dir / lang_dir / "metadata.yaml"
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error cargando metadatos para {lang_dir}: {e}")
            return {}
    
    def process_markdown(self, content: str, lang_dir: str) -> str:
        """Procesa markdown a LaTeX"""
        
        # 1. Headers
        content = re.sub(r'^# (.+)$', r'\\section{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', content, flags=re.MULTILINE)
        
        # 2. Imágenes ANTES de procesar otros elementos
        content = self.process_images(content, lang_dir)
        
        # 3. Tablas
        content = self.process_tables(content)
        
        # 4. Listas
        content = self.process_lists(content)
        
        # 5. Formato de texto
        content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
        content = re.sub(r'\*(.*?)\*(?!\*)', r'\\textit{\1}', content)
        content = re.sub(r'`([^`]+)`', r'\\texttt{\1}', content)
        
        # 6. Enlaces
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', content)
        
        # 7. Escapar caracteres especiales AL FINAL
        content = self.escape_latex_chars(content)
        
        return content
    
    def process_images(self, content: str, lang_dir: str) -> str:
        """Procesa imágenes markdown"""
        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Buscar imagen en diferentes ubicaciones
            source_path = None
            dest_filename = None
            
            # Opción 1: path directo desde images/
            if image_path.startswith('images/'):
                source_path = self.base_dir / image_path
                if source_path.exists():
                    dest_filename = f"{lang_dir}_{source_path.name}"
            
            # Opción 2: buscar en images/resources/
            elif image_path.startswith('resources/') or not image_path.startswith('images/'):
                # Quitar prefijo resources/ si existe
                clean_path = image_path.replace('resources/', '')
                resource_path = self.images_dir / "resources" / clean_path
                
                if resource_path.exists():
                    source_path = resource_path
                    dest_filename = f"{lang_dir}_{resource_path.name}"
                else:
                    # Buscar por nombre parcial en resources
                    resources_dir = self.images_dir / "resources"
                    if resources_dir.exists():
                        for img_file in resources_dir.glob("*"):
                            if (clean_path.lower() in img_file.name.lower() or 
                                img_file.stem.lower() in clean_path.lower()):
                                source_path = img_file
                                dest_filename = f"{lang_dir}_{img_file.name}"
                                break
            
            if source_path and source_path.exists():
                # Copiar imagen al directorio docs
                dest_path = self.docs_dir / dest_filename
                shutil.copy2(source_path, dest_path)
                
                # Determinar ancho basado en el tipo de imagen
                width = "0.8\\textwidth"
                name_lower = source_path.name.lower()
                
                if any(keyword in name_lower for keyword in ['pinout', 'pin_out', 'diagram']):
                    width = "0.9\\textwidth"
                elif any(keyword in name_lower for keyword in ['dimension', 'size', 'physical']):
                    width = "0.6\\textwidth"
                elif any(keyword in name_lower for keyword in ['schematic', 'circuit']):
                    width = "\\textwidth"
                elif any(keyword in name_lower for keyword in ['block', 'topology', 'top', 'btm']):
                    width = "0.7\\textwidth"
                
                return f'''
\\begin{{figure}}[H]
\\centering
\\includegraphics[width={width}]{{{dest_filename}}}
\\caption{{{alt_text}}}
\\label{{fig:{dest_filename.replace('.', '-').replace('_', '-')}}}
\\end{{figure}}

'''
            
            return f"[Imagen no encontrada: {image_path}]"
        
        return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, content)
    
    def process_tables(self, content: str) -> str:
        """Procesa tablas markdown"""
        lines = content.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Detectar tabla
            if '|' in line and i + 1 < len(lines) and '|' in lines[i + 1]:
                table_lines = []
                j = i
                
                # Recoger líneas de tabla
                while j < len(lines) and ('|' in lines[j] or lines[j].strip() == ''):
                    if '|' in lines[j]:
                        table_lines.append(lines[j])
                    j += 1
                
                if len(table_lines) >= 3:
                    latex_table = self.convert_table(table_lines)
                    result.append(latex_table)
                    i = j
                else:
                    result.append(line)
                    i += 1
            else:
                result.append(line)
                i += 1
        
        return '\n'.join(result)
    
    def convert_table(self, table_lines: List[str]) -> str:
        """Convierte tabla a LaTeX"""
        if len(table_lines) < 3:
            return '\n'.join(table_lines)
        
        # Header
        header_parts = [cell.strip() for cell in table_lines[0].split('|') if cell.strip()]
        num_cols = len(header_parts)
        
        if num_cols == 0:
            return '\n'.join(table_lines)
        
        # Data rows (skip separator)
        data_rows = []
        for line in table_lines[2:]:
            parts = [cell.strip() for cell in line.split('|') if cell.strip()]
            if parts:
                # Ajustar columnas
                while len(parts) < num_cols:
                    parts.append('')
                data_rows.append(parts[:num_cols])
        
        if not data_rows:
            return '\n'.join(table_lines)
        
        # Determinar especificación de columnas
        if num_cols <= 3:
            col_spec = '|' + 'c|' * num_cols
        else:
            col_spec = '|' + 'l|' * num_cols
        
        # Generar LaTeX
        latex = f'''
\\begin{{table}}[H]
\\centering
\\small
\\begin{{tabular}}{{{col_spec}}}
\\hline
'''
        
        # Header
        latex += ' & '.join(header_parts) + ' \\\\\n\\hline\n'
        
        # Data rows
        for row in data_rows:
            latex += ' & '.join(row) + ' \\\\\n'
        
        latex += '''\\hline
\\end{tabular}
\\caption{Especificaciones técnicas}
\\end{table}

'''
        
        return latex
    
    def process_lists(self, content: str) -> str:
        """Procesa listas"""
        lines = content.split('\n')
        result = []
        in_list = False
        list_type = None
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('- ') or stripped.startswith('* '):
                if not in_list:
                    result.append('\\begin{itemize}')
                    in_list = True
                    list_type = 'itemize'
                elif list_type != 'itemize':
                    result.append(f'\\end{{{list_type}}}')
                    result.append('\\begin{itemize}')
                    list_type = 'itemize'
                
                item = stripped[2:].strip()
                result.append(f'\\item {item}')
                
            elif re.match(r'^\s*\d+\.\s', line):
                if not in_list:
                    result.append('\\begin{enumerate}')
                    in_list = True
                    list_type = 'enumerate'
                elif list_type != 'enumerate':
                    result.append(f'\\end{{{list_type}}}')
                    result.append('\\begin{enumerate}')
                    list_type = 'enumerate'
                
                item = re.sub(r'^\s*\d+\.\s*', '', line)
                result.append(f'\\item {item}')
                
            else:
                if in_list:
                    result.append(f'\\end{{{list_type}}}')
                    in_list = False
                    list_type = None
                result.append(line)
        
        if in_list:
            result.append(f'\\end{{{list_type}}}')
        
        return '\n'.join(result)
    
    def escape_latex_chars(self, text: str) -> str:
        """Escapa caracteres especiales"""
        lines = text.split('\n')
        result = []
        in_latex_env = False
        
        for line in lines:
            # Detectar entornos LaTeX
            if ('\\begin{' in line or '\\end{' in line or 
                line.strip().startswith('\\') or
                '\\includegraphics' in line):
                in_latex_env = True
                result.append(line)
                continue
            
            if in_latex_env and (line.strip() == '' or '&' in line):
                result.append(line)
                continue
            else:
                in_latex_env = False
            
            # Escapar caracteres especiales solo en texto normal
            escape_chars = {
                '%': '\\%',
                '$': '\\$',
                '#': '\\#',
                '^': '\\textasciicircum{}',
                '_': '\\_',
                '~': '\\textasciitilde{}',
            }
            
            for char, replacement in escape_chars.items():
                line = line.replace(char, replacement)
            
            result.append(line)
        
        return '\n'.join(result)
    
    def process_template(self, template: str, metadata: Dict) -> str:
        """Procesa template"""
        # Reemplazar variables
        for key, value in metadata.items():
            template = template.replace(f'${key}$', str(value))
        
        # Limpiar condicionales y variables no definidas
        template = re.sub(r'\$if\([^)]+\)\$.*?\$endif\$', '', template, flags=re.DOTALL)
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
        latex_content = self.process_markdown(markdown_content, lang_dir)
        metadata['body'] = latex_content
        
        # Procesar template
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        return self.process_template(template, metadata)
    
    def compile_pdf(self, tex_file: Path) -> bool:
        """Compila PDF"""
        try:
            original_dir = os.getcwd()
            os.chdir(self.docs_dir)
            
            # Compilar 3 veces para referencias cruzadas
            for i in range(3):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_file.name],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )
                
                if "Fatal error" in result.stdout:
                    print(f"Error fatal: {result.stdout[-800:]}")
                    return False
            
            # Verificar PDF - si existe y tiene contenido, es exitoso
            pdf_file = tex_file.with_suffix('.pdf')
            if pdf_file.exists() and pdf_file.stat().st_size > 1000:
                # Limpiar archivos auxiliares
                for ext in ['.aux', '.log', '.out', '.toc', '.lof', '.lot']:
                    aux_file = tex_file.with_suffix(ext)
                    if aux_file.exists():
                        aux_file.unlink()
                return True
            else:
                print(f"PDF no generado correctamente: {pdf_file}")
                return False
            
        except Exception as e:
            print(f"Error compilación: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def generate_all(self):
        """Genera todos los documentos"""
        langs = self.find_language_dirs()
        
        if not langs:
            print("No se encontraron idiomas válidos")
            return
        
        print(f"Procesando idiomas: {', '.join(langs)}")
        
        for lang in langs:
            print(f"\n📝 Procesando {lang}...")
            
            try:
                # Generar LaTeX
                latex_doc = self.generate_document(lang)
                tex_file = self.docs_dir / f"datasheet_{lang}.tex"
                
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_doc)
                
                print(f"✅ LaTeX generado: {tex_file}")
                
                # Compilar PDF
                if self.compile_pdf(tex_file):
                    pdf_file = tex_file.with_suffix('.pdf')
                    size_kb = pdf_file.stat().st_size // 1024
                    print(f"✅ PDF generado: {pdf_file} ({size_kb} KB)")
                else:
                    print(f"❌ Error compilando PDF para {lang}")
                    
            except Exception as e:
                print(f"❌ Error procesando {lang}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generador de Documentación LaTeX")
    parser.add_argument('--lang', help='Idioma específico')
    parser.add_argument('--dir', default='.', help='Directorio base')
    
    args = parser.parse_args()
    
    generator = LatexDocGenerator(args.dir)
    
    if args.lang:
        print(f"🚀 Generando para {args.lang}...")
        try:
            latex_doc = generator.generate_document(args.lang)
            tex_file = generator.docs_dir / f"datasheet_{args.lang}.tex"
            
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_doc)
            
            print(f"✅ LaTeX generado: {tex_file}")
            
            if generator.compile_pdf(tex_file):
                pdf_file = tex_file.with_suffix('.pdf')
                size_kb = pdf_file.stat().st_size // 1024
                print(f"✅ PDF generado: {pdf_file} ({size_kb} KB)")
            else:
                print(f"❌ Error compilando PDF")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        generator.generate_all()

if __name__ == "__main__":
    main()
