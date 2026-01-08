#!/bin/bash

# AFRO-GENOMICS Platform - Quick Start Setup Script
# This script sets up both backend and frontend for local development

set -e

echo "=================================================="
echo "  AFRO-GENOMICS Platform - Setup Script"
echo "=================================================="
echo ""

# Check Python
echo "✓ Checking Python installation..."
python --version || { echo "Python 3.10+ required"; exit 1; }

# Setup Backend
echo ""
echo "📦 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python -m venv venv
fi

echo "  Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate 2>/dev/null

echo "  Installing dependencies..."
pip install -q -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "  Creating .env file..."
    cp .env.example .env
    echo "  ⚠️  Update .env with your configuration"
fi

echo "  ✓ Backend ready!"

# Setup Frontend
echo ""
echo "🎨 Setting up Frontend..."
cd ../frontend

echo "  Checking Node.js..."
node --version || { echo "Node.js 16+ required"; exit 1; }

echo "  Installing dependencies..."
npm install -q

echo "  ✓ Frontend ready!"

# Summary
echo ""
echo "=================================================="
echo "  ✅ Setup Complete!"
echo "=================================================="
echo ""
echo "To start the development servers:"
echo ""
echo "  Backend (in another terminal):"
echo "    cd backend"
echo "    source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "    python main.py"
echo "    → API: http://localhost:8000"
echo "    → Docs: http://localhost:8000/api/v1/docs"
echo ""
echo "  Frontend:"
echo "    cd frontend"
echo "    npm run dev"
echo "    → App: http://localhost:3000"
echo ""
echo "Demo Login (use any of these):"
echo "  • jane.kimani@knh.org (Lab Admin)"
echo "  • david.kipchoge@knh.org (Researcher)"
echo "  • oluwaseun.adeyemi@unilag.edu.ng (Researcher)"
echo "  Password: demo_password_123"
echo ""
echo "Documentation:"
echo "  • Design: See DESIGN.md"
echo "  • README: See README.md"
echo ""
