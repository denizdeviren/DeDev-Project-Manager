import streamlit as st
import uuid
import io
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from utils.data_handler import save_data

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def get_accounting_calculations(data):
    """
    Calculates dynamic Borç (Debit) and Alacak (Credit) totals for all accounts,
    synchronizes bank account balances dynamically, and resolves account structures.
    """
    ledger = data.setdefault("accounting_ledger", [])
    bank_accounts = data.setdefault("bank_accounts", [
        {"id": "ACC-01", "name": "Nakit Kasa", "balance": 10000.0, "currency": "TRY"},
        {"id": "ACC-02", "name": "Garanti Bankası (TRY)", "balance": 50000.0, "currency": "TRY"},
        {"id": "ACC-03", "name": "Vakıfbank (EUR)", "balance": 5000.0, "currency": "EUR"},
        {"id": "ACC-04", "name": "QNB Finansbank (USD)", "balance": 8000.0, "currency": "USD"}
    ])
    
    bank_names = [acc["name"] for acc in bank_accounts]
    
    # Account categories standard listing
    revenue_accounts = ["Satış Gelirleri", "Hizmet Gelirleri", "Diğer Gelirler"]
    expense_accounts = [
        "Personel Giderleri", 
        "Sunucu / Altyapı Giderleri", 
        "Ofis / Kira Giderleri", 
        "Pazarlama Giderleri", 
        "Genel Yönetim Giderleri"
    ]
    equity_accounts = ["Özkaynaklar / Sermaye"]
    liability_accounts = ["Ödenecek KDV", "Diğer Borçlar"]
    receivable_accounts = ["Alacaklar"]
    
    all_account_names = (
        bank_names + 
        revenue_accounts + 
        expense_accounts + 
        equity_accounts + 
        liability_accounts + 
        receivable_accounts
    )
    
    # Initialize Debit and Credit totals mapping
    debits = {name: 0.0 for name in all_account_names}
    credits = {name: 0.0 for name in all_account_names}
    
    # Compute totals from double-entry ledger logs
    for tx in ledger:
        deb_acc = tx.get("debit_account")
        cred_acc = tx.get("credit_account")
        total = float(tx.get("grand_total", 0.0))
        
        # Safe addition
        if deb_acc not in debits:
            debits[deb_acc] = 0.0
            credits[deb_acc] = 0.0
        if cred_acc not in debits:
            debits[cred_acc] = 0.0
            credits[cred_acc] = 0.0
            
        debits[deb_acc] += total
        credits[cred_acc] += total
        
    # Dynamically update the bank accounts list balances in data for persistence/consistency
    for acc in bank_accounts:
        name = acc["name"]
        deb_total = debits.get(name, 0.0)
        cred_total = credits.get(name, 0.0)
        # Bank is an asset account: Debit increases it, Credit decreases it
        acc["balance"] = deb_total - cred_total
        
    return debits, credits, all_account_names, bank_names, revenue_accounts, expense_accounts, equity_accounts, liability_accounts, receivable_accounts

def export_ledger_to_excel(data):
    """
    Generates a beautifully styled corporate Excel workbook containing multi-sheet ledger data,
    Mizan, Income Statement, and Balance Sheet using openpyxl.
    """
    wb = Workbook()
    
    font_family = "Segoe UI"
    title_font = Font(name=font_family, size=15, bold=True, color="1E3A8A")
    header_font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
    bold_font = Font(name=font_family, size=10, bold=True)
    regular_font = Font(name=font_family, size=10)
    
    header_fill = PatternFill(start_color="3F51B5", end_color="3F51B5", fill_type="solid")
    zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    accent_fill = PatternFill(start_color="E0E7FF", end_color="E0E7FF", fill_type="solid")
    green_fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
    
    thin_side = Side(border_style="thin", color="E5E7EB")
    double_bottom_side = Side(border_style="double", color="1E3A8A")
    thin_top_side = Side(border_style="thin", color="1E3A8A")
    
    border_all = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    border_total = Border(top=thin_top_side, bottom=double_bottom_side)
    
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")
    
    # -------------------------------------------------------------
    # TAB 1: ÖZET & HESAP BAKİYELERİ
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Özet ve Hesap Bakiyeleri"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1["A1"] = "DeDev ERP Muhasebe Genel Hesap Bakiyeleri"
    ws1["A1"].font = title_font
    ws1.row_dimensions[1].height = 30
    
    headers = ["Hesap ID", "Hesap Adı", "Mevcut Bakiye", "Para Birimi"]
    for col_idx, h in enumerate(headers, 1):
        cell = ws1.cell(row=3, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
    ws1.row_dimensions[3].height = 24
    
    debits, credits, all_account_names, bank_names, revenue_accounts, expense_accounts, equity_accounts, liability_accounts, receivable_accounts = get_accounting_calculations(data)
    
    for row_idx, acc in enumerate(data.get("bank_accounts", []), 4):
        ws1.cell(row=row_idx, column=1, value=acc.get("id")).alignment = align_center
        ws1.cell(row=row_idx, column=2, value=acc.get("name")).alignment = align_left
        
        val_cell = ws1.cell(row=row_idx, column=3, value=float(acc.get("balance", 0.0)))
        val_cell.alignment = align_right
        val_cell.number_format = "$#,##0.00" if acc.get("currency") == "USD" else ("€#,##0.00" if acc.get("currency") == "EUR" else "₺#,##0.00")
        
        ws1.cell(row=row_idx, column=4, value=acc.get("currency")).alignment = align_center
        
        for col_idx in range(1, 5):
            c = ws1.cell(row=row_idx, column=col_idx)
            c.font = regular_font
            c.border = border_all
            if row_idx % 2 == 1:
                c.fill = zebra_fill
        ws1.row_dimensions[row_idx].height = 20
        
    # -------------------------------------------------------------
    # TAB 2: YEVMİYE DEFTERİ
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Yevmiye Defteri")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2["A1"] = "DeDeV Muhasebe Yevmiye Defteri (General Ledger)"
    ws2["A1"].font = title_font
    
    headers_ledger = [
        "İşlem ID", "Tarih", "Fiş No", "Açıklama", 
        "Borçlu Hesap", "Alacaklı Hesap", "Net Tutar", "KDV Oranı (%)", 
        "KDV Tutarı", "Genel Toplam", "İşlem Türü", "Kayıt Yapan"
    ]
    
    for col_idx, h in enumerate(headers_ledger, 1):
        cell = ws2.cell(row=3, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
    ws2.row_dimensions[3].height = 24
    
    for row_idx, tx in enumerate(data.get("accounting_ledger", []), 4):
        ws2.cell(row=row_idx, column=1, value=tx.get("id")).alignment = align_center
        ws2.cell(row=row_idx, column=2, value=tx.get("date")).alignment = align_center
        ws2.cell(row=row_idx, column=3, value=tx.get("voucher_no")).alignment = align_center
        ws2.cell(row=row_idx, column=4, value=tx.get("description")).alignment = align_left
        ws2.cell(row=row_idx, column=5, value=tx.get("debit_account")).alignment = align_left
        ws2.cell(row=row_idx, column=6, value=tx.get("credit_account")).alignment = align_left
        
        ws2.cell(row=row_idx, column=7, value=float(tx.get("amount", 0.0))).number_format = "₺#,##0.00"
        ws2.cell(row=row_idx, column=8, value=int(tx.get("tax_rate", 0))).alignment = align_center
        ws2.cell(row=row_idx, column=9, value=float(tx.get("tax_amount", 0.0))).number_format = "₺#,##0.00"
        ws2.cell(row=row_idx, column=10, value=float(tx.get("grand_total", 0.0))).number_format = "₺#,##0.00"
        
        ws2.cell(row=row_idx, column=11, value=tx.get("type")).alignment = align_center
        ws2.cell(row=row_idx, column=12, value=tx.get("created_by")).alignment = align_center
        
        for col_idx in range(1, 13):
            c = ws2.cell(row=row_idx, column=col_idx)
            c.font = regular_font
            c.border = border_all
            if row_idx % 2 == 1:
                c.fill = zebra_fill
            if tx.get("is_correction"):
                c.fill = accent_fill
        ws2.row_dimensions[row_idx].height = 20

    # -------------------------------------------------------------
    # TAB 3: MİZAN (TRIAL BALANCE)
    # -------------------------------------------------------------
    ws3 = wb.create_sheet(title="Mizan")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3["A1"] = "Dönem Sonu Mizan Tablosu"
    ws3["A1"].font = title_font
    
    headers_mizan = ["Hesap Adı", "Borç Toplamı", "Alacak Toplamı", "Borç Bakiyesi", "Alacak Bakiyesi"]
    for col_idx, h in enumerate(headers_mizan, 1):
        cell = ws3.cell(row=3, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
    ws3.row_dimensions[3].height = 24
    
    sum_deb, sum_cred, sum_deb_bal, sum_cred_bal = 0.0, 0.0, 0.0, 0.0
    curr_row = 4
    
    for acc_name in all_account_names:
        deb_val = debits.get(acc_name, 0.0)
        cred_val = credits.get(acc_name, 0.0)
        
        if deb_val == 0.0 and cred_val == 0.0:
            continue
            
        deb_bal, cred_bal = 0.0, 0.0
        # Determine normal balance behavior
        if acc_name in bank_names + expense_accounts + receivable_accounts:
            if deb_val >= cred_val:
                deb_bal = deb_val - cred_val
            else:
                cred_bal = cred_val - deb_val
        else:
            if cred_val >= deb_val:
                cred_bal = cred_val - deb_val
            else:
                deb_bal = deb_val - cred_val
                
        ws3.cell(row=curr_row, column=1, value=acc_name).alignment = align_left
        ws3.cell(row=curr_row, column=2, value=deb_val).number_format = "₺#,##0.00"
        ws3.cell(row=curr_row, column=3, value=cred_val).number_format = "₺#,##0.00"
        ws3.cell(row=curr_row, column=4, value=deb_bal).number_format = "₺#,##0.00"
        ws3.cell(row=curr_row, column=5, value=cred_bal).number_format = "₺#,##0.00"
        
        sum_deb += deb_val
        sum_cred += cred_val
        sum_deb_bal += deb_bal
        sum_cred_bal += cred_bal
        
        for col_idx in range(1, 6):
            c = ws3.cell(row=curr_row, column=col_idx)
            c.font = regular_font
            c.border = border_all
            if curr_row % 2 == 1:
                c.fill = zebra_fill
        ws3.row_dimensions[curr_row].height = 20
        curr_row += 1
        
    # Totals Row
    ws3.cell(row=curr_row, column=1, value="TOPLAM").font = bold_font
    ws3.cell(row=curr_row, column=1).alignment = align_left
    ws3.cell(row=curr_row, column=2, value=sum_deb).font = bold_font
    ws3.cell(row=curr_row, column=2).number_format = "₺#,##0.00"
    ws3.cell(row=curr_row, column=3, value=sum_cred).font = bold_font
    ws3.cell(row=curr_row, column=3).number_format = "₺#,##0.00"
    ws3.cell(row=curr_row, column=4, value=sum_deb_bal).font = bold_font
    ws3.cell(row=curr_row, column=4).number_format = "₺#,##0.00"
    ws3.cell(row=curr_row, column=5, value=sum_cred_bal).font = bold_font
    ws3.cell(row=curr_row, column=5).number_format = "₺#,##0.00"
    
    for col_idx in range(1, 6):
        c = ws3.cell(row=curr_row, column=col_idx)
        c.border = border_total
        c.fill = green_fill
    ws3.row_dimensions[curr_row].height = 22

    # -------------------------------------------------------------
    # TAB 4: GELİR TABLOSU
    # -------------------------------------------------------------
    ws4 = wb.create_sheet(title="Gelir Tablosu")
    ws4.views.sheetView[0].showGridLines = True
    
    ws4["A1"] = "Dinamik Gelir Tablosu"
    ws4["A1"].font = title_font
    
    ws4.cell(row=3, column=1, value="Gelir Kalemleri").font = bold_font
    ws4.cell(row=3, column=2, value="Tutar").font = bold_font
    ws4.cell(row=3, column=2).alignment = align_right
    ws4.row_dimensions[3].height = 22
    
    total_revenues = 0.0
    r_row = 4
    for r_acc in revenue_accounts:
        val = credits.get(r_acc, 0.0) - debits.get(r_acc, 0.0)
        ws4.cell(row=r_row, column=1, value=f"   (+) {r_acc}").font = regular_font
        ws4.cell(row=r_row, column=2, value=val).number_format = "₺#,##0.00"
        ws4.cell(row=r_row, column=2).font = regular_font
        ws4.cell(row=r_row, column=2).alignment = align_right
        total_revenues += val
        r_row += 1
        
    ws4.cell(row=r_row, column=1, value="BRÜT SATIŞ GELİRLERİ").font = bold_font
    ws4.cell(row=r_row, column=2, value=total_revenues).font = bold_font
    ws4.cell(row=r_row, column=2).number_format = "₺#,##0.00"
    ws4.cell(row=r_row, column=2).alignment = align_right
    ws4.cell(row=r_row, column=1).border = Border(top=thin_side, bottom=thin_side)
    ws4.cell(row=r_row, column=2).border = Border(top=thin_side, bottom=thin_side)
    ws4.row_dimensions[r_row].height = 20
    
    r_row += 2
    ws4.cell(row=r_row, column=1, value="Gider Kalemleri").font = bold_font
    ws4.cell(row=r_row, column=2, value="Tutar").font = bold_font
    ws4.cell(row=r_row, column=2).alignment = align_right
    r_row += 1
    
    total_expenses = 0.0
    for e_acc in expense_accounts:
        val = debits.get(e_acc, 0.0) - credits.get(e_acc, 0.0)
        ws4.cell(row=r_row, column=1, value=f"   (-) {e_acc}").font = regular_font
        ws4.cell(row=r_row, column=2, value=val).number_format = "₺#,##0.00"
        ws4.cell(row=r_row, column=2).font = regular_font
        ws4.cell(row=r_row, column=2).alignment = align_right
        total_expenses += val
        r_row += 1
        
    ws4.cell(row=r_row, column=1, value="FAALİYET GİDERLERİ TOPLAMI").font = bold_font
    ws4.cell(row=r_row, column=2, value=total_expenses).font = bold_font
    ws4.cell(row=r_row, column=2).number_format = "₺#,##0.00"
    ws4.cell(row=r_row, column=2).alignment = align_right
    ws4.cell(row=r_row, column=1).border = Border(top=thin_side, bottom=thin_side)
    ws4.cell(row=r_row, column=2).border = Border(top=thin_side, bottom=thin_side)
    ws4.row_dimensions[r_row].height = 20
    
    r_row += 2
    net_profit = total_revenues - total_expenses
    ws4.cell(row=r_row, column=1, value="DÖNEM NET KÂRI (ZARARI)").font = bold_font
    ws4.cell(row=r_row, column=2, value=net_profit).font = bold_font
    ws4.cell(row=r_row, column=2).number_format = "₺#,##0.00"
    ws4.cell(row=r_row, column=2).alignment = align_right
    ws4.cell(row=r_row, column=1).border = border_total
    ws4.cell(row=r_row, column=2).border = border_total
    ws4.cell(row=r_row, column=1).fill = green_fill
    ws4.cell(row=r_row, column=2).fill = green_fill
    ws4.row_dimensions[r_row].height = 24

    # -------------------------------------------------------------
    # TAB 5: BİLANÇO
    # -------------------------------------------------------------
    ws5 = wb.create_sheet(title="Bilanço")
    ws5.views.sheetView[0].showGridLines = True
    
    ws5["A1"] = "Dinamik Bilanço Tablosu (Balance Sheet)"
    ws5["A1"].font = title_font
    
    # Sidebar layout for Balance Sheet
    ws5.cell(row=3, column=1, value="AKTİF (VARLIKLAR)").font = header_font
    ws5.cell(row=3, column=1).fill = header_fill
    ws5.cell(row=3, column=2, value="Tutar").font = header_font
    ws5.cell(row=3, column=2).fill = header_fill
    ws5.cell(row=3, column=2).alignment = align_right
    
    ws5.cell(row=3, column=4, value="PASİF (KAYNAKLAR & ÖZKAYNAKLAR)").font = header_font
    ws5.cell(row=3, column=4).fill = header_fill
    ws5.cell(row=3, column=5, value="Tutar").font = header_font
    ws5.cell(row=3, column=5).fill = header_fill
    ws5.cell(row=3, column=5).alignment = align_right
    
    ws5.row_dimensions[3].height = 24
    
    # 1. Fill Assets side (Left)
    total_assets = 0.0
    left_row = 4
    ws5.cell(row=left_row, column=1, value="Dönen Varlıklar").font = bold_font
    left_row += 1
    
    for bank_acc in data.get("bank_accounts", []):
        bal = float(bank_acc.get("balance", 0.0))
        ws5.cell(row=left_row, column=1, value=f"   {bank_acc.get('name')}").font = regular_font
        ws5.cell(row=left_row, column=2, value=bal).number_format = "₺#,##0.00"
        ws5.cell(row=left_row, column=2).alignment = align_right
        total_assets += bal
        left_row += 1
        
    # Unpaid invoices as Receivables
    unpaid_total = sum(float(inv.get("grand_total", 0)) for inv in data.get("invoices", []) if inv.get("status") == "Beklemede")
    ws5.cell(row=left_row, column=1, value="   Alacaklar (Bekleyen Faturalar)").font = regular_font
    ws5.cell(row=left_row, column=2, value=unpaid_total).number_format = "₺#,##0.00"
    ws5.cell(row=left_row, column=2).alignment = align_right
    total_assets += unpaid_total
    left_row += 1
    
    # 2. Fill Liabilities & Equity side (Right)
    total_liab_equity = 0.0
    right_row = 4
    ws5.cell(row=right_row, column=4, value="Özkaynaklar").font = bold_font
    right_row += 1
    
    # Capital
    cap_val = credits.get("Özkaynaklar / Sermaye", 0.0) - debits.get("Özkaynaklar / Sermaye", 0.0)
    ws5.cell(row=right_row, column=4, value="   Sermaye").font = regular_font
    ws5.cell(row=right_row, column=5, value=cap_val).number_format = "₺#,##0.00"
    ws5.cell(row=right_row, column=5).alignment = align_right
    total_liab_equity += cap_val
    right_row += 1
    
    # Net Profit
    ws5.cell(row=right_row, column=4, value="   Dönem Net Kârı").font = regular_font
    ws5.cell(row=right_row, column=5, value=net_profit).number_format = "₺#,##0.00"
    ws5.cell(row=right_row, column=5).alignment = align_right
    total_liab_equity += net_profit
    right_row += 1
    
    ws5.cell(row=right_row, column=4, value="Kısa Vadeli Yükümlülükler").font = bold_font
    right_row += 1
    
    # VAT Liability
    vat_val = credits.get("Ödenecek KDV", 0.0) - debits.get("Ödenecek KDV", 0.0)
    ws5.cell(row=right_row, column=4, value="   Ödenecek KDV").font = regular_font
    ws5.cell(row=right_row, column=5, value=vat_val).number_format = "₺#,##0.00"
    ws5.cell(row=right_row, column=5).alignment = align_right
    total_liab_equity += vat_val
    right_row += 1
    
    # Resolve aligning row size
    max_rows = max(left_row, right_row)
    for r in range(4, max_rows):
        ws5.row_dimensions[r].height = 20
        for col_idx in [1, 2, 4, 5]:
            ws5.cell(row=r, column=col_idx).border = border_all
            
    # Totals Row at the very bottom
    ws5.cell(row=max_rows, column=1, value="TOPLAM AKTİF").font = bold_font
    ws5.cell(row=max_rows, column=2, value=total_assets).font = bold_font
    ws5.cell(row=max_rows, column=2).number_format = "₺#,##0.00"
    ws5.cell(row=max_rows, column=2).alignment = align_right
    
    ws5.cell(row=max_rows, column=4, value="TOPLAM PASİF").font = bold_font
    ws5.cell(row=max_rows, column=5, value=total_liab_equity).font = bold_font
    ws5.cell(row=max_rows, column=5).number_format = "₺#,##0.00"
    ws5.cell(row=max_rows, column=5).alignment = align_right
    
    for col_idx in [1, 2, 4, 5]:
        c = ws5.cell(row=max_rows, column=col_idx)
        c.border = border_total
        c.fill = green_fill
    ws5.row_dimensions[max_rows].height = 24
    
    # Apply column width optimization across all tabs
    for ws in [ws1, ws2, ws3, ws4, ws5]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)
            
    # Save into Byte Stream and return
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

def show_finance(data):
    st.markdown('<div class="section-title">💰 ERP Bütçe, Gelir & Muhasebe Sistemleri</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Çift taraflı değiştirilemez yevmiye defteri, banka bakiyeleri, mizan, bilanço ve Excel raporlayıcı</div>', unsafe_allow_html=True)
    
    from utils.data_handler import get_filtered_elements
    active_owner, active_projects, _, _, _, _, _ = get_filtered_elements(data)
    active_project_ids = {p["id"] for p in active_projects}
    
    current_username = st.session_state.get("logged_in_user", "1denizdeviren")
    
    # 1. Fetch dynamic calculations
    debits, credits, all_account_names, bank_names, revenue_accounts, expense_accounts, equity_accounts, liability_accounts, receivable_accounts = get_accounting_calculations(data)
    
    # Calculate global indicators for ERP dashboard
    total_assets = sum(float(acc.get("balance", 0.0)) for acc in data.get("bank_accounts", []))
    
    # Sum dynamic Income and Expense from the general ledger to sync the main KPIs!
    total_income = sum(credits.get(r_acc, 0.0) - debits.get(r_acc, 0.0) for r_acc in revenue_accounts)
    total_expenses = sum(debits.get(e_acc, 0.0) - credits.get(e_acc, 0.0) for e_acc in expense_accounts)
    net_profit = total_income - total_expenses
    
    # Render financial command dashboard
    st.markdown("### 📊 ERP Finansal Özet Tablosu")
    col_inc, col_exp, col_prof, col_cash = st.columns(4)
    
    with col_inc:
        st.markdown(clean_html(f"""
        <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid #10b981; border-radius: 16px; padding: 20px; text-align: center;">
            <div style="font-size: 11px; color: #10b981; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Brüt Satış Gelirleri</div>
            <div style="font-size: 26px; font-weight: 800; color: white; margin-top: 5px;">₺{total_income:,.2f}</div>
        </div>
        """), unsafe_allow_html=True)
        
    with col_exp:
        st.markdown(clean_html(f"""
        <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid #ef4444; border-radius: 16px; padding: 20px; text-align: center;">
            <div style="font-size: 11px; color: #ef4444; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Toplam Faaliyet Giderleri</div>
            <div style="font-size: 26px; font-weight: 800; color: white; margin-top: 5px;">₺{total_expenses:,.2f}</div>
        </div>
        """), unsafe_allow_html=True)
        
    with col_prof:
        prof_color = "#10b981" if net_profit >= 0 else "#ef4444"
        prof_bg = "rgba(16, 185, 129, 0.08)" if net_profit >= 0 else "rgba(239, 68, 68, 0.08)"
        st.markdown(clean_html(f"""
        <div style="background: {prof_bg}; border: 1px solid {prof_color}; border-radius: 16px; padding: 20px; text-align: center;">
            <div style="font-size: 11px; color: {prof_color}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Net Dönem Kârı (ROI)</div>
            <div style="font-size: 26px; font-weight: 800; color: white; margin-top: 5px;">₺{net_profit:,.2f}</div>
        </div>
        """), unsafe_allow_html=True)
        
    with col_cash:
        st.markdown(clean_html(f"""
        <div style="background: rgba(99, 102, 241, 0.08); border: 1px solid #6366f1; border-radius: 16px; padding: 20px; text-align: center;">
            <div style="font-size: 11px; color: #6366f1; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Toplam Kasa / Banka Varlığı</div>
            <div style="font-size: 26px; font-weight: 800; color: white; margin-top: 5px;">₺{total_assets:,.2f}</div>
        </div>
        """), unsafe_allow_html=True)

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    
    # 5 Sekmeli Muhasebe Yapısı
    tab_accounts, tab_invoices, tab_expenses, tab_ledger, tab_reports = st.tabs([
        "🏛️ Kasa & Banka Hesapları", 
        "🧾 Fatura Kesme & Gelir", 
        "💸 Gider & Masraf Takibi", 
        "📖 Defter-i Kebir (Ledger)", 
        "📊 Raporlar & Excel Dışa Aktar"
    ])
    
    # =========================================================================
    # TAB 1: KASA & BANKA HESAPLARI
    # =========================================================================
    with tab_accounts:
        st.markdown("### 🏛️ Kasa & Banka Hesap Detayları")
        
        # Balance details cards grid
        cols_acc = st.columns(4)
        for idx, acc in enumerate(data.get("bank_accounts", [])):
            col = cols_acc[idx % 4]
            symbol = "₺" if acc["currency"] == "TRY" else ("$" if acc["currency"] == "USD" else "€")
            with col:
                st.markdown(clean_html(f"""
                <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 15px; text-align: center;">
                    <div style="font-size: 12px; color: #9ca3af; font-weight: 500;">{acc["name"]}</div>
                    <div style="font-size: 22px; font-weight: 800; color: white; margin-top: 6px;">{symbol}{acc["balance"]:,.2f}</div>
                    <div style="font-size: 10px; color: #6b7280; margin-top: 4px;">Hesap ID: {acc["id"]}</div>
                </div>
                """), unsafe_allow_html=True)
                
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        col_dep_form, col_vir_form = st.columns(2)
        
        with col_dep_form:
            st.markdown("##### 💵 Manuel Para Giriş / Çıkış (Nakit Fişi)")
            with st.form("deposit_withdraw_form"):
                acc_sel = st.selectbox("İşlem Yapılacak Hesap", bank_names)
                io_type = st.selectbox("İşlem Yönü", ["Nakit Girişi (Tahsilat)", "Nakit Çıkışı (Ödeme)"])
                amount_val = st.number_input("Tutar (Net)", min_value=1.0, step=10.0)
                desc_val = st.text_input("Açıklama / Kaynak", placeholder="Örn: Ortak sermaye katkısı veya nakit kasa çıkışı")
                
                if st.form_submit_button("Fişi Sisteme İşle"):
                    if desc_val:
                        tx_id = f"TX-{str(uuid.uuid4())[:8].upper()}"
                        voucher_no = f"FİŞ-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"
                        
                        if io_type == "Nakit Girişi (Tahsilat)":
                            # Debit: selected bank account, Credit: Özkaynaklar / Sermaye
                            deb = acc_sel
                            cred = "Özkaynaklar / Sermaye"
                            action_txt = "Para Girişi"
                        else:
                            # Debit: Genel Yönetim Giderleri, Credit: selected bank account
                            deb = "Genel Yönetim Giderleri"
                            cred = acc_sel
                            action_txt = "Para Çıkışı"
                            
                        data["accounting_ledger"].append({
                            "id": tx_id,
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "voucher_no": voucher_no,
                            "description": f"{action_txt}: {desc_val}",
                            "debit_account": deb,
                            "credit_account": cred,
                            "amount": float(amount_val),
                            "tax_rate": 0,
                            "tax_amount": 0.0,
                            "grand_total": float(amount_val),
                            "type": "Para Hareketi",
                            "project_id": None,
                            "created_by": current_username,
                            "is_correction": False,
                            "corrected_tx_id": None,
                            "is_corrected": False
                        })
                        save_data(data)
                        st.toast("💵 Nakit fişi başarıyla işlendi ve hesap bakiyesi güncellendi!", icon="💵")
                        st.rerun()
                    else:
                        st.error("Lütfen işlemin açıklamasını girin.")
                        
        with col_vir_form:
            st.markdown("##### 🔄 Hesaplar Arası Virman (Para Transferi)")
            with st.form("transfer_virman_form"):
                src_acc = st.selectbox("Gönderen Hesap (Alacaklı)", bank_names)
                dest_acc = st.selectbox("Alıcı Hesap (Borçlu)", bank_names)
                transfer_amount = st.number_input("Transfer Tutarı", min_value=1.0, step=50.0)
                transfer_desc = st.text_input("Açıklama", value="Hesaplar arası virman transferi.")
                
                if st.form_submit_button("Transferi Gerçekleştir"):
                    if src_acc == dest_acc:
                        st.error("Gönderen ve alıcı hesaplar aynı olamaz!")
                    else:
                        # Validate balance
                        src_balance = next(acc["balance"] for acc in data["bank_accounts"] if acc["name"] == src_acc)
                        if transfer_amount > src_balance:
                            st.error(f"Bakiye Yetersiz! Gönderen hesap bakiyesi: ₺{src_balance:,.2f}")
                        else:
                            tx_id = f"TX-{str(uuid.uuid4())[:8].upper()}"
                            voucher_no = f"VRM-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"
                            
                            # Debit: dest_acc (increases receiving asset), Credit: src_acc (decreases giving asset)
                            data["accounting_ledger"].append({
                                "id": tx_id,
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "voucher_no": voucher_no,
                                "description": transfer_desc,
                                "debit_account": dest_acc,
                                "credit_account": src_acc,
                                "amount": float(transfer_amount),
                                "tax_rate": 0,
                                "tax_amount": 0.0,
                                "grand_total": float(transfer_amount),
                                "type": "Virman",
                                "project_id": None,
                                "created_by": current_username,
                                "is_correction": False,
                                "corrected_tx_id": None,
                                "is_corrected": False
                            })
                            save_data(data)
                            st.toast("🔄 Virman transferi başarıyla gerçekleştirildi!", icon="🔄")
                            st.rerun()

    # =========================================================================
    # TAB 2: FATURA KESME & GELİR YÖNETİMİ
    # =========================================================================
    with tab_invoices:
        col_inv_form, col_inv_list = st.columns([2, 3])
        
        with col_inv_form:
            st.markdown("### 📝 Yeni Fatura Kes")
            
            default_inv_id = f"INV-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"
            
            with st.form("new_invoice_form"):
                inv_number = st.text_input("Fatura No", value=default_inv_id)
                inv_client = st.text_input("Müşteri / Alıcı Adı", placeholder="Örn: DeDev Tech Ltd.")
                inv_proj = st.selectbox("İlgili Proje", [p['name'] for p in active_projects])
                
                col_sub1, col_sub2 = st.columns(2)
                inv_subtotal = col_sub1.number_input("Hizmet Net Tutarı (₺)", min_value=0.0, step=10.0)
                inv_vat = col_sub2.selectbox("KDV / VAT Oranı (%)", [20, 10, 8, 0], index=0)
                
                col_d1, col_d2 = st.columns(2)
                inv_date = col_d1.date_input("Düzenleme Tarihi", value=datetime.now())
                inv_due = col_d2.date_input("Vade Tarihi", value=datetime.now())
                
                inv_status = st.selectbox("Ödeme Durumu", ["Ödendi", "Beklemede"])
                
                # Bank account destination for invoice receipt
                bank_dest = st.selectbox("Alıcı Şirket Hesabı (Ödeme Yapılacak)", bank_names)
                
                inv_desc = st.text_area("Hizmet Kalemleri Açıklaması", placeholder="Hizmet detayları...")
                
                if st.form_submit_button("Faturayı Kes"):
                    if inv_client and inv_subtotal > 0:
                        proj_id = next((p['id'] for p in active_projects if p['name'] == inv_proj), None)
                        
                        tax_amount = (inv_subtotal * inv_vat) / 100
                        grand_total = inv_subtotal + tax_amount
                        
                        # Add invoice record
                        new_inv = {
                            "id": inv_number,
                            "client_name": inv_client,
                            "project_id": proj_id,
                            "project_name": inv_proj,
                            "subtotal": float(inv_subtotal),
                            "vat_rate": int(inv_vat),
                            "tax_amount": float(tax_amount),
                            "grand_total": float(grand_total),
                            "date": inv_date.strftime("%Y-%m-%d"),
                            "due_date": inv_due.strftime("%Y-%m-%d"),
                            "status": inv_status,
                            "description": inv_desc if inv_desc else "Hizmet bedeli."
                        }
                        
                        # ERP Double-Entry Sync:
                        # If paid immediately: Debit Selected Bank Account, Credit "Satış Gelirleri"
                        # If pending: Debit "Alacaklar" (Receivables), Credit "Satış Gelirleri"
                        # Additionally, calculate KDV: Credit "Ödenecek KDV" by tax_amount, while Debit receives grand_total and Credit of Satış Gelirleri holds the net subtotal.
                        
                        tx_id = f"TX-{str(uuid.uuid4())[:8].upper()}"
                        deb_acc = bank_dest if inv_status == "Ödendi" else "Alacaklar"
                        
                        data.setdefault("invoices", []).append(new_inv)
                        
                        # Log primary sales transaction
                        data["accounting_ledger"].append({
                            "id": tx_id,
                            "date": inv_date.strftime("%Y-%m-%d"),
                            "voucher_no": inv_number,
                            "description": f"Hizmet Satışı Faturası: {inv_client} - {inv_desc[:30]}",
                            "debit_account": deb_acc,
                            "credit_account": "Satış Gelirleri",
                            "amount": float(inv_subtotal),
                            "tax_rate": int(inv_vat),
                            "tax_amount": float(tax_amount),
                            "grand_total": float(grand_total),
                            "type": "Gelir",
                            "project_id": proj_id,
                            "created_by": current_username,
                            "is_correction": False,
                            "corrected_tx_id": None,
                            "is_corrected": False
                        })
                        
                        # Log KDV liability if any
                        if tax_amount > 0:
                            data["accounting_ledger"].append({
                                "id": f"TX-{str(uuid.uuid4())[:8].upper()}",
                                "date": inv_date.strftime("%Y-%m-%d"),
                                "voucher_no": inv_number,
                                "description": f"KDV Tahakkuku: {inv_number}",
                                "debit_account": deb_acc,
                                "credit_account": "Ödenecek KDV",
                                "amount": float(tax_amount),
                                "tax_rate": 0,
                                "tax_amount": 0.0,
                                "grand_total": float(tax_amount),
                                "type": "KDV Yükümlülüğü",
                                "project_id": proj_id,
                                "created_by": current_username,
                                "is_correction": False,
                                "corrected_tx_id": None,
                                "is_corrected": False
                            })
                            
                        save_data(data)
                        st.toast("🎉 Fatura başarıyla kesildi ve çift taraflı kayıt olarak yevmiye defterine işlendi!", icon="🎉")
                        st.rerun()
                    else:
                        st.error("Lütfen müşteri adını ve tutarını girin.")
                        
        with col_inv_list:
            st.markdown("### 🏢 Kesilen Faturalar")
            active_invoices = [inv for inv in data.setdefault("invoices", []) if not inv.get("project_id") or inv.get("project_id") in active_project_ids]
            
            if active_invoices:
                for inv in reversed(active_invoices):
                    status_badge_color = "#10b981" if inv["status"] == "Ödendi" else ("#f59e0b" if inv["status"] == "Beklemede" else "#ef4444")
                    status_badge_bg = "rgba(16, 185, 129, 0.08)" if inv["status"] == "Ödendi" else ("rgba(245, 158, 11, 0.08)" if inv["status"] == "Beklemede" else "rgba(239, 68, 68, 0.08)")
                    
                    inv_col, act_col = st.columns([4, 1.5])
                    
                    with inv_col:
                        st.markdown(clean_html(f"""
                        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-left: 3px solid {status_badge_color}; border-radius: 12px; padding: 15px; margin-bottom: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                                <span style="font-weight: 700; color: white; font-size: 14px;">{inv["client_name"]}</span>
                                <span style="background: {status_badge_bg}; color: {status_badge_color}; border: 1px solid {status_badge_color}; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: bold;">{inv["status"]}</span>
                            </div>
                            <div style="font-size: 11px; color: #9ca3af;">
                                🆔 {inv["id"]} | 📁 {inv.get("project_name", "Genel")}
                            </div>
                            <div style="font-size: 12px; color: #d1d5db; margin: 8px 0; line-height: 1.4;">
                                {inv.get("description", "")}
                            </div>
                            <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 8px; font-size: 11px; color: #6b7280;">
                                <span>📅 Tarih: {inv["date"]}</span>
                                <span style="font-weight: 700; color: white; font-size: 13px;">Toplam: ₺{inv["grand_total"]:,.2f}</span>
                            </div>
                        </div>
                        """), unsafe_allow_html=True)
                        
                    with act_col:
                        st.write("")  # spacer
                        # PDF/HTML printing tool
                        pdf_data = f"""
                        <html>
                        <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; color: #333; margin: 40px; line-height: 1.5; }}
                            .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #667eea; padding-bottom: 20px; margin-bottom: 30px; }}
                            .title {{ font-size: 26px; font-weight: bold; color: #667eea; }}
                            .meta-table {{ width: 100%; margin-bottom: 30px; border-collapse: collapse; }}
                            .meta-table td {{ padding: 6px 0; }}
                            .meta-table td.label {{ font-weight: bold; width: 120px; }}
                            .items-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
                            .items-table th {{ background-color: #667eea; color: white; padding: 10px; text-align: left; }}
                            .items-table td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                            .totals {{ float: right; width: 250px; text-align: right; }}
                            .totals table {{ width: 100%; }}
                            .totals td {{ padding: 6px 0; }}
                            .totals td.bold {{ font-weight: bold; font-size: 16px; border-top: 2px solid #667eea; padding-top: 8px; }}
                        </style>
                        </head>
                        <body>
                            <div class="header">
                                <div>
                                    <div class="title">DeDev Command Center</div>
                                    <div>Solo Full-Stack Developer & ERP</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-size: 20px; font-weight: bold;">RESMİ FATURA</div>
                                    <div style="font-size: 12px; color: #777;">Fatura No: {inv["id"]}</div>
                                </div>
                            </div>
                            
                            <table class="meta-table">
                                <tr>
                                    <td class="label">Müşteri / Alıcı:</td>
                                    <td>{inv["client_name"]}</td>
                                    <td class="label" style="text-align: right;">Düzenleme:</td>
                                    <td style="text-align: right;">{inv["date"]}</td>
                                </tr>
                                <tr>
                                    <td class="label">Proje:</td>
                                    <td>{inv.get("project_name", "Genel")}</td>
                                    <td class="label" style="text-align: right;">Vade:</td>
                                    <td style="text-align: right;">{inv["due_date"]}</td>
                                </tr>
                            </table>
                            
                            <table class="items-table">
                                <thead>
                                    <tr>
                                        <th>Hizmet / Açıklama</th>
                                        <th style="text-align: right; width: 100px;">KDV</th>
                                        <th style="text-align: right; width: 120px;">Tutar</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>{inv["description"]}</td>
                                        <td style="text-align: right;">%{inv["vat_rate"]}</td>
                                        <td style="text-align: right;">₺{inv["subtotal"]:,.2f}</td>
                                    </tr>
                                </tbody>
                            </table>
                            
                            <div class="totals">
                                <table>
                                    <tr>
                                        <td>Net Tutar:</td>
                                        <td>₺{inv["subtotal"]:,.2f}</td>
                                    </tr>
                                    <tr>
                                        <td>Hesaplanan KDV (%{inv["vat_rate"]}):</td>
                                        <td>₺{inv["tax_amount"]:,.2f}</td>
                                    </tr>
                                    <tr>
                                        <td class="bold">Genel Toplam:</td>
                                        <td class="bold">₺{inv["grand_total"]:,.2f}</td>
                                    </tr>
                                </table>
                            </div>
                            <div style="margin-top: 150px; font-size: 11px; color: #777; border-top: 1px solid #ddd; padding-top: 10px;">
                                Not: Bu fatura DeDev ERP Command Center sistemi tarafından elektronik ortamda oluşturulmuştur. MIT Lisanslıdır.
                            </div>
                        </body>
                        </html>
                        """
                        
                        st.download_button(
                            label="📥 İndir",
                            data=pdf_data,
                            file_name=f"Fatura-{inv['id']}.html",
                            mime="text/html",
                            key=f"dl_inv_{inv['id']}",
                            use_container_width=True
                        )
                        
                        # In the new immutable ERP, instead of deleting, we CANCEL/REVERSE the invoice!
                        if inv["status"] != "İptal Edildi":
                            if st.button("🚫 İptal Et", key=f"del_inv_{inv['id']}", help="Faturayı iptal eder ve yevmiye defterine ters düzeltme kaydı işler.", use_container_width=True):
                                # Update status
                                inv["status"] = "İptal Edildi"
                                
                                # Log a correction entry in general ledger to reverse the financial impact!
                                # Retrieve matching transactions and reverse them
                                matching_txs = [tx for tx in data.get("accounting_ledger", []) if tx.get("voucher_no") == inv["id"]]
                                for tx in matching_txs:
                                    if not tx.get("is_corrected"):
                                        tx["is_corrected"] = True
                                        
                                        corr_id = f"TX-{str(uuid.uuid4())[:8].upper()}"
                                        data["accounting_ledger"].append({
                                            "id": corr_id,
                                            "date": datetime.now().strftime("%Y-%m-%d"),
                                            "voucher_no": f"DZT-{inv['id']}",
                                            "description": f"İPTAL: Fatura No: {inv['id']} Düzeltme Fişi",
                                            # Swap credit and debit accounts to reverse values!
                                            "debit_account": tx["credit_account"],
                                            "credit_account": tx["debit_account"],
                                            "amount": tx["amount"],
                                            "tax_rate": tx["tax_rate"],
                                            "tax_amount": tx["tax_amount"],
                                            "grand_total": tx["grand_total"],
                                            "type": "Düzeltme",
                                            "project_id": tx["project_id"],
                                            "created_by": current_username,
                                            "is_correction": True,
                                            "corrected_tx_id": tx["id"],
                                            "is_corrected": False
                                        })
                                        
                                save_data(data)
                                st.toast("Fatura başarıyla iptal edildi ve ters yevmiye düzeltme kaydı deftere işlendi!", icon="🚫")
                                st.rerun()
            else:
                st.info("Henüz kesilmiş fatura kaydı yok.")

    # =========================================================================
    # TAB 3: GİDER & MASRAF TAKİBİ
    # =========================================================================
    with tab_expenses:
        col_exp_form, col_exp_list = st.columns([1, 2])
        
        with col_exp_form:
            st.markdown('### 💸 Gider Ekle')
            with st.form("new_expense_form"):
                e_title = st.text_input("Açıklama / Harcama Kalemi", placeholder="Örn: Vercel Pro Plan")
                e_amount = st.number_input("Tutar (₺)", min_value=0.0, step=1.0)
                e_proj = st.selectbox("İlgili Proje", ["Genel (Tüm Projeler)"] + [p['name'] for p in active_projects])
                
                # Account that funded the expense
                funding_acc = st.selectbox("Ödeme Yapılan Kasa/Banka", bank_names, key="exp_funding_source")
                
                # Expense categories
                exp_cat = st.selectbox("Gider Muhasebe Kategorisi", expense_accounts)
                
                e_date = st.date_input("Tarih", key="exp_date")
                
                if st.form_submit_button("Ekle"):
                    if e_title and e_amount > 0:
                        proj_id = None
                        if e_proj != "Genel (Tüm Projeler)":
                            proj_id = next((p['id'] for p in active_projects if p['name'] == e_proj), None)
                        
                        exp_id = f"EXP-{str(uuid.uuid4())[:6].upper()}"
                        
                        # Add expense record
                        data.setdefault("finances", []).append({
                            "id": exp_id,
                            "title": e_title,
                            "amount": float(e_amount),
                            "project_id": proj_id,
                            "date": e_date.strftime("%Y-%m-%d"),
                            "funding_account": funding_acc,
                            "category": exp_cat
                        })
                        
                        # Dynamic double-entry sync:
                        # Debit: Selected Expense Account (increases expenses)
                        # Credit: Selected funding bank account (decreases assets)
                        tx_id = f"TX-{str(uuid.uuid4())[:8].upper()}"
                        data["accounting_ledger"].append({
                            "id": tx_id,
                            "date": e_date.strftime("%Y-%m-%d"),
                            "voucher_no": exp_id,
                            "description": f"Gider Masrafı: {e_title}",
                            "debit_account": exp_cat,
                            "credit_account": funding_acc,
                            "amount": float(e_amount),
                            "tax_rate": 0,
                            "tax_amount": 0.0,
                            "grand_total": float(e_amount),
                            "type": "Gider",
                            "project_id": proj_id,
                            "created_by": current_username,
                            "is_correction": False,
                            "corrected_tx_id": None,
                            "is_corrected": False
                        })
                        
                        save_data(data)
                        st.toast("Gider başarıyla eklendi ve double-entry yevmiye kaydı işlendi!", icon="💸")
                        st.rerun()
                        
        with col_exp_list:
            st.markdown('### 📊 Gider Hareketleri')
            active_expenses = [f for f in data.get("finances", []) if not f.get("project_id") or f.get("project_id") in active_project_ids]
            
            if active_expenses:
                for exp in reversed(active_expenses):
                    p_name = "Genel" if not exp.get('project_id') else next((p['name'] for p in active_projects if p['id'] == exp['project_id']), "Bilinmeyen")
                    
                    item_col, del_col = st.columns([5, 1.2])
                    
                    with item_col:
                        is_canceled = exp.get("status") == "İptal"
                        strike_style = "text-decoration: line-through; opacity: 0.5;" if is_canceled else ""
                        border_color = "#ef4444" if not is_canceled else "#6b7280"
                        
                        st.markdown(clean_html(f"""
                        <div style="display: flex; justify-content: space-between; background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; border-left: 2px solid {border_color}; height: 100%; {strike_style}">
                            <div>
                                <div style="font-size: 14px; font-weight: 600; color: white;">{exp['title']}</div>
                                <div style="font-size: 11px; color: #9ca3af;">📁 {p_name} | 📅 {exp['date']} | 🏛️ {exp.get('funding_account','Kasa')}</div>
                                <div style="font-size: 10px; color: #a5b4fc; font-style: italic;">{exp.get('category','Masraf')}</div>
                            </div>
                            <div style="color: {border_color}; font-weight: bold; font-size: 16px; align-self: center; margin-right: 10px;">₺{exp['amount']}</div>
                        </div>
                        """), unsafe_allow_html=True)
                    
                    with del_col:
                        st.write("")  # spacer
                        # Cancel Expense with immutable double-entry reversal
                        if exp.get("status") != "İptal":
                            if st.button("🗑️ İptal", key=f"del_exp_{exp['id']}", help="Harcamayı iptal eder ve ters düzeltme kaydı işler.", use_container_width=True):
                                exp["status"] = "İptal"
                                
                                # Log a correction entry in ledger to reverse the financial impact
                                matching_txs = [tx for tx in data.get("accounting_ledger", []) if tx.get("voucher_no") == exp["id"]]
                                for tx in matching_txs:
                                    if not tx.get("is_corrected"):
                                        tx["is_corrected"] = True
                                        
                                        corr_id = f"TX-{str(uuid.uuid4())[:8].upper()}"
                                        data["accounting_ledger"].append({
                                            "id": corr_id,
                                            "date": datetime.now().strftime("%Y-%m-%d"),
                                            "voucher_no": f"DZT-{exp['id']}",
                                            "description": f"İPTAL: Harcama Gideri: {exp['title']} Düzeltme Fişi",
                                            # Swap credit and debit accounts to reverse values!
                                            "debit_account": tx["credit_account"],
                                            "credit_account": tx["debit_account"],
                                            "amount": tx["amount"],
                                            "tax_rate": tx["tax_rate"],
                                            "tax_amount": tx["tax_amount"],
                                            "grand_total": tx["grand_total"],
                                            "type": "Düzeltme",
                                            "project_id": tx["project_id"],
                                            "created_by": current_username,
                                            "is_correction": True,
                                            "corrected_tx_id": tx["id"],
                                            "is_corrected": False
                                        })
                                        
                                save_data(data)
                                st.toast("Gider harcaması iptal edildi ve ters yevmiye düzeltme kaydı deftere işlendi!", icon="🗑️")
                                st.rerun()
            else:
                st.info("Henüz eklenmiş bir harcama yok.")

    # =========================================================================
    # TAB 4: YEVMİYE DEFTERİ (GENERAL LEDGER)
    # =========================================================================
    with tab_ledger:
        col_new_tx, col_tx_logs = st.columns([1, 2])
        
        with col_new_tx:
            st.markdown("### 📝 Yeni Genel Fiş Girişi")
            st.markdown("""
            <div style="font-size: 11px; color: #9ca3af; margin-bottom: 12px;">
                Çift taraflı muhasebe kaydı esasına göre yevmiye fişi girin. Borçlu ve Alacaklı hesaplar dengede olmalıdır.
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("new_journal_entry_form"):
                tx_date = st.date_input("İşlem Tarihi")
                tx_desc = st.text_input("Açıklama", placeholder="Örn: QNB Bankası Faiz Tahakkuku")
                
                # Combine standard accounts listing for selections
                selectable_accounts = all_account_names
                
                deb_sel = st.selectbox("Borçlu Hesap (Debit - Değer Alan)", selectable_accounts, index=0)
                cred_sel = st.selectbox("Alacaklı Hesap (Credit - Değer Veren)", selectable_accounts, index=1)
                
                col_amt, col_tax = st.columns(2)
                base_amt = col_amt.number_input("İşlem Tutarı (₺)", min_value=1.0, step=100.0)
                tax_sel = col_tax.selectbox("KDV / Vergi Oranı (%)", [0, 8, 10, 20])
                
                link_proj = st.selectbox("İlgili Proje Entegrasyonu", ["Yok (Genel)"] + [p['name'] for p in active_projects])
                
                if st.form_submit_button("Fişi Yevmiye Defterine Kaydet"):
                    if not tx_desc:
                        st.error("Lütfen fiş açıklaması girin.")
                    elif deb_sel == cred_sel:
                        st.error("Borçlu ve alacaklı hesaplar aynı olamaz! Çift taraflı kayıt kuralına aykırıdır.")
                    else:
                        proj_id = None
                        if link_proj != "Yok (Genel)":
                            proj_id = next((p['id'] for p in active_projects if p['name'] == link_proj), None)
                            
                        # Compute KDV & Grand totals
                        t_amount = (base_amt * tax_sel) / 100
                        g_total = base_amt + t_amount
                        
                        tx_id = f"TX-{str(uuid.uuid4())[:8].upper()}"
                        voucher_no = f"YVM-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"
                        
                        # Add double-entry ledger entry
                        data["accounting_ledger"].append({
                            "id": tx_id,
                            "date": tx_date.strftime("%Y-%m-%d"),
                            "voucher_no": voucher_no,
                            "description": tx_desc,
                            "debit_account": deb_sel,
                            "credit_account": cred_sel,
                            "amount": float(base_amt),
                            "tax_rate": int(tax_sel),
                            "tax_amount": float(t_amount),
                            "grand_total": float(g_total),
                            "type": "Genel Fiş",
                            "project_id": proj_id,
                            "created_by": current_username,
                            "is_correction": False,
                            "corrected_tx_id": None,
                            "is_corrected": False
                        })
                        save_data(data)
                        st.toast("📖 Yeni yevmiye fişi başarıyla deftere işlendi!", icon="📖")
                        st.rerun()
                        
        with col_tx_logs:
            st.markdown("### 📖 Defter-i Kebir Hareketleri")
            
            # Simple filters
            filter_search = st.text_input("🔍 Açıklama veya Fiş No Ara", "")
            
            ledger_logs = data.setdefault("accounting_ledger", [])
            
            # Apply search filter
            if filter_search:
                filtered_logs = [
                    tx for tx in ledger_logs 
                    if filter_search.lower() in tx.get("description", "").lower() or 
                       filter_search.lower() in tx.get("voucher_no", "").lower()
                ]
            else:
                filtered_logs = ledger_logs
                
            if filtered_logs:
                # Beautiful paginated or list view of transactions in reverse chronological order
                for tx in reversed(filtered_logs):
                    is_corr = tx.get("is_correction", False)
                    is_corrected = tx.get("is_corrected", False)
                    
                    left_border = "#3b82f6"  # Blue for standard
                    if is_corr:
                        left_border = "#f59e0b"  # Amber for correction
                    elif is_corrected:
                        left_border = "#ef4444"  # Red for corrected/reversed
                        
                    strike_text = "text-decoration: line-through; opacity: 0.5;" if is_corrected else ""
                    
                    col_tx_card, col_action_btn = st.columns([5, 1.2])
                    
                    with col_tx_card:
                        st.markdown(clean_html(f"""
                        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-left: 4px solid {left_border}; border-radius: 12px; padding: 14px; margin-bottom: 10px; {strike_text}">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                <span style="font-weight: 700; color: white; font-size: 13px;">📃 {tx["voucher_no"]}</span>
                                <span style="font-size: 10px; color: #9ca3af;">{tx["date"]}</span>
                            </div>
                            <div style="font-size: 13px; color: #e5e7eb; margin-bottom: 8px;">{tx["description"]}</div>
                            <div style="display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 6px; font-size: 11px; color: #9ca3af; font-family: monospace;">
                                <span>🟢 Borç: {tx["debit_account"]}</span>
                                <span>🔴 Alacak: {tx["credit_account"]}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 11px; color: #a5b4fc;">
                                <span>Tür: {tx.get("type", "Yevmiye")} | Yazan: {tx.get("created_by", "system")}</span>
                                <span style="font-weight: 700; color: white; font-size: 12px;">Tutar: ₺{tx["grand_total"]:,.2f}</span>
                            </div>
                        </div>
                        """), unsafe_allow_html=True)
                        
                    with col_action_btn:
                        st.write("")
                        # Correction transaction button
                        if not is_corr and not is_corrected:
                            if st.button("🔧 Düzelt", key=f"corr_{tx['id']}", help="Bu kaydı iptal etmek için otomatik ters yevmiye düzeltme fişi oluşturur.", use_container_width=True):
                                # Mark original corrected
                                tx["is_corrected"] = True
                                
                                corr_tx_id = f"TX-{str(uuid.uuid4())[:8].upper()}"
                                corr_voucher = f"DZT-{tx['voucher_no']}"
                                
                                # Debit and Credit accounts swapped to completely cancel out the previous transaction
                                data["accounting_ledger"].append({
                                    "id": corr_tx_id,
                                    "date": datetime.now().strftime("%Y-%m-%d"),
                                    "voucher_no": corr_voucher,
                                    "description": f"Düzeltme Fişi (Ters Kayıt): {tx['description']}",
                                    "debit_account": tx["credit_account"],
                                    "credit_account": tx["debit_account"],
                                    "amount": tx["amount"],
                                    "tax_rate": tx["tax_rate"],
                                    "tax_amount": tx["tax_amount"],
                                    "grand_total": tx["grand_total"],
                                    "type": "Düzeltme",
                                    "project_id": tx.get("project_id"),
                                    "created_by": current_username,
                                    "is_correction": True,
                                    "corrected_tx_id": tx["id"],
                                    "is_corrected": False
                                })
                                save_data(data)
                                st.toast("🔧 Ters kayıt düzeltme fişi başarıyla oluşturuldu!", icon="🔧")
                                st.rerun()
                        else:
                            # Show status labels
                            if is_corr:
                                st.markdown("<div style='color: #f59e0b; font-size: 11px; font-weight: bold; text-align: center; margin-top: 10px;'>DÜZELTME FİŞİ</div>", unsafe_allow_html=True)
                            if is_corrected:
                                st.markdown("<div style='color: #ef4444; font-size: 11px; font-weight: bold; text-align: center; margin-top: 10px;'>İPTAL EDİLMİŞ</div>", unsafe_allow_html=True)
            else:
                st.info("Kayıtlı yevmiye fişi bulunamadı.")

    # =========================================================================
    # TAB 5: RAPORLAR & EXCEL DIŞA AKTAR
    # =========================================================================
    with tab_reports:
        col_mali_sel, col_excel_sheets = st.columns([2, 1])
        
        with col_mali_sel:
            st.markdown("### 📊 Otomatik Dinamik Mali Tablolar")
            mali_tab_sel = st.selectbox("Görüntülenecek Mali Tablo", ["Mizan (Trial Balance)", "Bilanço (Balance Sheet)", "Gelir Tablosu (Income Statement)"])
            
            if mali_tab_sel == "Mizan (Trial Balance)":
                st.markdown("#### ⚖️ Şirket Mizan Tablosu")
                st.markdown("<div style='font-size: 11px; color: #9ca3af; margin-bottom: 10px;'>Aktif, Pasif, Gelir ve Gider hesaplarının Borç/Alacak dengesi analizi</div>", unsafe_allow_html=True)
                
                mizan_rows = []
                sum_deb, sum_cred, sum_deb_bal, sum_cred_bal = 0.0, 0.0, 0.0, 0.0
                
                for acc_name in all_account_names:
                    deb_val = debits.get(acc_name, 0.0)
                    cred_val = credits.get(acc_name, 0.0)
                    
                    if deb_val == 0.0 and cred_val == 0.0:
                        continue
                        
                    deb_bal, cred_bal = 0.0, 0.0
                    # Determine balance normal behavior
                    if acc_name in bank_names + expense_accounts + receivable_accounts:
                        if deb_val >= cred_val:
                            deb_bal = deb_val - cred_val
                        else:
                            cred_bal = cred_val - deb_val
                    else:
                        if cred_val >= deb_val:
                            cred_bal = cred_val - deb_val
                        else:
                            deb_bal = deb_val - cred_val
                            
                    mizan_rows.append({
                        "Hesap Adı": acc_name,
                        "Borç Toplamı (₺)": deb_val,
                        "Alacak Toplamı (₺)": cred_val,
                        "Borç Bakiyesi (₺)": deb_bal,
                        "Alacak Bakiyesi (₺)": cred_bal
                    })
                    
                    sum_deb += deb_val
                    sum_cred += cred_val
                    sum_deb_bal += deb_bal
                    sum_cred_bal += cred_bal
                    
                if mizan_rows:
                    df_mizan = pd.DataFrame(mizan_rows)
                    st.dataframe(df_mizan.style.format({
                        "Borç Toplamı (₺)": "{:,.2f} ₺",
                        "Alacak Toplamı (₺)": "{:,.2f} ₺",
                        "Borç Bakiyesi (₺)": "{:,.2f} ₺",
                        "Alacak Bakiyesi (₺)": "{:,.2f} ₺"
                    }), use_container_width=True)
                    
                    # Display summary row and validation checks!
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        st.markdown(f"**Borç Toplamı:** ₺{sum_deb:,.2f} | **Alacak Toplamı:** ₺{sum_cred:,.2f}")
                    with col_b2:
                        st.markdown(f"**Borç Kalanı:** ₺{sum_deb_bal:,.2f} | **Alacak Kalanı:** ₺{sum_cred_bal:,.2f}")
                        
                    # Verification badge
                    diff_totals = abs(sum_deb - sum_cred)
                    diff_balances = abs(sum_deb_bal - sum_cred_bal)
                    if diff_totals < 0.01 and diff_balances < 0.01:
                        st.markdown("""
                        <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid #10b981; border-radius: 8px; padding: 12px; margin-top: 10px; font-weight: bold; color: #10b981; text-align: center;">
                            ✅ MİZAN DENGEDE! (Borç ve Alacak Kayıtları Tam Eşitlikle Dengelenmiştir)
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: rgba(239, 68, 68, 0.05); border: 1px solid #ef4444; border-radius: 8px; padding: 12px; margin-top: 10px; font-weight: bold; color: #ef4444; text-align: center;">
                            ⚠️ MİZAN DENGESİZ! Fark: ₺{diff_totals:,.2f}. Lütfen yevmiye fişlerinizi kontrol edin.
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Hesap hareketleri bulunamadı.")
                    
            elif mali_tab_sel == "Gelir Tablosu (Income Statement)":
                st.markdown("#### 📊 Dinamik Gelir Tablosu")
                
                total_rev = 0.0
                st.markdown("**Gelir Kalemleri (Revenues)**")
                for r_acc in revenue_accounts:
                    val = credits.get(r_acc, 0.0) - debits.get(r_acc, 0.0)
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;(+) {r_acc}: **₺{val:,.2f}**")
                    total_rev += val
                st.markdown(f"👉 **BRÜT SATIŞ GELİRLERİ:** `₺{total_rev:,.2f}`")
                st.markdown("---")
                
                total_exp = 0.0
                st.markdown("**Gider Kalemleri (Expenses)**")
                for e_acc in expense_accounts:
                    val = debits.get(e_acc, 0.0) - credits.get(e_acc, 0.0)
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;(-) {e_acc}: **₺{val:,.2f}**")
                    total_exp += val
                st.markdown(f"👉 **FAALİYET GİDERLERİ TOPLAMI:** `₺{total_exp:,.2f}`")
                st.markdown("---")
                
                net_prof_loss = total_rev - total_exp
                prof_color_txt = "#10b981" if net_prof_loss >= 0 else "#ef4444"
                st.markdown(f"""
                <div style="font-size: 18px; font-weight: 800; color: {prof_color_txt}; background: rgba(255,255,255,0.02); padding: 15px; border-radius: 8px; text-align: center; border: 1px solid {prof_color_txt}">
                    DÖNEM NET KÂRI (ZARARI): ₺{net_prof_loss:,.2f}
                </div>
                """, unsafe_allow_html=True)
                
            elif mali_tab_sel == "Bilanço (Balance Sheet)":
                st.markdown("#### ⚖️ Şirket Bilançosu")
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.markdown("##### 🏛️ AKTİF (VARLIKLAR)")
                    tot_assets = 0.0
                    st.markdown("**Dönen Varlıklar**")
                    for bank_acc in data.get("bank_accounts", []):
                        bal = float(bank_acc.get("balance", 0.0))
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;• {bank_acc.get('name')}: **₺{bal:,.2f}**")
                        tot_assets += bal
                        
                    # Receivables (unpaid invoices)
                    unpaid_invoices_total = sum(float(inv.get("grand_total", 0)) for inv in data.get("invoices", []) if inv.get("status") == "Beklemede")
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;• Alacaklar (Bekleyen Faturalar): **₺{unpaid_invoices_total:,.2f}**")
                    tot_assets += unpaid_invoices_total
                    
                    st.markdown("---")
                    st.markdown(f"💳 **TOPLAM AKTİF:** **₺{tot_assets:,.2f}**")
                    
                with col_right:
                    st.markdown("##### 🏢 PASİF (KAYNAKLAR)")
                    tot_liab_eq = 0.0
                    st.markdown("**Özkaynaklar**")
                    cap_val = credits.get("Özkaynaklar / Sermaye", 0.0) - debits.get("Özkaynaklar / Sermaye", 0.0)
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;• Sermaye: **₺{cap_val:,.2f}**")
                    
                    net_in_prof = total_income - total_expenses
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;• Dönem Net Kârı: **₺{net_in_prof:,.2f}**")
                    tot_liab_eq += cap_val + net_in_prof
                    
                    st.markdown("**Kısa Vadeli Yükümlülükler**")
                    vat_liability = credits.get("Ödenecek KDV", 0.0) - debits.get("Ödenecek KDV", 0.0)
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;• Ödenecek KDV: **₺{vat_liability:,.2f}**")
                    tot_liab_eq += vat_liability
                    
                    st.markdown("---")
                    st.markdown(f"🏦 **TOPLAM PASİF:** **KB** **₺{tot_liab_eq:,.2f}**")
                    
                # Balanced verification check
                diff_bal = abs(tot_assets - tot_liab_eq)
                if diff_bal < 0.01:
                    st.markdown(f"""
                    <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid #10b981; border-radius: 8px; padding: 12px; margin-top: 15px; font-weight: bold; color: #10b981; text-align: center;">
                        ⚖️ AKTİF VE PASİF DENGEDE! (Aktif = Pasif = ₺{tot_assets:,.2f})
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(239, 68, 68, 0.05); border: 1px solid #ef4444; border-radius: 8px; padding: 12px; margin-top: 15px; font-weight: bold; color: #ef4444; text-align: center;">
                        ⚠️ BİLANÇO DENGESİZ! Fark: ₺{diff_bal:,.2f}. Lütfen yevmiye girişlerindeki sermaye veya aktif dengesini inceleyin.
                    </div>
                    """, unsafe_allow_html=True)
                    
        with col_excel_sheets:
            st.markdown("### 📥 Dışa Aktar & Bulut")
            st.markdown("##### 📁 Excel Raporlama Servisi")
            st.markdown("""
            <div style="font-size: 11px; color: #9ca3af; margin-bottom: 15px;">
                Tüm yevmiye hareketlerini, kasa hesaplarını, mizanı, gelir tablosunu ve bilançoyu tek tıkla şık biçimlendirilmiş kurumsal çok sekmeli bir Excel tablosu olarak indirin.
            </div>
            """, unsafe_allow_html=True)
            
            # Generate Excel binary
            excel_bytes = export_ledger_to_excel(data)
            
            st.download_button(
                label="📥 Kurumsal Excel Defteri İndir",
                data=excel_bytes,
                file_name="deved_muhasebe_raporu.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            st.markdown("---")
            st.markdown("##### ☁️ Google Sheets Bulut Senkronu")
            st.markdown("""
            <div style="font-size: 11px; color: #9ca3af; margin-bottom: 12px;">
                Eğer entegrasyon aktifse, yevmiye kayıtları ve kasa bakiyeleri doğrudan Google Sheets tablolarınıza real-time olarak anlık yedeklenecektir.
            </div>
            """, unsafe_allow_html=True)
            
            from utils.gsheets_handler import is_gsheets_configured, push_to_sheets
            if is_gsheets_configured():
                if st.button("📤 Google Sheets'e Anlık Yedekle", use_container_width=True):
                    success, msg = push_to_sheets(data)
                    if success:
                        st.toast("Muhasebe defteri buluta başarıyla yedeklendi!", icon="☁️")
                    else:
                        st.error(f"Yedekleme Başarısız: {msg}")
            else:
                st.info("Google Sheets bağlantısı secrets.toml içerisinde yapılandırılmamış.")
