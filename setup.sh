#!/bin/bash

# 🚀 Documentation System Setup Script
# This script sets up the development environment for the automated documentation system

set -e  # Exit on any error

echo "📚 DevLab Documentation System Setup"
echo "===================================="
echo ""

# Color definitions for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on supported system
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_warning "This script is designed for Linux systems. Manual setup may be required on other platforms."
fi

# Check for required commands
check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is available"
        return 0
    else
        print_error "$1 is not installed"
        return 1
    fi
}

print_status "Checking system dependencies..."

# Check Python
if check_command python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python version: $PYTHON_VERSION"
else
    print_error "Python 3 is required but not installed"
    exit 1
fi

# Check pip
if ! check_command pip3 && ! check_command pip; then
    print_error "pip is required but not installed"
    exit 1
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install --user -r requirements.txt
else
    pip install --user -r requirements.txt
fi

if python3 -c "import yaml" 2>/dev/null; then
    print_success "PyYAML installed successfully"
else
    print_error "Failed to install PyYAML"
    exit 1
fi

# Check LaTeX installation
print_status "Checking LaTeX installation..."
if check_command pdflatex; then
    LATEX_VERSION=$(pdflatex --version | head -n1)
    print_status "LaTeX: $LATEX_VERSION"
else
    print_warning "LaTeX not found. Installing LaTeX packages..."
    
    if command -v apt-get &> /dev/null; then
        print_status "Installing LaTeX via apt-get..."
        sudo apt-get update -qq
        sudo apt-get install -y \
            texlive-latex-recommended \
            texlive-fonts-recommended \
            texlive-latex-extra \
            texlive-lang-spanish \
            texlive-lang-english
        
        if check_command pdflatex; then
            print_success "LaTeX installed successfully"
        else
            print_error "LaTeX installation failed"
            exit 1
        fi
    else
        print_error "Cannot install LaTeX automatically. Please install manually:"
        echo "  - Ubuntu/Debian: sudo apt-get install texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra"
        echo "  - CentOS/RHEL: sudo yum install texlive-latex texlive-collection-fontsrecommended"
        echo "  - macOS: brew install --cask mactex"
        exit 1
    fi
fi

# Verify project structure
print_status "Verifying project structure..."

REQUIRED_FILES=(
    "template.tex"
    "generate_final.py"
    "en/content.md"
    "en/metadata.yaml"
    "es/content.md"
    "es/metadata.yaml"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        print_success "Found: $file"
    else
        print_error "Missing: $file"
        ((MISSING_FILES++))
    fi
done

if [[ $MISSING_FILES -gt 0 ]]; then
    print_error "Missing $MISSING_FILES required files. Please ensure you're in the correct directory."
    exit 1
fi

# Check images directory
if [[ -d "images/resources" ]]; then
    IMAGE_COUNT=$(find images/resources -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" | wc -l)
    print_success "Images directory found with $IMAGE_COUNT image files"
else
    print_warning "Images directory (images/resources/) not found. Creating it..."
    mkdir -p images/resources
    print_status "Please add your hardware images to images/resources/"
fi

# Create docs directory if it doesn't exist
if [[ ! -d "docs" ]]; then
    print_status "Creating docs/ directory..."
    mkdir -p docs
fi

# Test documentation generation
print_status "Testing documentation generation..."

# Clean previous builds first
print_status "Cleaning previous build artifacts..."
rm -rf docs/*.pdf docs/*.tex docs/*.log docs/*.aux docs/*.out docs/*.toc docs/*.lof docs/*.lot 2>/dev/null || true
rm -rf docs/*_*.png docs/*_*.jpg docs/*_*.jpeg 2>/dev/null || true
print_success "Build directory cleaned"

echo ""
echo "🧪 Testing English documentation..."
if python3 generate_final.py --lang en; then
    if [[ -f "docs/datasheet_en.pdf" ]]; then
        PDF_SIZE=$(stat -c%s "docs/datasheet_en.pdf" 2>/dev/null || stat -f%z "docs/datasheet_en.pdf" 2>/dev/null || echo "0")
        if [[ $PDF_SIZE -gt 5000 ]]; then
            print_success "English PDF generated successfully ($PDF_SIZE bytes)"
        else
            print_warning "English PDF generated but seems small ($PDF_SIZE bytes)"
        fi
    else
        print_error "English PDF not generated"
    fi
else
    print_error "English documentation generation failed"
fi

echo ""
echo "🧪 Testing Spanish documentation..."
if python3 generate_final.py --lang es; then
    if [[ -f "docs/datasheet_es.pdf" ]]; then
        PDF_SIZE=$(stat -c%s "docs/datasheet_es.pdf" 2>/dev/null || stat -f%z "docs/datasheet_es.pdf" 2>/dev/null || echo "0")
        if [[ $PDF_SIZE -gt 5000 ]]; then
            print_success "Spanish PDF generated successfully ($PDF_SIZE bytes)"
        else
            print_warning "Spanish PDF generated but seems small ($PDF_SIZE bytes)"
        fi
    else
        print_error "Spanish PDF not generated"
    fi
else
    print_error "Spanish documentation generation failed"
fi

# Display results
echo ""
echo "📊 Setup Summary"
echo "==============="
echo ""

if [[ -f "docs/datasheet_en.pdf" && -f "docs/datasheet_es.pdf" ]]; then
    print_success "✅ Setup completed successfully!"
    echo ""
    echo "📄 Generated files:"
    ls -lh docs/*.pdf 2>/dev/null || echo "No PDFs found"
    echo ""
    echo "🚀 Next steps:"
    echo "  1. Review generated PDFs in the docs/ directory"
    echo "  2. Edit content in en/content.md and es/content.md"
    echo "  3. Add images to images/resources/"
    echo "  4. Regenerate docs: python3 generate_final.py --lang en"
    echo "  5. Commit and push to trigger CI/CD pipeline"
else
    print_warning "⚠️  Setup completed with warnings"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "  1. Check LaTeX installation: pdflatex --version"
    echo "  2. Verify Python dependencies: python3 -c 'import yaml'"
    echo "  3. Review content files for syntax errors"
    echo "  4. Check images directory: ls images/resources/"
fi

echo ""
echo "📚 For more information, see README.md"
echo ""
