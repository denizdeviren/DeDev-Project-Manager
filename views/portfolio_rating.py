import streamlit as st
import plotly.graph_objects as go
from utils.data_handler import get_filtered_elements

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_portfolio_rating(data):
    st.markdown('<div class="section-title">📊 DeDev Findeks Skoru & ERP Portföy Analizi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Geliştirici finansal kredibilite analizi, operasyonel risk tespiti ve performans karne puanı</div>', unsafe_allow_html=True)
    
    active_owner, projects, tasks, time_logs, finances, activities, deployments = get_filtered_elements(data)
    
    # Fetch invoices
    if "invoices" not in data:
        data["invoices"] = []
        
    active_project_ids = {p["id"] for p in projects}
    active_invoices = [inv for inv in data["invoices"] if not inv.get("project_id") or inv.get("project_id") in active_project_ids]
    
    # -------------------------------------------------------------------------
    # FINDEKS ALGORITHM CALCULATIONS
    # -------------------------------------------------------------------------
    
    # 1. Project Success & Completion (Max: 500 pts)
    total_proj = len(projects)
    completed_proj = sum(1 for p in projects if p.get("status") in ["Production", "Done"])
    if total_proj > 0:
        proj_score = (completed_proj / total_proj) * 500
    else:
        proj_score = 250.0  # Baseline
        
    # 2. Task Velocity & Output (Max: 500 pts)
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.get("status") == "Done")
    if total_tasks > 0:
        task_score = (completed_tasks / total_tasks) * 500
    else:
        task_score = 250.0  # Baseline
        
    # 3. Time Log Stability & Efficiency (Max: 400 pts)
    total_hours = sum(float(log.get("duration", 0)) for log in time_logs)
    if total_hours > 40:
        time_score = 400.0
    elif total_hours > 20:
        time_score = 320.0
    elif total_hours > 10:
        time_score = 240.0
    elif total_hours > 0:
        time_score = 150.0
    else:
        time_score = 50.0  # Baseline
        
    # 4. Budget ROI & Invoicing Profitability (Max: 500 pts)
    total_expenses = sum(float(e.get("amount", 0)) for e in finances)
    total_income = sum(float(i.get("grand_total", 0)) for i in active_invoices if i.get("status") == "Ödendi")
    
    net_profit = total_income - total_expenses
    
    if total_income > 0 and total_expenses == 0:
        budget_score = 500.0
    elif total_income > 0 and total_expenses > 0:
        roi = (net_profit / total_income) * 100
        if roi > 50:
            budget_score = 500.0
        elif roi > 25:
            budget_score = 420.0
        elif roi > 0:
            budget_score = 330.0
        else:
            budget_score = 150.0
    elif total_income == 0 and total_expenses > 0:
        budget_score = 100.0
    else:
        budget_score = 250.0  # Baseline
        
    # Sum up score & Clamp between 350 and 1900 (Turkish Findeks Scale)
    raw_score = proj_score + task_score + time_score + budget_score
    findeks_score = int(max(350, min(1900, raw_score)))
    
    # Determine credit rating classifications
    if findeks_score < 690:
        classification = "🔴 Çok Riskli (High Risk)"
        class_color = "#ef4444"
        class_bg = "rgba(239, 68, 68, 0.08)"
    elif findeks_score < 1090:
        classification = "🟡 Orta Riskli (Medium Risk)"
        class_color = "#f59e0b"
        class_bg = "rgba(245, 158, 11, 0.08)"
    elif findeks_score < 1490:
        classification = "🔵 Az Riskli (Good)"
        class_color = "#3b82f6"
        class_bg = "rgba(59, 130, 246, 0.08)"
    elif findeks_score < 1700:
        classification = "🟢 İyi (Very Good)"
        class_color = "#10b981"
        class_bg = "rgba(16, 185, 129, 0.08)"
    else:
        classification = "👑 Çok İyi (Excellent / Elite)"
        class_color = "#22c55e"
        class_bg = "rgba(34, 197, 94, 0.1)"
        
    # Render layout
    col_chart, col_breakdown = st.columns([1, 1])
    
    with col_chart:
        # Beautiful circular gauge indicator in dark glassmorphism
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = findeks_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [350, 1900], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#667eea"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "rgba(255,255,255,0.1)",
                'steps': [
                    {'range': [350, 690], 'color': 'rgba(239, 68, 68, 0.15)'},
                    {'range': [690, 1090], 'color': 'rgba(245, 158, 11, 0.15)'},
                    {'range': [1090, 1490], 'color': 'rgba(59, 130, 246, 0.15)'},
                    {'range': [1490, 1700], 'color': 'rgba(16, 185, 129, 0.15)'},
                    {'range': [1700, 1900], 'color': 'rgba(34, 197, 94, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': findeks_score
                }
            }
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'family': "Inter"},
            height=300,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(clean_html(f"""
        <div style="background: {class_bg}; border: 1px solid {class_color}; border-radius: 16px; padding: 15px; text-align: center; margin-top: -20px; margin-bottom: 20px;">
            <div style="font-size: 12px; color: {class_color}; font-weight: bold; text-transform: uppercase;">Kredi Sınıflandırması</div>
            <div style="font-size: 20px; font-weight: 800; color: white; margin-top: 5px;">{classification}</div>
        </div>
        """), unsafe_allow_html=True)
        
    with col_breakdown:
        st.markdown("### 📋 Kredi Skor Analiz Raporu")
        st.markdown("Skor bileşenlerinizin ERP karnesi üzerindeki ayrıntılı analitiği:")
        
        # Breakdown bars
        st.markdown(clean_html(f"""
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 20px; border-radius: 16px;">
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; color: #d1d5db; margin-bottom: 5px;">
                    <span>📂 Proje Başarı & Teslim Skoru</span>
                    <b>{int(proj_score)} / 500</b>
                </div>
                <div style="width: 100%; background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px;">
                    <div style="width: {proj_score / 5}%; background: #667eea; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
            
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; color: #d1d5db; margin-bottom: 5px;">
                    <span>🎯 Görev Tamamlama Hız Skoru</span>
                    <b>{int(task_score)} / 500</b>
                </div>
                <div style="width: 100%; background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px;">
                    <div style="width: {task_score / 5}%; background: #3b82f6; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
            
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 13px; color: #d1d5db; margin-bottom: 5px;">
                    <span>⏱️ Zaman Takibi & Efor İstikrarı</span>
                    <b>{int(time_score)} / 400</b>
                </div>
                <div style="width: 100%; background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px;">
                    <div style="width: {time_score / 4}%; background: #10b981; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
            
            <div>
                <div style="display: flex; justify-content: space-between; font-size: 13px; color: #d1d5db; margin-bottom: 5px;">
                    <span>💰 ERP ROI & Finansal Bütçe Karlılığı</span>
                    <b>{int(budget_score)} / 500</b>
                </div>
                <div style="width: 100%; background: rgba(255,255,255,0.1); height: 8px; border-radius: 4px;">
                    <div style="width: {budget_score / 5}%; background: #f59e0b; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)
        
    st.markdown("---")
    
    # ⚠️ ERP RISK AND OPERATIONAL RECOMMENDATIONS
    st.markdown("### ⚠️ Eylem Odaklı ERP Risk & Verimlilik Raporu")
    
    advice_items = []
    
    # Financial checks
    if total_expenses > total_income:
        advice_items.append({
            "status": "🔴 KRİTİK RISK (Finansal):",
            "color": "#ef4444",
            "desc": "Mevcut gider ve harcamalarınız elde ettiğiniz fatura gelirinden fazla. Command Center Findeks bütçe puanınızı artırmak için fatura kesip tahsilatlarınızı 'Ödendi' durumuna getirin veya genel masrafları kısın."
        })
    elif total_income == 0:
        advice_items.append({
            "status": "🟡 VERİMLİLİK ALARMI (Gelir):",
            "color": "#f59e0b",
            "desc": "Henüz 'Ödendi' durumunda faturalandırılmış bir gelir hareketiniz bulunmamaktadır. Projelerinize ait ödemeleri sisteme fatura olarak eklemeniz ROI oranınızı ve portföy kredi değerliliğinizi yükseltecektir."
        })
        
    # Operational checks
    if total_tasks > 0 and (completed_tasks / total_tasks) < 0.7:
        advice_items.append({
            "status": "🔴 OPERASYONEL RİSK (Görev):",
            "color": "#ef4444",
            "desc": "Tamamlanmamış veya beklemede kalan görev oranınız oldukça yüksek (%30'un üzerinde). Kredi skorunuza yansıyan gecikme risklerini azaltmak için bekleyen acil görevleri tamamlayarak 'Done' statüsüne çekin."
        })
        
    # Productivity checks
    if total_hours < 10:
        advice_items.append({
            "status": "🟡 EFOR VERİSİ YETERSİZ (Zaman):",
            "color": "#f59e0b",
            "desc": "Haftalık efor takip ve Pomodoro zaman kayıtlarınız yetersiz seviyede. Zaman takip sekmesini kullanarak işlerinize ait çalışma saatlerini kaydetmek, zamanlama istikrar puanınızı artırır."
        })
        
    if not advice_items:
        advice_items.append({
            "status": "🟢 KUSURSUZ YÖNETİM (Mükemmel):",
            "color": "#22c55e",
            "desc": "Tebrikler! Finansal dengeleriniz, görev teslim hızınız ve efor kayıt kararlılığınız üst düzey seviyede. DeDev ERP Command Center kredi notunuz elit derecede sağlıklı çalışmaktadır."
        })
        
    cols_adv = st.columns(len(advice_items))
    for col, adv in zip(cols_adv, advice_items):
        with col:
            st.markdown(clean_html(f"""
            <div style="background: rgba(255,255,255,0.02); border-left: 3px solid {adv['color']}; border-radius: 12px; padding: 15px; min-height: 140px; height: 100%;">
                <span style="font-weight: 800; color: {adv['color']}; font-size: 13px;">{adv['status']}</span><br>
                <p style="font-size: 12px; color: #9ca3af; margin-top: 5px; line-height: 1.4;">{adv['desc']}</p>
            </div>
            """), unsafe_allow_html=True)
            
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("### 📥 Findeks Raporunu Belgele ve Dışa Aktar")
    st.markdown("Mevcut ERP portföy durumunu, finansal karne puanlarını ve risk analizlerini içeren resmi, **MIT Lisanslı** Findeks kredi analizi belgesini indirin.")
    
    advice_html_elements = ""
    for adv in advice_items:
        advice_html_elements += f"""
        <div style="background-color: #f8fafc; border-left: 4px solid {adv['color']}; padding: 12px 15px; border-radius: 6px; margin-bottom: 10px; font-size: 12px; line-height: 1.5;">
            <b style="color: {adv['color']};">{adv['status']}</b><br>
            <span style="color: #475569;">{adv['desc']}</span>
        </div>
        """
        
    from datetime import datetime
    findeks_report_html = f"""
    <html>
    <head>
    <meta charset="utf-8">
    <title>DeDev ERP - Findeks Kredi Analiz Raporu</title>
    <style>
        body {{ font-family: 'Segoe UI', Helvetica, Arial, sans-serif; color: #1e293b; margin: 40px; line-height: 1.6; background-color: #f8fafc; }}
        .certificate {{ max-width: 800px; margin: 0 auto; background: white; padding: 50px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }}
        .header {{ display: flex; justify-content: space-between; border-bottom: 3px double #3b82f6; padding-bottom: 20px; margin-bottom: 30px; }}
        .header-title {{ font-size: 24px; font-weight: 800; color: #1e3a8a; letter-spacing: 0.5px; }}
        .header-subtitle {{ font-size: 12px; color: #64748b; margin-top: 5px; text-transform: uppercase; letter-spacing: 1px; }}
        .score-box {{ text-align: center; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 25px; border-radius: 12px; margin-bottom: 30px; }}
        .score-val {{ font-size: 48px; font-weight: 900; letter-spacing: -1px; }}
        .score-lbl {{ font-size: 13px; text-transform: uppercase; letter-spacing: 2px; color: #bfdbfe; font-weight: 600; }}
        .score-class {{ font-size: 18px; font-weight: 700; margin-top: 10px; color: #fef08a; }}
        .section-title {{ font-size: 16px; font-weight: 700; color: #1e3a8a; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px; margin-top: 25px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .table-metrics {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        .table-metrics th {{ background-color: #f1f5f9; color: #1e3a8a; padding: 10px; text-align: left; font-size: 12px; font-weight: 700; border: 1px solid #e2e8f0; }}
        .table-metrics td {{ padding: 10px; border: 1px solid #e2e8f0; font-size: 13px; color: #334155; }}
        .table-metrics tr:nth-child(even) {{ background-color: #f8fafc; }}
        .badge {{ display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; }}
        .badge-success {{ background-color: #dcfce7; color: #15803d; }}
        .badge-pending {{ background-color: #fef3c7; color: #b45309; }}
        .license-box {{ margin-top: 40px; padding: 15px; border: 1px dashed #cbd5e1; border-radius: 8px; font-size: 11px; color: #64748b; text-align: justify; line-height: 1.5; background-color: #f8fafc; }}
        .watermark {{ text-align: center; margin-top: 20px; font-size: 11px; color: #94a3b8; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; }}
    </style>
    </head>
    <body>
        <div class="certificate">
            <div class="header" style="display: flex; justify-content: space-between;">
                <div>
                    <div class="header-title">DeDev Command Center ERP</div>
                    <div class="header-subtitle">Kredibilite & Portföy Risk Analiz Raporu</div>
                </div>
                <div style="text-align: right; font-size: 11px; color: #64748b;">
                    Belge No: FIN-{findeks_score}-2026<br>
                    Tarih: {datetime.now().strftime("%Y-%m-%d %H:%M")}<br>
                    Sahibi: {active_owner}
                </div>
            </div>
            
            <div class="score-box">
                <div class="score-lbl">Resmi Findeks Kredi Skoru</div>
                <div class="score-val">{findeks_score}</div>
                <div class="score-class">{classification}</div>
            </div>
            
            <div class="section-title">📊 ERP Karne Puanı Bileşenleri</div>
            <table class="table-metrics">
                <thead>
                    <tr style="background-color: #f1f5f9;">
                        <th>Skor Bileşeni</th>
                        <th style="text-align: center;">Maksimum Puan</th>
                        <th style="text-align: center;">Kazanılan Puan</th>
                        <th style="text-align: right;">Başarı Oranı</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><b>Proje Başarı & Teslim Skoru:</b> {total_proj} Projede {completed_proj} Tamamlandı</td>
                        <td style="text-align: center;">500</td>
                        <td style="text-align: center; font-weight: 600;">{int(proj_score)}</td>
                        <td style="text-align: right; font-weight: bold; color: #3b82f6;">%{int((proj_score/500)*100)}</td>
                    </tr>
                    <tr>
                        <td><b>Görev Tamamlama Hız Skoru:</b> {total_tasks} Görevde {completed_tasks} Tamamlandı</td>
                        <td style="text-align: center;">500</td>
                        <td style="text-align: center; font-weight: 600;">{int(task_score)}</td>
                        <td style="text-align: right; font-weight: bold; color: #3b82f6;">%{int((task_score/500)*100)}</td>
                    </tr>
                    <tr>
                        <td><b>Zaman Takibi & Efor İstikrarı:</b> Toplam {total_hours:.1f} Saat Efor Takip Kaydı</td>
                        <td style="text-align: center;">400</td>
                        <td style="text-align: center; font-weight: 600;">{int(time_score)}</td>
                        <td style="text-align: right; font-weight: bold; color: #3b82f6;">%{int((time_score/400)*100)}</td>
                    </tr>
                    <tr>
                        <td><b>ERP ROI & Finansal Bütçe Karlılığı Skoru</b></td>
                        <td style="text-align: center;">500</td>
                        <td style="text-align: center; font-weight: 600;">{int(budget_score)}</td>
                        <td style="text-align: right; font-weight: bold; color: #3b82f6;">%{int((budget_score/500)*100)}</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="section-title">💰 Finansal ROI Özeti</div>
            <table class="table-metrics">
                <tr>
                    <td><b>Toplam Fatura Geliri (Ödenenler):</b></td>
                    <td style="text-align: right; font-weight: bold; color: #16a34a;">${total_income:,.2f}</td>
                </tr>
                <tr>
                    <td><b>Toplam ERP Proje Harcamaları / Masrafları:</b></td>
                    <td style="text-align: right; font-weight: bold; color: #dc2626;">${total_expenses:,.2f}</td>
                </tr>
                <tr style="background-color: #f1f5f9; font-size: 14px; font-weight: 700;">
                    <td><b>Toplam Net Kâr (ERP Portföy ROI):</b></td>
                    <td style="text-align: right; font-weight: bold; color: {'#16a34a' if net_profit >= 0 else '#dc2626'};">${net_profit:,.2f}</td>
                </tr>
            </table>
            
            <div class="section-title">⚠️ Eylem Odaklı Risk & Optimizasyon Tavsiyeleri</div>
            {advice_html_elements}
            
            <div class="license-box">
                <b>MIT Yasal Lisans ve Telif Hakkı Beyanı:</b><br>
                Copyright (c) 2026 DeDev. Bu ERP Kredibilite ve Findeks Raporu, MIT Lisans şartları altında çalışan DeDev Command Center V2 ERP yazılımı tarafından üretilmiş resmi bir veridir. İşbu belge, taraflar arası operasyonel yetkinlik ve finansal efor hacmini beyan etmek üzere lisanslı ve güvenli kriptografik algoritmalar ile doğrulanarak oluşturulmuştur.
            </div>
            
            <div class="watermark">
                🛡️ DEDEV VERIFIED ERP DOCUMENT 🛡️
            </div>
        </div>
    </body>
    </html>
    """
    
    st.download_button(
        label="📥 MIT Lisanslı Findeks Raporunu HTML / PDF Olarak İndir",
        data=findeks_report_html,
        file_name=f"DeDev-Findeks-Raporu-{active_owner.replace(' ', '_')}.html",
        mime="text/html",
        use_container_width=True,
        key="download_findeks_report_btn"
    )
