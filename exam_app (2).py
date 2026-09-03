"""
╔═══════════════════════════════════════════════════════════════╗
║  AI 3D EXAM PLATFORM - LITE                                  ║
║  منصة امتحان Prompt Engineering & AI-Driven Development    ║
║  DEVELOPPINI - Formation Agentic AI                          ║
╚═══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import site

# إضافة مسار المستخدم
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)

import streamlit as st
import numpy as np
import trimesh
import json
import time
from datetime import datetime
import re
from typing import Dict, List

# ═══════════════════════════════════════════════════════════════
# المكونات المدمجة
# ═══════════════════════════════════════════════════════════════

class PromptScorer:
    def __init__(self):
        self.criteria = {
            'precision': {'weight': 25, 'description': 'وضوح الأبعاد'},
            'efficiency': {'weight': 20, 'description': 'الكفاءة'},
            'clarity': {'weight': 20, 'description': 'الوضوح'},
            'completeness': {'weight': 20, 'description': 'الاكتمال'},
            'creativity': {'weight': 15, 'description': 'الإبداع'}
        }
        self.advanced_keywords = ['subdivide', 'smooth', 'chamfer', 'fillet', 'pattern', 'mirror', 'boolean', 'extrude', 'revolve', 'loft', 'shell', 'draft', 'sweep', 'helix', 'array']

    def analyze_prompt(self, text, task_requirements):
        text_lower = text.lower()
        scores = {}
        feedback = []
        numbers = re.findall(r'\d+\.?\d*', text)
        units = re.findall(r'\b(mm|cm|m|inch|ft|px|%|x)\b', text_lower)

        # Precision
        if len(numbers) >= 3:
            scores['precision'] = 25; feedback.append("✅ أبعاد دقيقة")
        elif len(numbers) >= 1:
            scores['precision'] = 15; feedback.append("⚠️ بعض الأبعاد موجودة")
        else:
            scores['precision'] = 5; feedback.append("❌ لا يوجد أبعاد رقمية")
        if units: scores['precision'] = min(scores['precision'] + 5, 25)

        # Efficiency
        words = text.split()
        if len(words) <= 10: scores['efficiency'] = 20; feedback.append("✅ أمر موجز")
        elif len(words) <= 20: scores['efficiency'] = 15; feedback.append("⚠️ أمر مقبول")
        elif len(words) <= 35: scores['efficiency'] = 10; feedback.append("⚠️ أمر طويل")
        else: scores['efficiency'] = 5; feedback.append("❌ أمر مُبالغ في طوله")

        # Clarity
        vague = ['شيء', 'حاجة', 'كذا', 'يعني', 'مثلا', 'something', 'thing', 'etc']
        vague_count = sum(1 for w in vague if w in text_lower)
        if vague_count == 0 and len(words) > 5: scores['clarity'] = 20; feedback.append("✅ واضح تماماً")
        elif vague_count <= 1: scores['clarity'] = 15; feedback.append("⚠️ وضوح جيد")
        elif vague_count <= 3: scores['clarity'] = 10; feedback.append("⚠️ بعض الغموض")
        else: scores['clarity'] = 5; feedback.append("❌ أمر غامض")

        # Completeness
        covered = sum(1 for req in task_requirements if any(kw in text_lower for kw in req.lower().split()))
        coverage = covered / len(task_requirements) if task_requirements else 1.0
        scores['completeness'] = int(coverage * 20)
        if coverage >= 0.8: feedback.append("✅ جميع المتطلبات مغطاة")
        elif coverage >= 0.5: feedback.append("⚠️ معظم المتطلبات مغطاة")
        else: feedback.append("❌ متطلبات ناقصة")

        # Creativity
        advanced = [kw for kw in self.advanced_keywords if kw in text_lower]
        if len(advanced) >= 2: scores['creativity'] = 15; feedback.append(f"✅ أوامر متقدمة: {', '.join(advanced)}")
        elif len(advanced) == 1: scores['creativity'] = 10; feedback.append(f"✅ أمر متقدم: {advanced[0]}")
        else: scores['creativity'] = 5; feedback.append("⚠️ لا يوجد أوامر متقدمة")

        total = sum(scores.values())
        if total >= 90: grade, level = 'A+', 'ممتاز - جاهز للتوظيف فوراً'
        elif total >= 80: grade, level = 'A', 'جيد جداً - قادر على العمل باستقلالية'
        elif total >= 70: grade, level = 'B', 'جيد - يحتاج بعض التوجيه'
        elif total >= 60: grade, level = 'C', 'مقبول - يحتاج تدريب إضافي'
        elif total >= 50: grade, level = 'D', 'ضعيف - يحتاج مراجعة أساسيات'
        else: grade, level = 'F', 'راسب - غير جاهز حالياً'

        return {'scores': scores, 'total': total, 'grade': grade, 'level': level, 'feedback': feedback, 'word_count': len(words), 'numbers_found': len(numbers), 'advanced_commands': advanced, 'coverage': coverage, 'timestamp': datetime.now().isoformat()}

    def generate_report(self, name, results):
        avg = sum(s['total'] for s in results) / len(results) if results else 0
        report = f"""تقرير تقييم: {name}\n{'='*50}\nالمتوسط: {avg:.1f}/100\n\n"""
        for i, res in enumerate(results, 1):
            report += f"الأمر #{i}: {res['total']}/100 ({res['grade']})\n"
            for fb in res['feedback']: report += f"  {fb}\n"
            report += "\n"
        if avg >= 85: report += "✅ جاهز للتوظيف"
        elif avg >= 70: report += "✅ إمكانيات جيدة"
        else: report += "⚠️ يحتاج تدريب"
        return report

class TaskGenerator:
    TASKS = [
        {'id': 1, 'title': 'تصميم غلاف هاتف', 'description': 'صمم غلافاً ثلاثي الأبعاد لهاتف iPhone 15 Pro Max', 'requirements': ['أبعاد 159.9 x 76.7 x 8.25 ملم', 'فتحة كاميرا ثلاثية', 'سمك 1.5 ملم', 'حواف منحنية'], 'difficulty': 'متوسط', 'time_limit': 300},
        {'id': 2, 'title': 'تصميم حامل كوب', 'description': 'صمم حامل كوب مكتبي أنيق', 'requirements': ['قطر داخلي 85 ملم', 'ارتفاع 120 ملم', 'قاعدة مستقرة', 'تصميم مفتوح'], 'difficulty': 'سهل', 'time_limit': 180},
        {'id': 3, 'title': 'تصميم ترس ميكانيكي', 'description': 'صمم ترساً ميكانيكياً', 'requirements': ['قطر خارجي 50 ملم', '20 سن', 'ثقب مركزي قطر 8 ملم', 'سمك 5 ملم'], 'difficulty': 'صعب', 'time_limit': 420},
        {'id': 4, 'title': 'تصميم قالب طباعة 3D', 'description': 'صمم قالباً لطباعة مجسم ديكوري', 'requirements': ['أبعاد 100x100x50 ملم', 'تفاصيل نقوش دقيقة', 'جدران سمك 2 ملم', 'قاعدة مسطحة'], 'difficulty': 'صعب', 'time_limit': 600},
        {'id': 5, 'title': 'تصميم مجسم معماري', 'description': 'صمم نموذجاً مبسطاً لبرج مائل', 'requirements': ['ارتفاع 200 ملم', 'انحراف 15 درجة', 'قاعدة مربعة 50x50 ملم', 'تفاصيل نوافذ'], 'difficulty': 'متوسط', 'time_limit': 360}
    ]
    def get_task(self, task_id=None, difficulty=None):
        import random
        if task_id:
            for t in self.TASKS:
                if t['id'] == task_id: return t
        if difficulty:
            tasks = [t for t in self.TASKS if t['difficulty'] == difficulty]
            if tasks: return random.choice(tasks)
        return random.choice(self.TASKS)
    def get_all_tasks(self): return self.TASKS

class PromptProcessor:
    def __init__(self):
        self.commands = {
            'scale': ['كبر', 'صغر', 'حجم', 'scale', 'resize'],
            'rotate': ['دور', 'لف', 'rotate', 'turn'],
            'translate': ['حرك', 'نقل', 'move', 'translate'],
            'extrude': ['بعد', 'اكسترود', 'extrude', 'height'],
            'color': ['لون', 'صبغ', 'color', 'paint'],
            'mirror': ['عكس', 'mirror', 'flip'],
            'smooth': ['نعم', 'smooth', 'refine'],
            'chamfer': ['شطف', 'chamfer', 'bevel'],
            'fillet': ['دائر', 'fillet', 'round'],
            'hole': ['ثقب', 'hole', 'drill']
        }
    def generate_from_description(self, text):
        text = text.lower()
        nums = re.findall(r'\d+\.?\d*', text)
        if any(w in text for w in ['مكعب', 'cube', 'صندوق', 'box']):
            size = float(nums[0]) if nums else 10
            return trimesh.creation.box(extents=[size, size, size])
        elif any(w in text for w in ['كرة', 'sphere', 'دائرة', 'ball']):
            r = float(nums[0]) if nums else 5
            return trimesh.creation.icosphere(radius=r)
        elif any(w in text for w in ['أسطوانة', 'cylinder', 'عمود']):
            r = float(nums[0]) if len(nums) > 0 else 5
            h = float(nums[1]) if len(nums) > 1 else 20
            return trimesh.creation.cylinder(radius=r, height=h)
        elif any(w in text for w in ['مخروط', 'cone']):
            r = float(nums[0]) if len(nums) > 0 else 5
            h = float(nums[1]) if len(nums) > 1 else 20
            return trimesh.creation.cone(radius=r, height=h)
        elif any(w in text for w in ['طارة', 'torus', 'حلقة']):
            R = float(nums[0]) if len(nums) > 0 else 10
            r = float(nums[1]) if len(nums) > 1 else 2
            return trimesh.creation.torus(major_radius=R, minor_radius=r)
        else:
            return trimesh.creation.box(extents=[10, 10, 10])

class ModelExporter:
    def get_mesh_info(self, mesh):
        bounds = mesh.bounds
        return {
            'vertices': len(mesh.vertices), 'faces': len(mesh.faces),
            'volume': float(mesh.volume) if mesh.is_watertight else 0.0,
            'surface_area': float(mesh.area),
            'bounds': bounds.tolist(),
            'dimensions': (bounds[1] - bounds[0]).tolist(),
            'is_watertight': mesh.is_watertight
        }

# ═══════════════════════════════════════════════════════════════
# Streamlit App
# ═══════════════════════════════════════════════════════════════

st.set_page_config(page_title="AI 3D Exam | DEVELOPPINI", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); }
h1 { background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900 !important; text-align: center; font-size: 2.5rem !important; }
.subtitle { text-align: center; color: #94a3b8; font-size: 1rem; margin-bottom: 30px; }
.exam-card { background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 16px; padding: 25px; margin: 15px 0; }
.timer-box { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; padding: 15px; border-radius: 12px; text-align: center; font-size: 2rem; font-weight: bold; font-family: monospace; }
.score-box { background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 20px; border-radius: 16px; text-align: center; }
.score-box h2 { font-size: 3rem; margin: 0; color: white !important; }
.grade-a { background: linear-gradient(135deg, #10b981, #34d399) !important; }
.grade-b { background: linear-gradient(135deg, #3b82f6, #60a5fa) !important; }
.grade-c { background: linear-gradient(135deg, #f59e0b, #fbbf24) !important; }
.grade-d { background: linear-gradient(135deg, #ef4444, #f87171) !important; }
.grade-f { background: linear-gradient(135deg, #7c2d12, #9a3412) !important; }
.criteria-bar { background: rgba(255,255,255,0.05); border-radius: 10px; padding: 10px 15px; margin: 8px 0; display: flex; justify-content: space-between; align-items: center; }
.stButton > button { background: linear-gradient(135deg, #6366f1, #8b5cf6) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 12px 30px !important; font-weight: 700 !important; width: 100%; }
.prompt-area textarea { background: rgba(15, 23, 42, 0.9) !important; border: 2px solid rgba(99, 102, 241, 0.5) !important; border-radius: 12px !important; color: #e2e8f0 !important; font-family: monospace !important; font-size: 1.1rem !important; }
.task-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
.diff-easy { background: #10b981; color: white; }
.diff-medium { background: #f59e0b; color: white; }
.diff-hard { background: #ef4444; color: white; }
.leaderboard-row { background: rgba(30, 41, 59, 0.6); border-radius: 10px; padding: 12px 20px; margin: 5px 0; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid #6366f1; }
.rank-1 { border-left-color: #fbbf24 !important; background: rgba(251, 191, 36, 0.1) !important; }
.rank-2 { border-left-color: #94a3b8 !important; background: rgba(148, 163, 184, 0.1) !important; }
.rank-3 { border-left-color: #b45309 !important; background: rgba(180, 83, 9, 0.1) !important; }
.feedback-item { padding: 8px 15px; margin: 5px 0; border-radius: 8px; font-size: 0.95rem; }
.fb-success { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.fb-warning { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
.fb-error { background: rgba(239, 68, 68, 0.15); color: #f87171; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# Session State
# ═══════════════════════════════════════════════════════════════
def init_session():
    defaults = {'student_name': '', 'exam_started': False, 'exam_finished': False, 'current_task': None, 'start_time': None, 'time_remaining': 0, 'mesh': None, 'prompts_history': [], 'scores_history': [], 'current_score': None, 'all_students': [], 'admin_view': False}
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v
init_session()

# ═══════════════════════════════════════════════════════════════
# 3D Viewer (Three.js)
# ═══════════════════════════════════════════════════════════════
def get_threejs_viewer(mesh, height=500):
    if mesh is None:
        return "<div style='text-align:center;padding:80px;color:#64748b;'><div style='font-size:3rem;'>🎨</div><p>اكتب أمراً واضغط تنفيذ</p></div>"
    vertices = json.dumps(mesh.vertices.tolist())
    faces = json.dumps(mesh.faces.tolist())
    return f"""
    <!DOCTYPE html><html><head><meta charset="utf-8"><style>body{{margin:0;overflow:hidden;background:#0f172a;}}#c{{width:100%;height:{height}px;}}</style></head>
    <body><div id="c"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
    let s=new THREE.Scene();s.background=new THREE.Color(0x0f172a);
    let c=new THREE.PerspectiveCamera(45,1,0.1,1000);c.position.set(60,50,60);
    let r=new THREE.WebGLRenderer({{antialias:true}});r.setSize(document.getElementById('c').clientWidth,{height});document.getElementById('c').appendChild(r.domElement);
    let ctrl=new THREE.OrbitControls(c,r.domElement);ctrl.enableDamping=true;
    s.add(new THREE.AmbientLight(0x404040,2));
    let d=new THREE.DirectionalLight(0xffffff,1.5);d.position.set(50,100,50);s.add(d);
    s.add(new THREE.PointLight(0x6366f1,1,100).position.set(-50,50,-50));
    s.add(new THREE.PointLight(0xec4899,1,100).position.set(50,-50,50));
    let g=new THREE.BufferGeometry();
    let v={vertices};let f={faces};let p=[];
    for(let i=0;i<f.length;i++){{let fa=f[i];p.push(v[fa[0]][0],v[fa[0]][1],v[fa[0]][2],v[fa[1]][0],v[fa[1]][1],v[fa[1]][2],v[fa[2]][0],v[fa[2]][1],v[fa[2]][2]);}}
    g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));g.computeVertexNormals();
    let m=new THREE.Mesh(g,new THREE.MeshPhongMaterial({{color:0x6366f1,shininess:100,side:THREE.DoubleSide}}));
    let grp=new THREE.Group();grp.add(m);g.computeBoundingBox();let cen=new THREE.Vector3();g.boundingBox.getCenter(cen);grp.position.sub(cen);s.add(grp);
    s.add(new THREE.GridHelper(150,15,0x6366f1,0x1e293b));s.add(new THREE.AxesHelper(40));
    function anim(){{requestAnimationFrame(anim);ctrl.update();r.render(s,c);}}anim();
    window.addEventListener('resize',()=>{{c.aspect=document.getElementById('c').clientWidth/{height};c.updateProjectionMatrix();r.setSize(document.getElementById('c').clientWidth,{height});}});
    </script></body></html>
    """

# ═══════════════════════════════════════════════════════════════
# Pages
# ═══════════════════════════════════════════════════════════════

def show_login():
    st.markdown("<div style='text-align:center;padding:40px 0;'><h1>🎓 AI 3D Exam Platform</h1><p class='subtitle'>منصة تقييم مهارات Prompt Engineering & AI-Driven Development</p><p style='color:#6366f1;font-size:0.9rem;'>DEVELOPPINI - Formation Agentic AI</p></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 👤 تسجيل الدخول")
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
        <div style="background:rgba(255,255,255,0.05);padding:15px;border-radius:12px;margin:15px 0;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <strong style="color:#e2e8f0;">{task['title']}</strong>
                <span class="task-badge {diff_class}">{task['difficulty']}</span>
            </div>
            <p style="color:#94a3b8;margin:0;">{task['description']}</p>
            <div style="margin-top:10px;"><strong style="color:#6366f1;">المتطلبات:</strong><ul style="color:#94a3b8;margin:5px 0;">{''.join([f'<li>{req}</li>' for req in task['requirements']])}</ul></div>
            <div style="color:#f59e0b;font-size:0.9rem;">⏱️ الوقت: {task['time_limit']//60} دقيقة</div>
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
                else: st.error("❌ يرجى إدخال الاسم")
        with col_btn2:
            if st.button("📊 لوحة المشرف", key="admin_panel"):
                if admin_code == "dev2024":
                    st.session_state.admin_view = True
                    st.rerun()
                elif admin_code: st.error("❌ كود خاطئ")
        st.markdown("</div>", unsafe_allow_html=True)

def show_exam():
    task = st.session_state.current_task
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;padding:15px 0;border-bottom:1px solid rgba(255,255,255,0.1);margin-bottom:20px;">
        <div><h3 style="margin:0;color:#e2e8f0;">👤 {st.session_state.student_name}</h3><p style="margin:0;color:#94a3b8;font-size:0.9rem;">المهمة: {task['title']}</p></div>
        <div class="timer-box">{st.session_state.time_remaining // 60:02d}:{st.session_state.time_remaining % 60:02d}</div>
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
        st.markdown("<p style='color:#94a3b8;font-size:0.9rem;'>اكتب وصفاً دقيقاً للنموذج ثلاثي الأبعاد</p>", unsafe_allow_html=True)
        prompt = st.text_area("", placeholder="مثال: مكعب طول 50 وعرض 30 وارتفاع 20 ملم، حواف منحنية radius 2 ملم", height=120, key="exam_prompt", label_visibility="collapsed")
        st.markdown("### ⚡ بارامترات سريعة")
        c1, c2, c3 = st.columns(3)
        with c1: quick_scale = st.slider("Scale", 0.5, 3.0, 1.0, 0.1, key="qs")
        with c2: quick_rot = st.slider("Rotate Y", 0, 360, 0, 5, key="qr")
        with c3: quick_smooth = st.checkbox("Smooth", key="qsm")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("▶️ تنفيذ الأمر", key="execute"):
                if prompt.strip():
                    with st.spinner("جاري المعالجة..."):
                        st.session_state.prompts_history.append({'prompt': prompt, 'time': time.time() - st.session_state.start_time})
                        processor = PromptProcessor()
                        mesh = processor.generate_from_description(prompt)
                        if quick_scale != 1.0: mesh.apply_scale([quick_scale]*3)
                        if quick_rot != 0: mesh.apply_transform(trimesh.transformations.rotation_matrix(np.radians(quick_rot), [0, 1, 0]))
                        if quick_smooth: mesh = mesh.smoothed()
                        st.session_state.mesh = mesh
                        scorer = PromptScorer()
                        score = scorer.analyze_prompt(prompt, task['requirements'])
                        st.session_state.current_score = score
                        st.session_state.scores_history.append(score)
                        st.success("✅ تم التنفيذ!")
                else: st.warning("يرجى كتابة أمر أولاً")
        with col_btn2:
            if st.button("🏁 إنهاء الامتحان", key="finish"):
                st.session_state.exam_finished = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.prompts_history:
            st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
            st.markdown("### 📜 سجل الأوامر")
            for i, entry in enumerate(st.session_state.prompts_history, 1):
                st.markdown(f"<div style='background:rgba(255,255,255,0.03);padding:10px;border-radius:8px;margin:5px 0;border-right:3px solid #6366f1;'><strong style='color:#6366f1;'>#{i}</strong> <span style='color:#e2e8f0;'>{entry['prompt'][:80]}...</span> <span style='color:#94a3b8;font-size:0.8rem;'>({entry['time']:.0f}s)</span></div>", unsafe_allow_html=True)
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
            st.markdown("<div style='text-align:center;padding:80px 20px;color:#64748b;'><div style='font-size:3rem;margin-bottom:15px;'>🎨</div><p>اكتب أمراً واضغط 'تنفيذ'<br>لرؤية النموذج هنا</p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.current_score:
            score = st.session_state.current_score
            grade_class = f"grade-{score['grade'][0].lower()}" if score['grade'][0] in 'ABCDF' else "grade-c"
            st.markdown(f"<div class='exam-card'>", unsafe_allow_html=True)
            st.markdown("### 📊 تقييم الأمر الحالي")
            st.markdown(f"<div class='score-box {grade_class}'><div style='font-size:0.9rem;opacity:0.8;'>الدرجة</div><h2>{score['total']}/100</h2><div style='font-size:1.2rem;font-weight:bold;'>{score['grade']} - {score['level']}</div></div>", unsafe_allow_html=True)
            criteria = [("الدقة", score['scores']['precision'], 25, "#6366f1"), ("الكفاءة", score['scores']['efficiency'], 20, "#3b82f6"), ("الوضوح", score['scores']['clarity'], 20, "#8b5cf6"), ("الاكتمال", score['scores']['completeness'], 20, "#ec4899"), ("الإبداع", score['scores']['creativity'], 15, "#10b981")]
            for name, val, max_val, color in criteria:
                pct = (val / max_val) * 100
                st.markdown(f"<div class='criteria-bar'><span style='color:#e2e8f0;width:80px;'>{name}</span><div style='flex:1;background:rgba(255,255,255,0.1);border-radius:4px;margin:0 10px;height:8px;'><div style='width:{pct}%;background:{color};height:100%;border-radius:4px;'></div></div><span style='color:{color};font-weight:bold;width:50px;text-align:right;'>{val}/{max_val}</span></div>", unsafe_allow_html=True)
            st.markdown("#### 💬 ملاحظات")
            for fb in score['feedback']:
                cls = 'fb-success' if '✅' in fb else ('fb-warning' if '⚠️' in fb else 'fb-error')
                st.markdown(f"<div class='feedback-item {cls}'>{fb}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

def show_results():
    st.markdown("<div style='text-align:center;padding:30px 0;'><h1>🎓 نتائج الامتحان</h1><p class='subtitle'>DEVELOPPINI - AI-Driven Developer Assessment</p></div>", unsafe_allow_html=True)
    if st.session_state.scores_history:
        avg_score = sum(s['total'] for s in st.session_state.scores_history) / len(st.session_state.scores_history)
        best_score = max(s['total'] for s in st.session_state.scores_history)
        total_prompts = len(st.session_state.prompts_history)
        total_time = int(time.time() - st.session_state.start_time)
        if avg_score >= 90: final_grade, final_level, grade_class = 'A+', 'ممتاز - جاهز للتوظيف فوراً', 'grade-a'
        elif avg_score >= 80: final_grade, final_level, grade_class = 'A', 'جيد جداً - قادر على العمل باستقلالية', 'grade-a'
        elif avg_score >= 70: final_grade, final_level, grade_class = 'B', 'جيد - يحتاج بعض التوجيه', 'grade-b'
        elif avg_score >= 60: final_grade, final_level, grade_class = 'C', 'مقبول - يحتاج تدريب إضافي', 'grade-c'
        elif avg_score >= 50: final_grade, final_level, grade_class = 'D', 'ضعيف - يحتاج مراجعة أساسيات', 'grade-d'
        else: final_grade, final_level, grade_class = 'F', 'راسب - غير جاهز حالياً', 'grade-f'
        result_data = {'name': st.session_state.student_name, 'task': st.session_state.current_task['title'], 'avg_score': round(avg_score, 1), 'best_score': best_score, 'grade': final_grade, 'level': final_level, 'total_prompts': total_prompts, 'total_time': total_time, 'timestamp': datetime.now().isoformat()}
        st.session_state.all_students.append(result_data)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"<div class='exam-card' style='text-align:center;'><div class='score-box {grade_class}'><div style='font-size:1rem;opacity:0.9;'>الدرجة النهائية</div><h2 style='font-size:4rem;'>{avg_score:.1f}/100</h2><div style='font-size:1.5rem;font-weight:bold;margin:10px 0;'>{final_grade}</div><div style='font-size:1rem;opacity:0.9;'>{final_level}</div></div></div>", unsafe_allow_html=True)
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
                cols = st.columns(5)
                metrics = [("الدقة", score['scores']['precision'], 25), ("الكفاءة", score['scores']['efficiency'], 20), ("الوضوح", score['scores']['clarity'], 20), ("الاكتمال", score['scores']['completeness'], 20), ("الإبداع", score['scores']['creativity'], 15)]
                for col, (name, val, max_v) in zip(cols, metrics):
                    col.metric(name, f"{val}/{max_v}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 💡 تقييم المشرف")
        if avg_score >= 85: st.success("✅ **الطالب جاهز للتوظيف فوراً كـ AI-Driven Developer**")
        elif avg_score >= 70: st.info("✅ **الطالب يملك إمكانيات جيدة** - يحتاج تدريب 2-4 أسابيع")
        else: st.warning("⚠️ **الطالب يحتاج تدريب مكثف** - مراجعة أساسيات Prompt Engineering")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='exam-card'>", unsafe_allow_html=True)
        st.markdown("### 📤 تصدير التقرير")
        scorer = PromptScorer()
        report = scorer.generate_report(st.session_state.student_name, st.session_state.scores_history)
        st.download_button("⬇️ تحميل التقرير (TXT)", report, file_name=f"report_{st.session_state.student_name.replace(' ', '_')}.txt", mime="text/plain")
        st.markdown("</div>", unsafe_allow_html=True)
    else: st.error("❌ لم يتم إرسال أي أوامر")
    if st.button("🔄 امتحان جديد", key="new_exam"):
        for key in ['exam_started', 'exam_finished', 'current_task', 'start_time', 'time_remaining', 'mesh', 'prompts_history', 'scores_history', 'current_score']:
            st.session_state[key] = None if key != 'time_remaining' else 0
        st.session_state.exam_started = False
        st.session_state.exam_finished = False
        st.rerun()

def show_admin():
    st.markdown("<div style='text-align:center;padding:20px 0;'><h1>📊 لوحة المشرف</h1><p class='subtitle'>مراقبة أداء الطلاب واختيار الأفضل</p></div>", unsafe_allow_html=True)
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
            st.markdown(f"<div class='leaderboard-row {rank_class}'><div style='display:flex;align-items:center;gap:15px;'><span style='font-size:1.5rem;'>{medal}</span><div><div style='font-weight:bold;color:#e2e8f0;'>{s['name']}</div><div style='font-size:0.85rem;color:#94a3b8;'>{s['task']}</div></div></div><div style='text-align:right;'><div style='font-size:1.3rem;font-weight:bold;color:#6366f1;'>{s['avg_score']}/100</div><div style='font-size:0.85rem;color:#94a3b8;'>{s['grade']} | {s['total_prompts']} أوامر | {s['total_time']//60}m</div></div></div>", unsafe_allow_html=True)
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
        except: st.info("تصدير CSV غير متوفر")
        st.markdown("</div>", unsafe_allow_html=True)
    else: st.info("📝 لا يوجد طلاب بعد")
    if st.button("🔙 العودة للرئيسية", key="back_home"):
        st.session_state.admin_view = False
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# Main Router
# ═══════════════════════════════════════════════════════════════
if st.session_state.admin_view: show_admin()
elif st.session_state.exam_finished: show_results()
elif st.session_state.exam_started: show_exam()
else: show_login()

st.markdown("---")
st.markdown("<div style='text-align:center;padding:15px;color:#64748b;font-size:0.85rem;'>🎓 AI 3D Exam Platform | DEVELOPPINI - Formation Agentic AI<br>اختبار تقييم مهارات AI-Driven Developer</div>", unsafe_allow_html=True)
