#!/bin/bash
set -e

echo ""
echo " Démarrage de l'environnement virtuel..."
echo ""

virtualenv --python=python3.7 venv
if [[ "$OSTYPE" == "linux-gnu" ]]; then
	source venv/bin/activate
elif [[ "$OSTYPE" == "msys" ]]; then
	./venv/Scripts/activate
fi
pip install -r requirements.txt

echo ""
echo " =============================================="
echo ""
echo "   Bienvenue dans votre environnement virtuel"
echo ""
echo "   $(python --version)"
echo ""
echo "   Tapez \"exit\" pour quitter"
echo ""
echo " =============================================="
echo ""

$SHELL $@