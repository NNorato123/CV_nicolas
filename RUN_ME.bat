#!/usr/bin/env bash
# SCRIPT DE EJECUCIÓN RÁPIDA - Copia y pega esto en tu terminal

# 🎯 OPCIÓN 1: TODO EN UN COMANDO
# python -m flask --app run init-db && python run.py

# 🎯 OPCIÓN 2: PASO A PASO (más detallado)

echo "========================================="
echo "🚀 INICIANDO PORTFOLIO CORREGIDO"
echo "========================================="
echo ""

echo "📦 Paso 1/3: Inicializando base de datos con datos correctos..."
python -m flask --app run init-db
echo "✅ BD inicializada"
echo ""

echo "▶️  Paso 2/3: Iniciando servidor..."
python run.py
echo ""

echo "📱 Paso 3/3: Abre tu navegador en:"
echo "     👉 http://localhost:5000"
echo ""

echo "========================================="
echo "✨ Portfolio listo!"
echo "========================================="
