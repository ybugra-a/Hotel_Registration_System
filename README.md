# Otel Kayit ve Oda Yonetim Sistemi
## Kurulum ve Derleme Kilavuzu

---

## KLASOR YAPISI

```
OtelKayit/
  src/                    ← Python kaynak kodlari
    main.py
    data_manager.py
    kayit_modulu.py
    aktif_musteri_paneli.py
    oda_durumu_paneli.py
    arama_arsiv.py
    ayarlar.py
    styles.py
  OtelKayit.spec          ← PyInstaller yapilandirmasi
  setup.iss               ← Inno Setup kurulum scripti
  build.bat               ← Otomatik derleme betigi
  requirements.txt        ← Python bagimliliklar
  README.md               ← Bu dosya
```

---

## ADIM 1 - PYTHON KUR

1. https://python.org/downloads adresine git
2. "Download Python 3.x.x" butonuna tikla
3. Kurulum sirasinda **"Add Python to PATH"** kutucugunu mutlaka isaretle
4. Kurulumu tamamla

Kontrol: Komut satirinda `python --version` yazinca versiyon gormeli.

---

## ADIM 2 - INNO SETUP KUR

1. https://jrsoftware.org/isdl.php adresine git
2. "Inno Setup 6.x.x" indir
3. Varsayilan ayarlarla kur

---

## ADIM 3 - DERLE (TEK TIKLA)

1. Bu klasoru bir yere kopyala (orn: `C:\OtelKayitBuild\`)
2. `build.bat` dosyasina **cift tikla**
3. Siyah pencere acilacak, islemleri izle
4. Tamamlaninca `dist\installer\OtelKayitKurulum.exe` olusacak

---

## ADIM 4 - HEDEF BILGISAYARA KUR

1. `OtelKayitKurulum.exe` dosyasini USB bellee kopyala
2. Hedef bilgisayarda USB'den calistir
3. Kurulum sihirbazini takip et
4. Bitince masaustunde "Otel Kayit Sistemi" kisayolu olusur

---

## ILK KULLANIM

- Uygulama ilk acildiginda otomatik olarak `C:\OtelKayit\` yapisi olusur
- Ayarlar sekmesinden odalar ekle (101, 102, 103 vb.)
- Kayit formundan ilk musteri kaydini gir

---

## VERI YEDEKLEME

- `C:\OtelKayit\data\kayitlar.xlsx` tum verileri icerir
- Ayarlar > "Simdi Yedekle" butonu ile yedek al
- Her 30 gunde bir uygulama acilisinda hatirlatma yapar

---

## SORUN GIDERME

**"Python bulunamadi" hatasi:**
- Python'u "Add to PATH" secenegiyle yeniden kur

**"Inno Setup bulunamadi" uyarisi:**
- Inno Setup'i kur ve build.bat'i tekrar calistir
- Ya da setup.iss dosyasini Inno Setup ile manuel ac ve derle

**PyQt5 import hatasi:**
- Komut satirinda: `pip install PyQt5 --force-reinstall`

**Excel dosyasi acilamadi:**
- `C:\OtelKayit\data\` klasorunun var oldugunu kontrol et
- Baska bir program Excel dosyasini acik tutuyorsa kapat
