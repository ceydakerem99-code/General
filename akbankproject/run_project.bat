@echo off
title Akbank Gemini RAG System
echo =========================================
echo 🚀 AkbankProject - Otomatik Calistirici
echo =========================================
echo.

REM Ortam degiskenlerini yukle
echo [1/3] Veriler isleniyor...
python 01_veri_isleme.py

if %errorlevel% neq 0 (
    echo ❌ Hata: veri_isleme.py calismadi!
    pause
    exit /b
)

echo [2/3] Embedding veritabani olusturuluyor...
python python1.py
if %errorlevel% neq 0 (
    echo ❌ Hata: python1.py calismadi!
    pause
    exit /b
)

echo [3/3] Uygulama baslatiliyor...
python app.py
if %errorlevel% neq 0 (
    echo ❌ Hata: app.py calismadi!
    pause
    exit /b
)

echo.
echo ✅ Tum islemler basariyla tamamlandi!
echo 🌐 Tarayici: http://127.0.0.1:7860/
pause
