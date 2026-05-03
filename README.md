Hotel Registration and Room Management System
A lightweight Windows desktop application for hotel receptionists to manage guest registrations and room availability. Built with Python, PyQt5, and Excel-based data storage.
Features
Guest Registration — Record guest details with TC ID validation and autocomplete for returning guests
Active Guests Panel — View all checked-in guests at a glance, with edit and checkout functionality
Room Status Panel — Real-time overview of all rooms (available / occupied)
Search & Archive — Search across all historical records by name, surname, or TC ID with year/quarter filters
Backup Reminder — Automatic warning if data has not been backed up in over 30 days
Tech Stack
Layer	Technology
Language	Python 3.x
UI	PyQt5
Data storage	openpyxl (Excel .xlsx)
Distribution	PyInstaller + Inno Setup
Target OS	Windows
Data Structure
All records are stored in a single `kayitlar.xlsx` file. Sheets are named by year and quarter: `2025_Q1`, `2025_Q2`, `2025_Q3`, `2025_Q4`. A new quarter sheet is created automatically when needed. Room status is tracked in a separate `Odalar` sheet within the same file.
File Structure
```
C:/OtelKayit/
  app/
    OtelKayit.exe
  data/
    kayitlar.xlsx
  config/
    ayarlar.cfg
```
Getting Started
Requirements
Python 3.x (with "Add to PATH" checked during installation)
Inno Setup 6 (for building the installer)
Build
```
cd C:\OtelKayit
build.bat
```
The build script will automatically install dependencies, compile with PyInstaller, and package with Inno Setup. The output installer will be at `dist\installer\OtelKayitKurulum.exe`.
Install on target machine
Run `OtelKayitKurulum.exe` on the target Windows machine. The installer creates the folder structure, registers the application, and adds a desktop shortcut.
Modules
Registration Module — Form with TC ID, name, surname, room selection (available rooms only), check-in/out dates, and payment info. Autocomplete suggests returning guests based on previous records.
Active Guests Panel — Shows all guests with status `Aktif`. Each card displays payment status — a red warning is shown if payment has not been recorded. Supports inline edit and one-click checkout.
Room Status Panel — Grid view of all rooms. Green = available, red = occupied. Room list feeds directly into the registration form dropdown.
Search & Archive — Full-history search across all quarters and years. Filterable by year, quarter, and status.
Settings — Add or remove rooms, trigger manual backup, view application info.
Versioning
This project follows a simple version tag system on GitHub releases.
Version	Description
v0.1	First working release — all core modules functional
License
For internal use only.
