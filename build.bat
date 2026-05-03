@echo off
title Otel Kayit - Build

echo.
echo ================================================
echo   OTEL KAYIT SISTEMI - DERLEME ARACI v1.0
echo ================================================
echo.

if not exist "src\main.py" (
    echo HATA: Bu betik OtelKayit klasoru icinde calistirilmalidir!
    echo Dogru klasor: OtelKayit\build.bat
    pause
    exit /b 1
)

echo [1/5] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi!
    echo Lutfen https://python.org adresinden Python 3 kurun.
    echo Kurulumda "Add Python to PATH" kutusunu isaretleyin.
    pause
    exit /b 1
)
python --version
echo       Python bulundu, devam ediliyor.

echo.
echo [2/5] Gerekli kutuphane kurulumu basliyor...
echo       Internet hizine gore 1-5 dakika surebilir.
pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo HATA: Kutuphane kurulumu basarisiz!
    echo Internet baglantinizi kontrol edin.
    pause
    exit /b 1
)
echo       Kutuphaneler hazir.

echo.
echo [3/5] Eski build dosyalari temizleniyor...
if exist "dist\OtelKayit" rmdir /s /q "dist\OtelKayit"
if exist "build\OtelKayit" rmdir /s /q "build\OtelKayit"
if not exist "dist\installer" mkdir "dist\installer"
echo       Temizlik tamamlandi.

echo.
echo [4/5] PyInstaller ile derleme basliyor...
echo       Bu adim 2-5 dakika surebilir, lutfen bekleyin...
pyinstaller OtelKayit.spec --noconfirm --clean
if errorlevel 1 (
    echo HATA: PyInstaller derlemesi basarisiz!
    echo Yukaridaki hata mesajlarina bakin.
    pause
    exit /b 1
)
if not exist "dist\OtelKayit\OtelKayit.exe" (
    echo HATA: OtelKayit.exe olusturulamadi!
    pause
    exit /b 1
)
echo       Derleme tamamlandi: dist\OtelKayit\OtelKayit.exe

echo.
echo [5/5] Inno Setup ile kurulum paketi olusturuluyor...

set ISCC=""
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set ISCC="C:\Program Files\Inno Setup 6\ISCC.exe"
if exist "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" set ISCC="C:\Program Files (x86)\Inno Setup 5\ISCC.exe"
if exist "C:\Program Files\Inno Setup 5\ISCC.exe" set ISCC="C:\Program Files\Inno Setup 5\ISCC.exe"

if %ISCC%=="" (
    echo.
    echo UYARI: Inno Setup bulunamadi!
    echo Lutfen https://jrsoftware.org/isdl.php adresinden indirip kurun.
    echo Sonra build.bat'i tekrar calistirin.
    echo.
    echo PyInstaller ciktisi hazir: dist\OtelKayit\
    pause
    exit /b 0
)

%ISCC% setup.iss
if errorlevel 1 (
    echo HATA: Inno Setup derlemesi basarisiz!
    pause
    exit /b 1
)

echo.
echo ================================================
echo   DERLEME TAMAMLANDI!
echo ================================================
echo.
echo   Kurulum dosyasi: dist\installer\OtelKayitKurulum.exe
echo   Bu dosyayi hedef bilgisayara kopyalayip calistirin.
echo.
explorer dist\installer
pause
