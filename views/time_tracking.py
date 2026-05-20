import streamlit as st
import time
from datetime import datetime
from utils.data_handler import save_data

def clean_html(html_str):
    return "\n".join([line.strip() for line in html_str.split("\n")])

def show_time_tracking(data):
    st.markdown('<div class="section-title">⏱️ Pomodoro & Zaman Takibi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Görevlerine odaklan ve harcadığın süreyi projelerine kaydet</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1.9])

    with col1:
        st.markdown('### 🍅 Pomodoro Sayacı')
        
        # Real-time HTML5/JS Pomodoro Timer Component
        pomodoro_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {
                    background: transparent;
                    margin: 0;
                    padding: 0;
                    font-family: 'Inter', system-ui, -apple-system, sans-serif;
                    color: white;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                }
                .pomodoro-card {
                    background: rgba(255, 255, 255, 0.02);
                    border: 1px solid rgba(255, 255, 255, 0.06);
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 20px;
                    width: 290px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                }
                .tabs {
                    display: flex;
                    gap: 4px;
                    margin-bottom: 20px;
                    background: rgba(0, 0, 0, 0.2);
                    padding: 4px;
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.05);
                    width: 100%;
                    box-sizing: border-box;
                }
                .tab-btn {
                    flex: 1;
                    background: transparent;
                    border: none;
                    color: #9ca3af;
                    padding: 8px 4px;
                    font-size: 11px;
                    font-weight: 600;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    text-align: center;
                }
                .tab-btn.active {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
                }
                .timer-circle-container {
                    position: relative;
                    width: 170px;
                    height: 170px;
                    margin-bottom: 20px;
                }
                .timer-circle-container svg {
                    transform: rotate(-90deg);
                    width: 100%;
                    height: 100%;
                }
                .bg-circle {
                    fill: none;
                    stroke: rgba(255, 255, 255, 0.04);
                    stroke-width: 8px;
                }
                .progress-circle {
                    fill: none;
                    stroke: url(#timer-grad);
                    stroke-width: 8px;
                    stroke-linecap: round;
                    stroke-dasharray: 502; /* 2 * PI * r (r=80) */
                    stroke-dashoffset: 0;
                    transition: stroke-dashoffset 0.1s linear;
                }
                .time-display {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    font-size: 34px;
                    font-weight: 700;
                    letter-spacing: -1px;
                    color: white;
                    text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
                    font-variant-numeric: tabular-nums;
                }
                .controls {
                    display: flex;
                    gap: 16px;
                }
                .control-btn {
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    color: white;
                    border-radius: 50%;
                    width: 46px;
                    height: 46px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    font-size: 16px;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }
                .control-btn:hover {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                    border-color: transparent;
                }
                .control-btn:active {
                    transform: translateY(0px) scale(0.95);
                }
            </style>
        </head>
        <body>
            <div class="pomodoro-card">
                <div class="tabs">
                    <button class="tab-btn active" onclick="setMode('focus', 25)">🍅 Odaklan</button>
                    <button class="tab-btn" onclick="setMode('short', 5)">☕ Kısa Mola</button>
                    <button class="tab-btn" onclick="setMode('long', 15)">🌌 Uzun Mola</button>
                </div>
                
                <div class="timer-circle-container">
                    <svg viewBox="0 0 180 180">
                        <defs>
                            <linearGradient id="timer-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#667eea" />
                                <stop offset="100%" stop-color="#764ba2" />
                            </linearGradient>
                        </defs>
                        <circle class="bg-circle" cx="90" cy="90" r="80"></circle>
                        <circle id="progress" class="progress-circle" cx="90" cy="90" r="80"></circle>
                    </svg>
                    <div id="time" class="time-display">25:00</div>
                </div>
                
                <div class="controls">
                    <button id="play-pause" class="control-btn" onclick="toggleTimer()" title="Başlat / Duraklat">▶️</button>
                    <button class="control-btn" onclick="resetTimer()" title="Sıfırla">🔄</button>
                </div>
            </div>

            <script>
                var totalDuration = 25 * 60;
                var timeLeft = totalDuration;
                var timerId = null;
                var isRunning = false;
                var currentMode = 'focus';
                
                var timeDisplay = document.getElementById('time');
                var progressCircle = document.getElementById('progress');
                var playPauseBtn = document.getElementById('play-pause');
                
                var totalDash = 2 * Math.PI * 80; // 502.65

                function updateDisplay() {
                    var mins = Math.floor(timeLeft / 60);
                    var secs = timeLeft % 60;
                    timeDisplay.textContent = (mins < 10 ? '0' : '') + mins + ':' + (secs < 10 ? '0' : '') + secs;
                    
                    var offset = totalDash - (timeLeft / totalDuration) * totalDash;
                    progressCircle.style.strokeDashoffset = offset;
                }

                function toggleTimer() {
                    if (isRunning) {
                        clearInterval(timerId);
                        timerId = null;
                        isRunning = false;
                        playPauseBtn.textContent = '▶️';
                    } else {
                        isRunning = true;
                        playPauseBtn.textContent = '⏸️';
                        timerId = setInterval(function() {
                            if (timeLeft > 0) {
                                timeLeft--;
                                updateDisplay();
                            } else {
                                clearInterval(timerId);
                                timerId = null;
                                isRunning = false;
                                playPauseBtn.textContent = '▶️';
                                playChime();
                                alert(currentMode === 'focus' ? 'Tebrikler, odaklanma süresi bitti! Şimdi mola zamanı.' : 'Mola bitti! Yeni bir odaklanma seansı başlatmaya hazır mısınız?');
                            }
                        }, 1000);
                    }
                }

                function resetTimer() {
                    clearInterval(timerId);
                    timerId = null;
                    isRunning = false;
                    playPauseBtn.textContent = '▶️';
                    if (currentMode === 'focus') timeLeft = 25 * 60;
                    else if (currentMode === 'short') timeLeft = 5 * 60;
                    else if (currentMode === 'long') timeLeft = 15 * 60;
                    updateDisplay();
                }

                function setMode(mode, mins) {
                    currentMode = mode;
                    totalDuration = mins * 60;
                    timeLeft = totalDuration;
                    
                    var btns = document.querySelectorAll('.tab-btn');
                    btns.forEach(function(btn) { btn.classList.remove('active'); });
                    event.target.classList.add('active');
                    
                    resetTimer();
                }

                function playChime() {
                    try {
                        var AudioContext = window.AudioContext || window.webkitAudioContext;
                        var ctx = new AudioContext();
                        
                        // Ding tone
                        var osc1 = ctx.createOscillator();
                        var gain1 = ctx.createGain();
                        osc1.type = 'sine';
                        osc1.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
                        gain1.gain.setValueAtTime(0.3, ctx.currentTime);
                        gain1.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.2);
                        osc1.connect(gain1);
                        gain1.connect(ctx.destination);
                        osc1.start();
                        osc1.stop(ctx.currentTime + 1.2);
                        
                        // Dong tone
                        setTimeout(function() {
                            var osc2 = ctx.createOscillator();
                            var gain2 = ctx.createGain();
                            osc2.type = 'sine';
                            osc2.frequency.setValueAtTime(880.00, ctx.currentTime); // A5
                            gain2.gain.setValueAtTime(0.3, ctx.currentTime);
                            gain2.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.5);
                            osc2.connect(gain2);
                            gain2.connect(ctx.destination);
                            osc2.start();
                            osc2.stop(ctx.currentTime + 1.5);
                        }, 180);
                    } catch(e) {
                        console.error("Audio synthesis error:", e);
                    }
                }

                updateDisplay();
            </script>
        </body>
        </html>
        """
        
        st.components.v1.html(pomodoro_html, height=340)
        
        st.markdown('### 📝 Süreyi Günlüğe Kaydet')
        
        # Duration recording form
        selected_proj = st.selectbox("Çalışılan Proje", [p['name'] for p in data.get("projects", [])], key="tracking_proj_select")
        task_desc = st.text_input("Şu an ne üzerinde çalışıyorsun?", placeholder="Örn: Emlak AI modeli eğitimi", key="tracking_task_desc")
        duration_mins = st.number_input("Harcadığın Süre (Dakika)", min_value=1, max_value=480, value=25, step=5, help="Çalışma kaydına yazılacak dakikayı buradan ayarlayabilirsiniz.")
        
        if st.button("Bitir & Kaydet", use_container_width=True, key="save_time_log_btn"):
            if selected_proj and task_desc:
                proj_id = next((p['id'] for p in data["projects"] if p['name'] == selected_proj), None)
                data.setdefault("time_logs", []).append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "project_id": proj_id,
                    "task": task_desc,
                    "duration": int(duration_mins)
                })
                save_data(data)
                st.success("Çalışma süresi kaydedildi!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.warning("Lütfen proje ve açıklama alanlarını doldurun.")

    with col2:
        st.markdown('### 📊 Son Çalışma Kayıtları')
        if "time_logs" in data and data["time_logs"]:
            st.markdown("**Çalışma Kayıtları:**")
            for idx, log in enumerate(reversed(data["time_logs"])):
                p_name = next((p['name'] for p in data["projects"] if p['id'] == log['project_id']), "Bilinmeyen")
                
                # Column structure to separate card and the delete button
                item_col, del_col = st.columns([5, 1])
                
                with item_col:
                    st.markdown(clean_html(f"""
                    <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; border-left: 3px solid #f59e0b; height: 100%;">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="font-weight: 600; color: white;">{log['task']}</span>
                            <span style="color: #f59e0b; font-weight: bold; margin-right: 10px;">{log['duration']} Dk</span>
                        </div>
                        <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">{p_name} | {log['date']}</div>
                    </div>
                    """), unsafe_allow_html=True)
                
                with del_col:
                    st.write("")  # small spacer
                    # Unique delete button key incorporating index and time data to avoid streamlit duplicated keys
                    if st.button("🗑️", key=f"del_log_{idx}_{log['date']}_{log.get('duration', 25)}", help="Kaydı Sil", use_container_width=True):
                        # Safely delete match from list
                        data["time_logs"] = [l for l in data["time_logs"] if not (l["date"] == log["date"] and l["task"] == log["task"] and l["project_id"] == log["project_id"] and l.get("duration") == log.get("duration"))]
                        save_data(data)
                        st.toast("Çalışma kaydı silindi!", icon="🗑️")
                        st.rerun()
        else:
            st.info("Henüz kaydedilmiş bir çalışma süresi yok.")
