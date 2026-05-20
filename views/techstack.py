import streamlit as st
import plotly.graph_objects as go
from utils.encryption import decrypt_text

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_techstack(data):
    st.markdown('<div class="section-title">💻 Teknoloji Stack Haritası</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Tüm genel ve şifresi çözülmüş gizli projelerde kullanılan diller, frameworkler ve kütüphaneler</div>', unsafe_allow_html=True)

    # 1. Dynamic Technology Counter and Decryption
    unlocked_secrets = st.session_state.get("unlocked_secrets", {})
    all_tech = {}

    for proj in data.get('projects', []):
        is_sec = proj.get('is_secret', False)
        proj_id = proj['id']
        
        # Determine accessible tech stack
        proj_techs = []
        if not is_sec:
            proj_techs = proj.get('tech_stack', [])
        else:
            saved_pwd = unlocked_secrets.get(proj_id)
            if saved_pwd and proj.get('tech_stack'):
                # Decrypt tech stack string
                t_res = decrypt_text(proj['tech_stack'][0], saved_pwd)
                if t_res and t_res != "ERROR_WRONG_PASSWORD":
                    proj_techs = [t.strip() for t in t_res.split(",") if t.strip()]
            else:
                proj_techs = ["🔒 Kilitli (Kasa)"]

        for tech in proj_techs:
            if not tech:
                continue
            if tech not in all_tech:
                all_tech[tech] = {"count": 0, "projects": [], "is_locked": (tech == "🔒 Kilitli (Kasa)")}
            all_tech[tech]["count"] += 1
            proj_display_name = f"{proj['name']} 🔒" if is_sec else proj['name']
            all_tech[tech]["projects"].append(proj_display_name)

    # Pre-defined categories for beautiful grid mapping
    categories = {
        "🐍 Python Ekosistemi": ["Python", "Streamlit", "Pandas", "NumPy", "Plotly", "Scikit-learn"],
        "📱 Mobil & UI": ["Dart", "Flutter", "Provider", "React", "Vue", "HTML", "CSS", "TailwindCSS"],
        "🎮 Oyun & 3D": ["C++", "Unreal Engine 5", "Blueprints", "Blender", "Flame", "Unity", "C#"],
        "☁️ Backend & Cloud": ["Node.js", "Firebase", "OpenAI API", "PostgreSQL", "MongoDB", "Express"],
        "🤖 Yapay Zeka": ["Ollama", "PyTorch", "TensorFlow"],
        "🛠️ Diğer Araçlar & Güvenlik": ["Audacity", "Pillow", "🔒 Kilitli (Kasa)"]
    }

    # Gather any uncategorized technologies
    all_categorized = set()
    for techs in categories.values():
        for t in techs:
            all_categorized.add(t.lower())

    uncategorized_techs = []
    for t_name in all_tech.keys():
        if t_name.lower() not in all_categorized:
            uncategorized_techs.append(t_name)

    if uncategorized_techs:
        categories["✨ Diğer Ek Teknolojiler"] = uncategorized_techs

    # Render Category Grid
    for cat_name, techs in categories.items():
        # Check if we have at least one technology in this category
        has_techs = any(t in all_tech for t in techs)
        if not has_techs:
            continue

        cat_html = f"""
        <div style="margin-bottom: 24px;">
            <div style="font-size: 14px; font-weight: 600; color: #e5e7eb; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px;">
                {cat_name}
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 12px;">
        """

        for tech in techs:
            if tech in all_tech:
                info = all_tech[tech]
                size = 12 + min(info['count'] * 4, 18)
                opacity = 0.2 + min(info['count'] * 0.15, 0.7)
                
                border_color = "rgba(239, 68, 68, 0.4)" if info['is_locked'] else "rgba(102, 126, 234, 0.3)"
                bg_gradient = "linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(153, 27, 27, 0.15))" if info['is_locked'] else f"linear-gradient(135deg, rgba(102, 126, 234, {opacity}), rgba(118, 75, 162, {opacity}))"
                text_color = "#fca5a5" if info['is_locked'] else "#c7d2fe"

                cat_html += f"""
                <div style="
                    background: {bg_gradient};
                    border: 1px solid {border_color};
                    border-radius: 12px;
                    padding: 16px 20px;
                    min-width: 140px;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                    flex: 1 1 140px;
                    max-width: 220px;
                ">
                    <div style="font-size: {size}px; font-weight: 700; color: white; margin-bottom: 4px;">{tech}</div>
                    <div style="font-size: 11px; color: {text_color};">{info['count']} projede</div>
                    <div style="font-size: 10px; color: #9ca3af; margin-top: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 160px;" title="{', '.join(info['projects'])}">
                        {', '.join(info['projects'][:2])}{'...' if len(info['projects']) > 2 else ''}
                    </div>
                </div>
                """

        cat_html += "</div></div>"
        st.markdown(clean_html(cat_html), unsafe_allow_html=True)


    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size: 18px;">📊 Kod Dağılımı (Satır Bazlı - Dinamik)</div>', unsafe_allow_html=True)

    # 2. DYNAMIC LANGUAGE MAP CALCULATION
    lang_data = []
    
    # Pre-defined mapping of technologies to primary programming languages
    tech_lang_map = {
        "python": "Python",
        "streamlit": "Python",
        "scikit-learn": "Python",
        "dart": "Dart",
        "flutter": "Dart",
        "c++": "C++",
        "blueprints": "Blueprints",
        "unreal engine 5": "C++",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "node.js": "JavaScript",
        "react": "JavaScript"
    }

    for proj in data.get('projects', []):
        is_sec = proj.get('is_secret', False)
        loc = proj.get('lines_of_code', 0)
        proj_name = f"{proj['name']} 🔒" if is_sec else proj['name']
        
        if loc <= 0:
            continue
            
        # Extract tech stack
        proj_techs = []
        if not is_sec:
            proj_techs = proj.get('tech_stack', [])
        else:
            saved_pwd = unlocked_secrets.get(proj['id'])
            if saved_pwd and proj.get('tech_stack'):
                t_res = decrypt_text(proj['tech_stack'][0], saved_pwd)
                if t_res and t_res != "ERROR_WRONG_PASSWORD":
                    proj_techs = [t.strip() for t in t_res.split(",") if t.strip()]
        
        # Detect languages used
        detected_langs = []
        for t in proj_techs:
            lang_match = tech_lang_map.get(t.lower())
            if lang_match and lang_match not in detected_langs:
                detected_langs.append(lang_match)
                
        if not detected_langs:
            # Guess language from category or fallback to "Other"
            cat = proj.get("category", "").lower()
            if "python" in cat:
                detected_langs = ["Python"]
            elif "oyun" in cat or "fps" in cat or "unreal" in cat:
                detected_langs = ["C++"]
            elif "mobil" in cat or "flutter" in cat:
                detected_langs = ["Dart"]
            else:
                detected_langs = ["Diğer"]
                
        # Split LOC evenly among detected languages for this project
        split_loc = int(loc / len(detected_langs))
        for lang in detected_langs:
            lang_data.append({
                "Proje": proj_name,
                "Dil": lang,
                "Satır": split_loc
            })

    if lang_data:
        fig = go.Figure()
        unique_langs = list(set([d["Dil"] for d in lang_data]))
        
        lang_colors = {
            "Python": "#667eea",
            "Dart": "#00b4ab",
            "C++": "#3b82f6",
            "Blueprints": "#f59e0b",
            "JavaScript": "#ec4899",
            "TypeScript": "#8b5cf6",
            "Diğer": "#6b7280"
        }
        
        for lang in unique_langs:
            l_items = [d for d in lang_data if d["Dil"] == lang]
            fig.add_trace(go.Bar(
                name=lang,
                x=[d["Proje"] for d in l_items],
                y=[d["Satır"] for d in l_items],
                marker_color=lang_colors.get(lang, '#db2777'),
                text=[f"{d['Satır']:,}" for d in l_items],
                textposition='auto',
                textfont=dict(color='white')
            ))
            
        fig.update_layout(
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
            margin=dict(t=20, b=40, l=40, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Kod satırı (LOC) verisine sahip proje bulunamadı.")
