"""
╔═══════════════════════════════════════════════════════════════╗
║  AI 3D EXAM PLATFORM                                         ║
║  منصة امتحان Prompt Engineering & AI-Driven Development    ║
║  DEVELOPPINI - Formation Agentic AI                          ║
╚═══════════════════════════════════════════════════════════════╝
"""

import site
import sys
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)

import streamlit as st
import numpy as np
import trimesh
import json
import time
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from components.scoring_engine import PromptScorer, TaskGenerator
from components.prompt_processor import PromptProcessor
from components.mesh_generator import ImageTo3D
from components.exporters import ModelExporter

st.set_page_config(
    page_title="AI 3D Exam | DEVELOPPINI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    :root {
        --primary: #6366f1;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --info: #3b82f6;
        --dark: #0f172a;
        --card: #1e293b;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    h1 {
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        text-align: center;
        font-size: 2.5rem !important;
        margin-bottom: 5px !important;
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 30px;
    }
    .exam-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .timer-box {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        font-family: monospace;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }
    .score-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
    }
    .score-box h2 {
        font-size: 3rem;
        margin: 0;
        color: white !important;
    }
    .grade-a { background: linear-gradient(135deg, #10b981, #34d399) !important; }
    .grade-b { background: linear-gradient(135deg, #3b82f6, #60a5fa) !important; }
    .grade-c { background: linear-gradient(135deg, #f59e0b, #fbbf24) !important; }
    .grade-d { background: linear-gradient(135deg, #ef4444, #f87171) !important; }
    .grade-f { background: linear-gradient(135deg, #7c2d12, #9a3412) !important; }
    .criteria-bar {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px 15px;
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        width: 100%;
        transition: all 0.3s !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5) !important;
    }
    .prompt-area textarea {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 2px solid rgba(99, 102, 241, 0.5) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
    }
    .stTextInput > div > div > input {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 2px solid rgba(99, 102, 241, 0.5) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    .task-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .diff-easy { background: #10b981; color: white; }
    .diff-medium { background: #f59e0b; color: white; }
    .diff-hard { background: #ef4444; color: white; }
    .leaderboard-row {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 10px;
        padding: 12px 20px;
        margin: 5px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 4px solid #6366f1;
    }
    .rank-1 { border-left-color: #fbbf24 !important; background: rgba(251, 191, 36, 0.1) !important; }
    .rank-2 { border-left-color: #94a3b8 !important; background: rgba(148, 163, 184, 0.1) !important; }
    .rank-3 { border-left-color: #b45309 !important; background: rgba(180, 83, 9, 0.1) !important; }
    .feedback-item {
        padding: 8px 15px;
        margin: 5px 0;
        border-radius: 8px;
        font-size: 0.95rem;
    }
    .fb-success { background: rgba(16, 185, 129, 0.15); color: #34d399; }
    .fb-warning { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
    .fb-error { background: rgba(239, 68, 68, 0.15); color: #f87171; }
</style>
""", unsafe_allow_html=True)

def init_session():
    defaults = {
        'student_name': '',
        'exam_started': False,
        'exam_finished': False,
        'current_task': None,
        'start_time': None,
        'time_remaining': 0,
        'mesh': None,
        'prompts_history': [],
        'scores_history': [],
        'current_score': None,
        'task_results': [],
        'admin_view': False,
        'all_students': []
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

def get_threejs_viewer(mesh, height=500):
    if mesh is None:
        return "<div style='text-align:center;padding:50px;color:#666;'>لا يوجد نموذج</div>"
    vertices = mesh.vertices.tolist()
    faces = mesh.faces.tolist()
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8">
    <style>body{{margin:0;overflow:hidden;background:#0f172a;}}#c{{width:100%;height:{height}px;}}</style>
    </head>
    <body>
    <div id="c"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
    let s=new THREE.Scene();s.background=new THREE.Color(0x0f172a);
    let c=new THREE.PerspectiveCamera(45,1,0.1,1000);
    c.position.set(60,50,60);
    let r=new THREE.WebGLRenderer({{antialias:true}});
    r.setSize(document.getElementById('c').clientWidth,{height});
    document.getElementById('c').appendChild(r.domElement);
    let ctrl=new THREE.OrbitControls(c,r.domElement);
    ctrl.enableDamping=true;
    s.add(new THREE.AmbientLight(0x404040,2));
    let d=new THREE.DirectionalLight(0xffffff,1.5);
    d.position.set(50,100,50);s.add(d);
    s.add(new THREE.PointLight(0x6366f1,1,100).position.set(-50,50,-50));
    s.add(new THREE.PointLight(0xec4899,1,100).position.set(50,-50,50));
    let g=new THREE.BufferGeometry();
    let v={json.dumps(vertices)};let f={json.dumps(faces)};
    let p=[];
    for(let i=0;i<f.length;i++){{
        let fa=f[i];
        p.push(v[fa[0]][0],v[fa[0]][1],v[fa[0]][2],v[fa[1]][0],v[fa[1]][1],v[fa[1]][2],v[fa[2]][0],v[fa[2]][1],v[fa[2]][2]);
    }}
    g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));
    g.computeVertexNormals();
    let m=new THREE.Mesh(g,new THREE.MeshPhongMaterial({{color:0x6366f1,shininess:100,side:THREE.DoubleSide}}));
    let grp=new THREE.Group();grp.add(m);
    g.computeBoundingBox();let cen=new THREE.Vector3();g.boundingBox.getCenter(cen);
    grp.position.sub(cen);s.add(grp);
    s.add(new THREE.GridHelper(150,15,0x6366f1,0x1e293b));
    s.add(new THREE.AxesHelper(40));
    function anim(){{requestAnimationFrame(anim);ctrl.update();r.render(s,c);}}
    anim();
    window.addEventListener('resize',()=>{{c.aspect=document.getElementById('c').clientWidth/{height};c.updateProjectionMatrix();r.setSize(document.getElementById('c').clientWidth,{height});}});
    </script>
    </body>
    </html>
    """
    return html

def show_login():
    st.markdown("""
    <div style="text-align:center; padding: 40px 0;">
        <h1>🎓 AI 3D Exam Platform</h1>
        <p class="subtitle">منصة تقييم مهارات Prompt Engineering & AI-Driven Development</p>
        <p style="color:#6366f1; font-size:0.9rem;">DEVELOPPINI - Formation Agentic AI</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 👤 تسجيل الدخول للامتحان")
        name = st.text_input("الاسم الكامل", placeholder="مثال: أحمد بن علي", key="login_name")

        st.markdown("### 📋 اختيار المهمة")
        task_gen = TaskGenerator()
        tasks = task_gen.get_all_tasks()
        task_options = [f"{t['id']}. {t['title']} ({t['difficulty']})" for t in tasks]
        selected = st.selectbox("اختر المهمة", task_options)
        task_id = int(selected.split('.')[0])

        task = task_gen.get_task(task_id)
        diff_class = f"diff-{task['difficulty']}"
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:12px; margin:15px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <strong style="color:#e2e8f0;">{task['title']}</strong>
                <span class="task-badge {diff_class}">{task['difficulty']}</span>
            </div>
            <p style="color:#94a3b8; margin:0;">{task['description']}</p>
            <div style="margin-top:10px;">
                <strong style="color:#6366f1;">المتطلبات:</strong>
                <ul style="color:#94a3b8; margin:5px 0;">
                    {''.join([f'<li>{req}</li>' for req in task['requirements']])}
                </ul>
            </div>
            <div style="color:#f59e0b; font-size:0.9rem;">⏱️ الوقت المحدد: {task['time_limit']//60} دقيقة</div>
        </div>
        """, unsafe_allow_html=True)

        admin_code = st.text_input("🔐 كود المشرف (اختياري)", type="password", key="admin_code")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 بدء الامتحان", key="start_exam"):
                if name.strip():
                    st.session_state.student_name = name
                    st.session_state.current_task = task
                    st.session_state.exam_started = True
                    st.session_state.start_time = time.time()
                    st.session_state.time_remaining = task['time_limit']
                    st.session_state.prompts_history = []
                    st.session_state.scores_history = []
                    st.session_state.mesh = None
                    st.rerun()
                else:
                    st.error("❌ يرجى إدخال الاسم")
        with col_btn2:
            if st.button("📊 لوحة المشرف", key="admin_panel"):
                if admin_code == "dev2024":
                    st.session_state.admin_view = True
                    st.rerun()
                elif admin_code:
                    st.error("❌ كود خاطئ")
        st.markdown("</div>", unsafe_allow_html=True)

def show_exam():
    task = st.session_state.current_task
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; padding:15px 0; border-bottom:1px solid rgba(255,255,255,0.1); margin-bottom:20px;">
        <div>
            <h3 style="margin:0; color:#e2e8f0;">👤 {st.session_state.student_name}</h3>
            <p style="margin:0; color:#94a3b8; font-size:0.9rem;">المهمة: {task['title']}</p>
        </div>
        <div class="timer-box" id="timer">
            {st.session_state.time_remaining // 60:02d}:{st.session_state.time_remaining % 60:02d}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.exam_started and not st.session_state.exam_finished:
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, task['time_limit'] - elapsed)
        st.session_state.time_remaining = remaining
        if remaining <= 0:
            st.session_state.exam_finished = True
            st.warning("⏰ انتهى الوقت!")
            st.rerun()

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 📝 منطقة الأوامر (Prompt Area)")
        st.markdown("<p style='color:#94a3b8; font-size:0.9rem;'>اكتب وصفاً دقيقاً للنموذج ثلاثي الأبعاد</p>", unsafe_allow_html=True)

        prompt = st.text_area("", placeholder="مثال: مكعب طول 50 وعرض 30 وارتفاع 20 ملم، حواف منحنية radius 2 ملم", height=120, key="exam_prompt", label_visibility="collapsed")

        st.markdown("### ⚡ بارامترات سريعة")
        c1, c2, c3 = st.columns(3)
        with c1:
            quick_scale = st.slider("Scale", 0.5, 3.0, 1.0, 0.1, key="qs")
        with c2:
            quick_rot = st.slider("Rotate Y", 0, 360, 0, 5, key="qr")
        with c3:
            quick_smooth = st.checkbox("Smooth", key="qsm")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("▶️ تنفيذ الأمر", key="execute"):
                if prompt.strip():
                    with st.spinner("جاري المعالجة..."):
                        st.session_state.prompts_history.append({'prompt': prompt, 'time': time.time() - st.session_state.start_time})
                        processor = PromptProcessor()
                        mesh = processor.generate_from_description(prompt)
                        if quick_scale != 1.0:
                            mesh.apply_scale([quick_scale]*3)
                        if quick_rot != 0:
                            mesh.apply_transform(trimesh.transformations.rotation_matrix(np.radians(quick_rot), [0, 1, 0]))
                        if quick_smooth:
                            mesh = mesh.smoothed()
                        st.session_state.mesh = mesh
                        scorer = PromptScorer()
                        score = scorer.analyze_prompt(prompt, task['requirements'])
                        st.session_state.current_score = score
                        st.session_state.scores_history.append(score)
                        st.success("✅ تم التنفيذ!")
                else:
                    st.warning("يرجى كتابة أمر أولاً")
        with col_btn2:
            if st.button("🏁 إنهاء الامتحان", key="finish"):
                st.session_state.exam_finished = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.prompts_history:
            st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
            st.markdown("### 📜 سجل الأوامر")
            for i, entry in enumerate(st.session_state.prompts_history, 1):
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:8px; margin:5px 0; border-right:3px solid #6366f1;">
                    <strong style="color:#6366f1;">#{i}</strong> 
                    <span style="color:#e2e8f0;">{entry['prompt'][:80]}...</span>
                    <span style="color:#94a3b8; font-size:0.8rem;">({entry['time']:.0f}s)</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 🎮 المعاينة ثلاثية الأبعاد")
        if st.session_state.mesh is not None:
            html = get_threejs_viewer(st.session_state.mesh, height=400)
            st.components.v1.html(html, height=400, scrolling=False)
            exporter = ModelExporter()
            info = exporter.get_mesh_info(st.session_state.mesh)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("نقاط", info['vertices'])
            c2.metric("وجوه", info['faces'])
            c3.metric("حجم", f"{info['volume']:.1f}")
            c4.metric("مساحة", f"{info['surface_area']:.1f}")
        else:
            st.markdown("""
            <div style="text-align:center; padding:80px 20px; color:#64748b;">
                <div style="font-size:3rem; margin-bottom:15px;">🎨</div>
                <p>اكتب أمراً واضغط "تنفيذ"<br>لرؤية النموذج هنا</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.current_score:
            score = st.session_state.current_score
            grade_class = f"grade-{score['grade'][0].lower()}" if score['grade'][0] in 'ABCDF' else "grade-c"
            st.markdown(f"<div class='exam-card'>", unsafe_allow_html=True)
            st.markdown("### 📊 تقييم الأمر الحالي")
            st.markdown(f"""
            <div class="score-box {grade_class}">
                <div style="font-size:0.9rem; opacity:0.8;">الدرجة</div>
                <h2>{score['total']}/100</h2>
                <div style="font-size:1.2rem; font-weight:bold;">{score['grade']} - {score['level']}</div>
            </div>
            """, unsafe_allow_html=True)

            criteria = [
                ("الدقة", score['scores']['precision'], 25, "#6366f1"),
                ("الكفاءة", score['scores']['efficiency'], 20, "#3b82f6"),
                ("الوضوح", score['scores']['clarity'], 20, "#8b5cf6"),
                ("الاكتمال", score['scores']['completeness'], 20, "#ec4899"),
                ("الإبداع", score['scores']['creativity'], 15, "#10b981")
            ]
            for name, val, max_val, color in criteria:
                pct = (val / max_val) * 100
                st.markdown(f"""
                <div class="criteria-bar">
                    <span style="color:#e2e8f0; width:80px;">{name}</span>
                    <div style="flex:1; background:rgba(255,255,255,0.1); border-radius:4px; margin:0 10px; height:8px;">
                        <div style="width:{pct}%; background:{color}; height:100%; border-radius:4px;"></div>
                    </div>
                    <span style="color:{color}; font-weight:bold; width:50px; text-align:right;">{val}/{max_val}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### 💬 ملاحظات")
            for fb in score['feedback']:
                cls = 'fb-success' if '✅' in fb else ('fb-warning' if '⚠️' in fb else 'fb-error')
                st.markdown(f"<div class='feedback-item {cls}'>{fb}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

def show_results():
    st.markdown("""
    <div style="text-align:center; padding: 30px 0;">
        <h1>🎓 نتائج الامتحان</h1>
        <p class="subtitle">DEVELOPPINI - AI-Driven Developer Assessment</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.scores_history:
        avg_score = sum(s['total'] for s in st.session_state.scores_history) / len(st.session_state.scores_history)
        best_score = max(s['total'] for s in st.session_state.scores_history)
        total_prompts = len(st.session_state.prompts_history)
        total_time = int(time.time() - st.session_state.start_time)

        if avg_score >= 90:
            final_grade = 'A+'; final_level = 'ممتاز - جاهز للتوظيف فوراً'; grade_class = 'grade-a'
        elif avg_score >= 80:
            final_grade = 'A'; final_level = 'جيد جداً - قادر على العمل باستقلالية'; grade_class = 'grade-a'
        elif avg_score >= 70:
            final_grade = 'B'; final_level = 'جيد - يحتاج بعض التوجيه'; grade_class = 'grade-b'
        elif avg_score >= 60:
            final_grade = 'C'; final_level = 'مقبول - يحتاج تدريب إضافي'; grade_class = 'grade-c'
        elif avg_score >= 50:
            final_grade = 'D'; final_level = 'ضعيف - يحتاج مراجعة أساسيات'; grade_class = 'grade-d'
        else:
            final_grade = 'F'; final_level = 'راسب - غير جاهز حالياً'; grade_class = 'grade-f'

        result_data = {
            'name': st.session_state.student_name,
            'task': st.session_state.current_task['title'],
            'avg_score': round(avg_score, 1),
            'best_score': best_score,
            'grade': final_grade,
            'level': final_level,
            'total_prompts': total_prompts,
            'total_time': total_time,
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.all_students.append(result_data)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class="exam-card" style="text-align:center;">
                <div class="score-box {grade_class}">
                    <div style="font-size:1rem; opacity:0.9;">الدرجة النهائية</div>
                    <h2 style="font-size:4rem;">{avg_score:.1f}/100</h2>
                    <div style="font-size:1.5rem; font-weight:bold; margin:10px 0;">{final_grade}</div>
                    <div style="font-size:1rem; opacity:0.9;">{final_level}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 📈 إحصائيات الأداء")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📝 عدد الأوامر", total_prompts)
        c2.metric("⭐ أفضل درجة", f"{best_score}/100")
        c3.metric("⏱️ الوقت", f"{total_time//60}m {total_time%60}s")
        c4.metric("🎯 الكفاءة", f"{best_score/max(total_prompts,1):.1f}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 تفاصيل الأوامر")
        for i, (prompt_entry, score) in enumerate(zip(st.session_state.prompts_history, st.session_state.scores_history), 1):
            with st.expander(f"الأمر #{i} - {score['total']}/100 ({score['grade']})"):
                st.write(f"**الأمر:** {prompt_entry['prompt']}")
                st.write(f"**الوقت:** {prompt_entry['time']:.1f} ثانية")
                st.write(f"**الكلمات:** {score['word_count']}")
                st.write(f"**الأوامر المتقدمة:** {', '.join(score['advanced_commands']) or 'لا يوجد'}")
                cols = st.columns(5)
                metrics = [("الدقة", score['scores']['precision'], 25), ("الكفاءة", score['scores']['efficiency'], 20), ("الوضوح", score['scores']['clarity'], 20), ("الاكتمال", score['scores']['completeness'], 20), ("الإبداع", score['scores']['creativity'], 15)]
                for col, (name, val, max_v) in zip(cols, metrics):
                    col.metric(name, f"{val}/{max_v}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 💡 تقييم المشرف")
        if avg_score >= 85:
            st.success("✅ **الطالب جاهز للتوظيف فوراً كـ AI-Driven Developer**\n\nيملك مهارات عالية في صياغة الأوامر الدقيقة والموجزة، وفهم متطلبات المهام بسرعة، وإنتاج نتائج عملية من المرة الأولى.")
        elif avg_score >= 70:
            st.info("✅ **الطالب يملك إمكانيات جيدة**\n\nيحتاج تدريب عملي 2-4 أسابيع على تحسين دقة الأوامر وتقليل عدد المحاولات واستخدام أوامر أكثر تقدماً.")
        else:
            st.warning("⚠️ **الطالب يحتاج تدريب مكثف**\n\nنقاط الضعف: الأوامر غامضة أو غير مكتملة، يحتاج عدة محاولات للوصول للنتيجة، يجب مراجعة أساسيات Prompt Engineering.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 📤 تصدير التقرير")
        scorer = PromptScorer()
        report = scorer.generate_report(st.session_state.student_name, st.session_state.scores_history)
        st.download_button("⬇️ تحميل التقرير (TXT)", report, file_name=f"report_{st.session_state.student_name.replace(' ', '_')}.txt", mime="text/plain")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("❌ لم يتم إرسال أي أوامر خلال الامتحان")

    if st.button("🔄 امتحان جديد", key="new_exam"):
        for key in ['exam_started', 'exam_finished', 'current_task', 'start_time', 'time_remaining', 'mesh', 'prompts_history', 'scores_history', 'current_score', 'task_results']:
            st.session_state[key] = None if key != 'time_remaining' else 0
        st.session_state.exam_started = False
        st.session_state.exam_finished = False
        st.rerun()

def show_admin():
    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <h1>📊 لوحة المشرف</h1>
        <p class="subtitle">مراقبة أداء الطلاب واختيار الأفضل</p>
    </div>
    """, unsafe_allow_html=True)

    students = st.session_state.all_students
    if students:
        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 📈 إحصائيات الدفعة")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("👥 عدد الطلاب", len(students))
        c2.metric("⭐ متوسط الدفعة", f"{sum(s['avg_score'] for s in students)/len(students):.1f}")
        c3.metric("🥇 الأعلى", max(s['avg_score'] for s in students))
        c4.metric("⏱️ متوسط الوقت", f"{sum(s['total_time'] for s in students)//len(students)//60}m")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 🏆 لوحة المتصدرين")
        sorted_students = sorted(students, key=lambda x: x['avg_score'], reverse=True)
        for i, s in enumerate(sorted_students, 1):
            rank_class = f"rank-{i}" if i <= 3 else ""
            medal = "🥇" if i == 1 else ("🥈" if i == 2 else ("🥉" if i == 3 else f"#{i}"))
            st.markdown(f"""
            <div class="leaderboard-row {rank_class}">
                <div style="display:flex; align-items:center; gap:15px;">
                    <span style="font-size:1.5rem;">{medal}</span>
                    <div>
                        <div style="font-weight:bold; color:#e2e8f0;">{s['name']}</div>
                        <div style="font-size:0.85rem; color:#94a3b8;">{s['task']}</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:1.3rem; font-weight:bold; color:#6366f1;">{s['avg_score']}/100</div>
                    <div style="font-size:0.85rem; color:#94a3b8;">{s['grade']} | {s['total_prompts']} أوامر | {s['total_time']//60}m</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 📊 توزيع الدرجات")
        try:
            import plotly.express as px
            import pandas as pd
            df = pd.DataFrame(students)
            fig = px.bar(df, x='name', y='avg_score', color='grade',
                         color_discrete_map={'A+': '#10b981', 'A': '#34d399', 'B': '#3b82f6', 'C': '#f59e0b', 'D': '#ef4444', 'F': '#7c2d12'},
                         title="درجات الطلاب")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#e2e8f0', xaxis_title="الطالب", yaxis_title="الدرجة")
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.info("مكتبة plotly غير متوفرة للرسم البياني")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 📤 تصدير النتائج")
        try:
            import csv, io
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['الاسم', 'المهمة', 'الدرجة', 'التقدير', 'المستوى', 'عدد الأوامر', 'الوقت', 'التاريخ'])
            for s in sorted_students:
                writer.writerow([s['name'], s['task'], s['avg_score'], s['grade'], s['level'], s['total_prompts'], s['total_time'], s['timestamp']])
            st.download_button("⬇️ تحميل CSV", output.getvalue(), file_name="exam_results.csv", mime="text/csv")
        except:
            st.info("تصدير CSV غير متوفر")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("📝 لا يوجد طلاب قاموا بالامتحان بعد")

    if st.button("🔙 العودة للرئيسية", key="back_home"):
        st.session_state.admin_view = False
        st.rerun()

if st.session_state.admin_view:
    show_admin()
elif st.session_state.exam_finished:
    show_results()
elif st.session_state.exam_started:
    show_exam()
else:
    show_login()

st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:15px; color:#64748b; font-size:0.85rem;">
    🎓 AI 3D Exam Platform | DEVELOPPINI - Formation Agentic AI<br>
    اختبار تقييم مهارات AI-Driven Developer
</div>
""", unsafe_allow_html=True)
