"""
Rezervasyon Takvim Dosyasi Yazici - v0.7
Her ay icin ayri Excel dosyasi: C:/data/rezervasyon/rezervasyon_YYYY_MM.xlsx
Satir: gunler, Sutun: oda numaralari, Hucre: AD SOYAD
"""

import os
import calendar
from datetime import date, datetime, timedelta
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

TAKVIM_BASE_DIR = "C:/data/rezervasyon"

GUN_ISIMLERI = {
    0: "Pazartesi", 1: "Salı", 2: "Çarşamba",
    3: "Perşembe", 4: "Cuma", 5: "Cumartesi", 6: "Pazar"
}


def get_takvim_path(yil, ay):
    return os.path.join(TAKVIM_BASE_DIR, f"rezervasyon_{yil}_{ay:02d}.xlsx")


def _style_header(ws, row, col, value, bg="1a1a2e", fg="ffffff", bold=True):
    cell = ws.cell(row=row, column=col, value=value)
    cell.fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
    cell.font = Font(color=fg, bold=bold, size=10)
    cell.alignment = Alignment(horizontal="center", vertical="center")
    return cell


def _style_cell(ws, row, col, value, bg="ffffff", fg="1a1a2e"):
    cell = ws.cell(row=row, column=col, value=value)
    cell.fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
    cell.font = Font(color=fg, size=9)
    cell.alignment = Alignment(horizontal="center", vertical="center")
    thin = Side(style="thin", color="d1d5db")
    cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)
    return cell


def takvim_guncelle(rezervasyonlar, odalar, yil, ay):
    """
    Verilen yil ve ay icin takvim Excel dosyasini olustur/guncelle.
    rezervasyonlar: [{'isim':..., 'soyisim':..., 'oda':..., 'giris':..., 'cikis':...}]
    odalar: ['101', '102', ...]
    """
    os.makedirs(TAKVIM_BASE_DIR, exist_ok=True)
    path = get_takvim_path(yil, ay)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"{yil}-{ay:02d}"

    # Aydaki gun sayisi
    gun_sayisi = calendar.monthrange(yil, ay)[1]
    gunler = [date(yil, ay, g) for g in range(1, gun_sayisi + 1)]

    # Oda listesi sirala
    odalar_sorted = sorted(odalar, key=lambda x: int(x) if x.isdigit() else x)

    # --- Baslik satiri ---
    # Sol ust kose bos
    _style_header(ws, 1, 1, "", bg="0f0f1a")
    ws.column_dimensions['A'].width = 22

    for col_idx, oda in enumerate(odalar_sorted, start=2):
        _style_header(ws, 1, col_idx, oda, bg="1B3A6B")
        col_letter = ws.cell(row=1, column=col_idx).column_letter
        ws.column_dimensions[col_letter].width = 18

    ws.row_dimensions[1].height = 22

    # --- Gun satirlari ---
    for row_idx, gun in enumerate(gunler, start=2):
        # Tarih + gun adi
        gun_adi = GUN_ISIMLERI[gun.weekday()]
        tarih_str = f"{gun.strftime('%d/%m/%Y')} {gun_adi}"

        # Hafta sonu farkli renk
        if gun.weekday() in (5, 6):
            tarih_bg = "2d2d44"
            tarih_fg = "94a3b8"
        else:
            tarih_bg = "1e1e30"
            tarih_fg = "e2e8f0"

        _style_header(ws, row_idx, 1, tarih_str, bg=tarih_bg, fg=tarih_fg, bold=False)
        ws.row_dimensions[row_idx].height = 20

        # Her oda icin hucre
        for col_idx, oda in enumerate(odalar_sorted, start=2):
            # Bu gun bu odada rezervasyon var mi?
            misafir = _find_misafir(rezervasyonlar, gun, oda)
            if misafir:
                isim = f"{misafir.get('isim', '')} {misafir.get('soyisim', '')}"
                _style_cell(ws, row_idx, col_idx, isim, bg="1a3a2a", fg="4ade80")
            else:
                _style_cell(ws, row_idx, col_idx, "", bg="ffffff", fg="1a1a2e")

    # Freeze ilk satir ve sutun
    ws.freeze_panes = "B2"

    wb.save(path)
    return path


def _find_misafir(rezervasyonlar, gun, oda):
    """Verilen gunde verilen odada rezervasyon var mi?"""
    for r in rezervasyonlar:
        if str(r.get('oda', '')) != str(oda):
            continue
        if r.get('durum') in ('İptal', 'Tamamlandı', 'Iptal'):
            continue
        try:
            giris = datetime.strptime(str(r.get('giris', '')), "%d/%m/%Y").date()
            cikis_str = str(r.get('cikis', ''))
            if cikis_str:
                cikis = datetime.strptime(cikis_str, "%d/%m/%Y").date()
            else:
                cikis = giris + timedelta(days=1)
            if giris <= gun < cikis:
                return r
        except:
            continue
    return None


def takvim_oku(yil, ay):
    """
    Takvim verisini DataFrame benzeri dict listesi olarak dondur.
    UI'da gostermek icin kullanilir.
    Returns: {
        'odalar': [...],
        'gunler': [{'tarih': date, 'gun_adi': str, 'hucreler': {'101': 'AD SOYAD', ...}}]
    }
    """
    # Direkt rezervasyon verisinden oku (Excel'e gerek yok)
    return None  # data_manager'dan cagrilacak


def guncelle_tum_aylar(rezervasyonlar, odalar):
    """
    Tum aktif rezervasyonlarin ait oldugu aylari guncelle.
    """
    aylar = set()
    for r in rezervasyonlar:
        if r.get('durum') in ('İptal', 'Tamamlandı', 'Iptal'):
            continue
        try:
            giris = datetime.strptime(str(r.get('giris', '')), "%d/%m/%Y").date()
            aylar.add((giris.year, giris.month))
            cikis_str = str(r.get('cikis', ''))
            if cikis_str:
                cikis = datetime.strptime(cikis_str, "%d/%m/%Y").date()
                # Cikis farkli aydaysa onu da ekle
                if cikis.year != giris.year or cikis.month != giris.month:
                    aylar.add((cikis.year, cikis.month))
        except:
            continue

    # Hicbir rezervasyon yoksa bu ayi yine de olustur
    if not aylar:
        from datetime import date
        bugun = date.today()
        aylar.add((bugun.year, bugun.month))

    for yil, ay in aylar:
        takvim_guncelle(rezervasyonlar, odalar, yil, ay)
