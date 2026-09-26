"""Hojas de estilo QSS para el tema Cyber-Gym (Modo Oscuro / Modo Claro)."""

QSS_MODO_OSCURO = """
    QMainWindow { background-color: #0F172A; }
    QWidget { color: #F8FAFC; font-family: 'Segoe UI', Roboto, -apple-system, Helvetica, Arial, sans-serif; font-size: 13px; }
    QLabel { color: #F8FAFC; }
    QLineEdit, QComboBox {
        background-color: #1E293B; color: #F8FAFC; border: 1px solid #334155;
        border-radius: 6px; padding: 8px 12px; selection-background-color: #F97316;
    }
    QLineEdit:focus, QComboBox:focus { border: 1.5px solid #F97316; background-color: #0F172A; }
    QPushButton {
        background-color: #F97316; color: #FFFFFF; border: none;
        border-radius: 6px; padding: 10px 16px; font-weight: bold;
    }
    QPushButton:hover { background-color: #EA580C; }
    QPushButton:pressed { background-color: #C2410C; }
    QGroupBox {
        font-weight: bold; font-size: 13px; color: #38BDF8; border: 1px solid #334155;
        border-radius: 8px; margin-top: 12px; padding-top: 15px; background-color: #1E293B;
    }
    QGroupBox::title {
        subcontrol-origin: margin; subcontrol-position: top left; padding: 2px 8px;
        background-color: #0F172A; border-radius: 4px; color: #38BDF8;
    }
    QTableWidget { background-color: #1E293B; color: #F8FAFC; gridline-color: #334155; border: 1px solid #334155; border-radius: 6px; }
    QTableWidget::item { padding: 6px; }
    QTableWidget::item:selected { background-color: #F97316; color: #FFFFFF; }
    QHeaderView::section { background-color: #0F172A; color: #38BDF8; padding: 8px; font-weight: bold; border: 1px solid #334155; }
    QStatusBar { background-color: #0F172A; color: #94A3B8; border-top: 1px solid #1E293B; }
"""

QSS_MODO_CLARO = """
    QMainWindow { background-color: #F8FAFC; }
    QWidget { color: #0F172A; font-family: 'Segoe UI', Roboto, -apple-system, Helvetica, Arial, sans-serif; font-size: 13px; }
    QLabel { color: #0F172A; }
    QLineEdit, QComboBox {
        background-color: #FFFFFF; color: #0F172A; border: 1px solid #CBD5E1;
        border-radius: 6px; padding: 8px 12px; selection-background-color: #F97316;
    }
    QLineEdit:focus, QComboBox:focus { border: 1.5px solid #F97316; background-color: #FFFFFF; }
    QPushButton {
        background-color: #F97316; color: #FFFFFF; border: none;
        border-radius: 6px; padding: 10px 16px; font-weight: bold;
    }
    QPushButton:hover { background-color: #EA580C; }
    QPushButton:pressed { background-color: #C2410C; }
    QGroupBox {
        font-weight: bold; font-size: 13px; color: #0284C7; border: 1px solid #E2E8F0;
        border-radius: 8px; margin-top: 12px; padding-top: 15px; background-color: #FFFFFF;
    }
    QGroupBox::title {
        subcontrol-origin: margin; subcontrol-position: top left; padding: 2px 8px;
        background-color: #F1F5F9; border-radius: 4px; color: #0284C7;
    }
    QTableWidget { background-color: #FFFFFF; color: #0F172A; gridline-color: #E2E8F0; border: 1px solid #CBD5E1; border-radius: 6px; }
    QTableWidget::item { padding: 6px; }
    QTableWidget::item:selected { background-color: #F97316; color: #FFFFFF; }
    QHeaderView::section { background-color: #F1F5F9; color: #0284C7; padding: 8px; font-weight: bold; border: 1px solid #CBD5E1; }
    QStatusBar { background-color: #F1F5F9; color: #475569; border-top: 1px solid #E2E8F0; }
"""
