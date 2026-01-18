#!/bin/bash

# YouTube Transcript Viewer Launch Script
# This script sets up the environment and launches the Streamlit app

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🚀 YouTube Transcript Viewer${NC}"
echo "================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Virtual environment directory
VENV_DIR="venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"

    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}❌ Failed to create virtual environment.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Check if requirements are installed
REQUIREMENTS_FILE="requirements.txt"
REQUIREMENTS_INSTALLED="${VENV_DIR}/.requirements_installed"

if [ ! -f "$REQUIREMENTS_INSTALLED" ] || [ "$REQUIREMENTS_FILE" -nt "$REQUIREMENTS_INSTALLED" ]; then
    echo -e "${BLUE}📥 Installing dependencies...${NC}"
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r "$REQUIREMENTS_FILE"

    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}❌ Failed to install dependencies.${NC}"
        exit 1
    fi

    # Mark requirements as installed
    touch "$REQUIREMENTS_INSTALLED"
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Dependencies already installed${NC}"
fi

# Configure Streamlit
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Launch Streamlit app
echo -e "${BLUE}🌐 Launching Streamlit app...${NC}"
echo -e "${GREEN}📱 The app will open in your browser automatically${NC}"
echo -e "${YELLOW}💡 Press Ctrl+C to stop the server${NC}"
echo "================================"

streamlit run app.py --server.port=$STREAMLIT_SERVER_PORT --browser.gatherUsageStats=false

# Deactivate virtual environment on exit
deactivate
