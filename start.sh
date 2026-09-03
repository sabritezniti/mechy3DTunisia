#!/bin/bash
echo "🎓 AI 3D Exam Platform - Starting..."
echo "======================================"
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "🚀 Launching Exam Platform..."
echo "🌐 Open your browser at: http://localhost:8501"
echo "🔐 Admin code: dev2024"
echo ""
streamlit run exam_app.py
