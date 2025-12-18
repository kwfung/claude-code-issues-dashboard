#!/bin/bash
# Quick start script for Issue Categorization Toolkit

echo "=================================="
echo "Issue Categorization Quick Start"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if pandas is installed
python3 -c "import pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠ pandas not found. Installing..."
    pip install pandas
fi

echo "✓ pandas installed"
echo ""

# Check for input files
if [ ! -f "data/raw_issues.csv" ]; then
    echo "❌ data/raw_issues.csv not found"
    echo "   Please place your GitHub issues CSV in data/raw_issues.csv"
    exit 1
fi

if [ ! -f "data/taxonomy_l1_l2.csv" ]; then
    echo "❌ data/taxonomy_l1_l2.csv not found"
    echo "   Please place your taxonomy CSV in data/taxonomy_l1_l2.csv"
    echo "   (or rename taxonomy_l1_l2_EXAMPLE.csv)"
    exit 1
fi

echo "✓ Input files found"
echo ""

# Create output directory
mkdir -p output/reports

# Run classification
echo "🚀 Running classification..."
python3 scripts/classify_issues.py \
    --input data/raw_issues.csv \
    --taxonomy data/taxonomy_l1_l2.csv \
    --output output/classified_issues.csv \
    --progress

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Classification complete!"
    echo ""
    
    # Run analysis
    echo "📊 Generating reports..."
    python3 scripts/analyze_results.py \
        --input output/classified_issues.csv \
        --output-dir output/reports/
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=================================="
        echo "✅ All done!"
        echo "=================================="
        echo ""
        echo "📁 Results:"
        echo "   - Classified issues: output/classified_issues.csv"
        echo "   - Summary report: output/reports/summary_report.md"
        echo "   - Edge cases: output/reports/edge_cases.csv"
        echo ""
    fi
fi
