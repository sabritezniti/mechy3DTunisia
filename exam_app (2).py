"""
╔══════════════════════════════════════════════════════════════════╗
║  AI 3D DESIGNER & EXAM PLATFORM                                 ║
║  DEVELOPPINI — Formation Agentic AI                              ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os, sys, site, json, time, re, io, base64
from datetime import datetime

# ── إصلاح المسار ────────────────────────────────────────────────
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)

import streamlit as st
import numpy as np
import trimesh

# ═════════════════════════════════════════════════════════════════
#  CSS  احترافي
# ═════════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');

:root {
  --primary: #6366f1;
  --primary-dark: #4f46e5;
  --secondary: #ec4899;
  --accent: #06b6d4;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --bg: #0b0f19;
  --bg-card: #111827;
  --bg-elevated: #1f2937;
  --text: #f3f4f6;
  --text-muted: #9ca3af;
  --border: rgba(99,102,241,0.25);
}

* { font-family: 'Tajawal', sans-serif !important; }

.stApp {
  background: var(--bg) !important;
  background-image:
    radial-gradient(circle at 10% 20%, rgba(99,102,241,0.08) 0%, transparent 40%),
    radial-gradient(circle at 90% 80%, rgba(236,72,153,0.06) 0%, transparent 40%) !important;
}

/* ===== HEADER ===== */
.app-header {
  text-align: center;
  padding: 30px 0 10px;
}
.app-header h1 {
  font-size: 2.8rem !important;
  font-weight: 900 !important;
  background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0 !important;
  letter-spacing: -1px;
}
.app-header .tagline {
  color: var(--text-muted);
  font-size: 1.05rem;
  margin-top: 8px;
  font-weight: 500;
}
.app-header .brand {
  color: var(--primary);
  font-size: 0.8rem;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-top: 6px;
  opacity: 0.7;
}

/* ===== CARDS ===== */
.glass-card {
  background: linear-gradient(145deg, rgba(31,41,55,0.9), rgba(17,24,39,0.95));
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 28px;
  margin: 16px 0;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
  backdrop-filter: blur(12px);
  transition: transform 0.2s, box-shadow 0.2s;
}
.glass-card:hover {
  box-shadow: 0 12px 40px rgba(99,102,241,0.15);
}

/* ===== BUTTONS ===== */
.stButton > button {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
  color: white !important;
  border: none !important;
  border-radius: 14px !important;
  padding: 14px 28px !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
  letter-spacing: 0.5px;
  transition: all 0.25s ease !important;
  box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 30px rgba(99,102,241,0.5) !important;
}
.stButton > button:active {
  transform: scale(0.98);
}

/* ===== INPUTS ===== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  background: rgba(17,24,39,0.8) !important;
  border: 1.5px solid rgba(99,102,241,0.3) !important;
  border-radius: 14px !important;
  color: var(--text) !important;
  font-size: 1rem !important;
  padding: 14px 18px !important;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* ===== SLIDERS ===== */
.stSlider > div > div > div[data-testid="stThumbValue"] {
  color: var(--primary) !important;
  font-weight: 700;
}

/* ===== METRICS ===== */
[data-testid="stMetricValue"] {
  font-size: 1.6rem !important;
  font-weight: 800 !important;
  background: linear-gradient(135deg, #818cf8, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
[data-testid="stMetricLabel"] {
  color: var(--text-muted) !important;
  font-size: 0.8rem !important;
}

/* ===== TIMER ===== */
.timer-display {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  padding: 16px 28px;
  border-radius: 16px;
  text-align: center;
  font-size: 2.2rem;
  font-weight: 800;
  font-family: 'Courier New', monospace;
  box-shadow: 0 8px 30px rgba(239,68,68,0.35);
  letter-spacing: 2px;
}

/* ===== SCORE ===== */
.score-circle {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  background: linear-gradient(145deg, rgba(16,185,129,0.2), rgba(5,150,105,0.3));
  border: 3px solid rgba(16,185,129,0.5);
  box-shadow: 0 0 40px rgba(16,185,129,0.2);
}
.score-circle .score-num {
  font-size: 3rem;
  font-weight: 900;
  color: white;
  line-height: 1;
}
.score-circle .score-label {
  font-size: 0.9rem;
  color: rgba(255,255,255,0.8);
  margin-top: 4px;
}

/* ===== BADGES ===== */
.badge {
  display: inline-block;
  padding: 5px 14px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.badge-easy { background: rgba(16,185,129,0.2); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
.badge-medium { background: rgba(245,158,11,0.2); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
.badge-hard { background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

/* ===== PROGRESS BARS ===== */
.progress-track {
  background: rgba(255,255,255,0.06);
  border-radius: 8px;
  height: 10px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  border-radius: 8px;
  background: linear-gradient(90deg, #6366f1, #a855f7);
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ===== DIVIDER ===== */
.fancy-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(99,102,241,0.4), transparent);
  margin: 24px 0;
}

/* ===== VIEWER FRAME ===== */
.viewer-frame {
  border: 1.5px solid rgba(99,102,241,0.25);
  border-radius: 20px;
  overflow: hidden;
  background: #0a0e1a;
  box-shadow: inset 0 0 60px rgba(0,0,0,0.5);
}

/* ===== FOOTER ===== */
.app-footer {
  text-align: center;
  padding: 30px;
  color: var(--text-muted);
  font-size: 0.8rem;
  border-top: 1px solid rgba(255,255,255,0.05);
  margin-top: 40px;
}
</style>
"""

# ═════════════════════════════════════════════════════════════════
#  SCORING ENGINE
# ═════════════════════════════════════════════════════════════════

class PromptScorer:
    ADVANCED = ['subdivide','smooth','chamfer','fillet','pattern','mirror','boolean','extrude','revolve','loft','shell','draft','sweep','helix','array','bevel','round','taper','twist']

    def analyze(self, text: str, reqs: list) -> dict:
        t = text.lower()
        nums = re.findall(r'\d+\.?\d*', text)
        units = re.findall(r'\b(mm|cm|m|inch|ft|\%)\b', t)
        words = text.split()

        # Precision
        p = 25 if len(nums) >= 3 else (15 if len(nums) >= 1 else 5)
        if units: p = min(p+5, 25)

        # Efficiency
        w = len(words)
        e = 20 if w <= 10 else (15 if w <= 20 else (10 if w <= 35 else 5))

        # Clarity
        vague = ['شيء','حاجة','كذا','يعني','مثلا','something','thing','stuff','etc']
        vc = sum(1 for v in vague if v in t)
        c = 20 if vc == 0 and w > 5 else (15 if vc <= 1 else (10 if vc <= 3 else 5))

        # Completeness
        cov = sum(1 for r in reqs if any(k in t for k in r.lower().split()))
        comp = int((cov / len(reqs) * 20)) if reqs else 20

        # Creativity
        adv = [a for a in self.ADVANCED if a in t]
        cr = 15 if len(adv) >= 2 else (10 if len(adv) == 1 else 5)

        total = p + e + c + comp + cr

        if total >= 90: g, lv = 'A+', 'ممتاز — جاهز للتوظيف فوراً'
        elif total >= 80: g, lv = 'A', 'جيد جداً — يعمل باستقلالية'
        elif total >= 70: g, lv = 'B', 'جيد — يحتاج توجيه بسيط'
        elif total >= 60: g, lv = 'C', 'مقبول — تدريب إضافي مطلوب'
        elif total >= 50: g, lv = 'D', 'ضعيف — مراجعة أساسيات'
        else: g, lv = 'F', 'راسب — غير جاهز'

        fb = []
        if p >= 20: fb.append(('✅ أبعاد دقيقة وواضحة', 'success'))
        elif p >= 10: fb.append(('⚠️ بعض الأبعاد ناقصة', 'warning'))
        else: fb.append(('❌ لا يوجد أبعاد رقمية', 'error'))

        if e >= 15: fb.append(('✅ أمر موجز وفعال', 'success'))
        else: fb.append(('⚠️ الأمر طويل، يحتاج تبسيط', 'warning'))

        if c >= 15: fb.append(('✅ وضوح تام بدون غموض', 'success'))
        else: fb.append(('⚠️ يوجد غموض في الصياغة', 'warning'))

        if comp >= 16: fb.append(('✅ جميع المتطلبات مغطاة', 'success'))
        elif comp >= 10: fb.append(('⚠️ معظم المتطلبات مغطاة', 'warning'))
        else: fb.append(('❌ متطلبات ناقصة كثيراً', 'error'))

        if cr >= 10: fb.append((f'✅ أوامر متقدمة: {", ".join(adv[:3])}', 'success'))
        else: fb.append(('⚠️ لا يوجد أوامر متقدمة', 'warning'))

        return {
            'total': total, 'grade': g, 'level': lv,
            'precision': p, 'efficiency': e, 'clarity': c,
            'completeness': comp, 'creativity': cr,
            'feedback': fb, 'words': w, 'numbers': len(nums),
            'advanced': adv, 'coverage': cov / len(reqs) if reqs else 1.0
        }

class TaskGenerator:
    TASKS = [
        {'id':1,'title':'غلاف هاتف ذكي','desc':'صمم غلافاً ثلاثي الأبعاد لهاتف iPhone 15 Pro Max',
         'reqs':['159.9 x 76.7 ملم','سمك 1.5 ملم','فتحة كاميرا ثلاثية','حواف منحنية'],'diff':'متوسط','time':300},
        {'id':2,'title':'حامل كوب مكتبي','desc':'صمم حامل كوب أنيق وعملي',
         'reqs':['قطر داخلي 85 ملم','ارتفاع 120 ملم','قاعدة مستقرة','تصميم مفتوح'],'diff':'سهل','time':180},
        {'id':3,'title':'ترس ميكانيكي','desc':'صمم ترساً ميكانيكياً دقيقاً',
         'reqs':['قطر خارجي 50 ملم','20 سن','ثقب مركزي 8 ملم','سمك 5 ملم'],'diff':'صعب','time':420},
        {'id':4,'title':'قالب طباعة 3D','desc':'صمم قالباً لطباعة مجسم ديكوري',
         'reqs':['100x100x50 ملم','نقوش دقيقة','جدران 2 ملم','قاعدة مسطحة'],'diff':'صعب','time':600},
        {'id':5,'title':'برج مائل معماري','desc':'صمم نموذجاً مبسطاً لبرج مائل',
         'reqs':['ارتفاع 200 ملم','انحراف 15 درجة','قاعدة 50x50 ملم','نوافذ'],'diff':'متوسط','time':360}
    ]
    def get_all(self): return self.TASKS
    def get(self, tid=None):
        import random
        if tid:
            for t in self.TASKS:
                if t['id']==tid: return t
        return random.choice(self.TASKS)

# ═════════════════════════════════════════════════════════════════
#  3D ENGINE
# ═════════════════════════════════════════════════════════════════

class Mesh3D:
    """محرك توليد النماذج ثلاثية الأبعاد"""

    @staticmethod
    def from_image(img_path: str, height: float = 10.0, res: int = 128, invert: bool = False) -> trimesh.Trimesh:
        from PIL import Image
        img = Image.open(img_path).convert('L')
        img = img.resize((res, res), Image.Resampling.LANCZOS)
        arr = np.array(img)
        if invert: arr = 255 - arr
        hmap = (arr / 255.0) * height
        return Mesh3D._heightmap_to_mesh(hmap, res)

    @staticmethod
    def _heightmap_to_mesh(hmap, res):
        x = np.linspace(-50, 50, res)
        y = np.linspace(-50, 50, res)
        xx, yy = np.meshgrid(x, y)
        verts = np.column_stack([xx.ravel(), yy.ravel(), hmap.ravel()])
        faces = []
        for i in range(res-1):
            for j in range(res-1):
                v0 = i*res + j
                v1 = i*res + (j+1)
                v2 = (i+1)*res + j
                v3 = (i+1)*res + (j+1)
                faces.extend([[v0,v1,v2],[v1,v3,v2]])
        mesh = trimesh.Trimesh(vertices=verts, faces=np.array(faces))
        mesh.process()
        return mesh

    @staticmethod
    def from_prompt(text: str) -> trimesh.Trimesh:
        t = text.lower()
        nums = [float(n) for n in re.findall(r'\d+\.?\d*', text)]

        if any(w in t for w in ['مكعب','cube','box','صندوق']):
            s = nums[0] if nums else 20
            return trimesh.creation.box(extents=[s,s,s])
        if any(w in t for w in ['كرة','sphere','ball','دائرة']):
            r = nums[0] if nums else 10
            return trimesh.creation.icosphere(radius=r, subdivisions=3)
        if any(w in t for w in ['أسطوانة','cylinder','عمود']):
            r = nums[0] if len(nums)>0 else 5
            h = nums[1] if len(nums)>1 else 20
            return trimesh.creation.cylinder(radius=r, height=h)
        if any(w in t for w in ['مخروط','cone']):
            r = nums[0] if len(nums)>0 else 5
            h = nums[1] if len(nums)>1 else 20
            return trimesh.creation.cone(radius=r, height=h)
        if any(w in t for w in ['طارة','torus','حلقة','ring']):
            R = nums[0] if len(nums)>0 else 10
            r = nums[1] if len(nums)>1 else 2
            return trimesh.creation.torus(major_radius=R, minor_radius=r)
        if any(w in t for w in ['هرم','pyramid']):
            s = nums[0] if nums else 15
            return trimesh.creation.cylinder(radius=s, height=s*1.5, sections=4)
        if any(w in t for w in ['كبسولة','capsule']):
            r = nums[0] if len(nums)>0 else 3
            h = nums[1] if len(nums)>1 else 10
            return trimesh.creation.capsule(radius=r, height=h)
        # افتراضي
        return trimesh.creation.box(extents=[20,20,20])

    @staticmethod
    def info(mesh: trimesh.Trimesh) -> dict:
        b = mesh.bounds
        return {
            'vertices': len(mesh.vertices),
            'faces': len(mesh.faces),
            'volume': float(mesh.volume) if mesh.is_watertight else 0.0,
            'area': float(mesh.area),
            'dims': (b[1]-b[0]).tolist(),
            'watertight': mesh.is_watertight
        }

    @staticmethod
    def export_stl(mesh: trimesh.Trimesh) -> bytes:
        buf = io.BytesIO()
        mesh.export(buf, file_type='stl')
        return buf.getvalue()

    @staticmethod
    def export_obj(mesh: trimesh.Trimesh) -> bytes:
        buf = io.BytesIO()
        mesh.export(buf, file_type='obj')
        return buf.getvalue()

    @staticmethod
    def export_ply(mesh: trimesh.Trimesh) -> bytes:
        buf = io.BytesIO()
        mesh.export(buf, file_type='ply')
        return buf.getvalue()

# ═════════════════════════════════════════════════════════════════
#  THREE.JS VIEWER
# ═════════════════════════════════════════════════════════════════

def threejs_html(mesh: trimesh.Trimesh, h: int = 520) -> str:
    v = json.dumps(mesh.vertices.tolist())
    f = json.dumps(mesh.faces.tolist())
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body{{margin:0;overflow:hidden;background:#0a0e1a}}#c{{width:100%;height:{h}px}}</style>
</head><body><div id="c"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
const scene=new THREE.Scene();scene.background=new THREE.Color(0x0a0e1a);
scene.fog=new THREE.Fog(0x0a0e1a,100,500);
const camera=new THREE.PerspectiveCamera(45,1,0.1,1000);
camera.position.set(70,55,70);
const renderer=new THREE.WebGLRenderer({{antialias:true}});
renderer.setSize(document.getElementById('c').clientWidth,{h});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.shadowMap.enabled=true;
document.getElementById('c').appendChild(renderer.domElement);
const controls=new THREE.OrbitControls(camera,renderer.domElement);
controls.enableDamping=true;controls.dampingFactor=0.05;
controls.minDistance=20;controls.maxDistance=250;
scene.add(new THREE.AmbientLight(0x404040,2.5));
const dl=new THREE.DirectionalLight(0xffffff,1.8);
dl.position.set(60,120,60);dl.castShadow=true;scene.add(dl);
scene.add(new THREE.PointLight(0x6366f1,1.2,120).position.set(-60,60,-60));
scene.add(new THREE.PointLight(0xec4899,1.0,120).position.set(60,-40,60));
const geo=new THREE.BufferGeometry();
const verts={v};const faces={f};const pos=[];
for(let i=0;i<faces.length;i++){{
  const fa=faces[i];
  pos.push(verts[fa[0]][0],verts[fa[0]][1],verts[fa[0]][2],
           verts[fa[1]][0],verts[fa[1]][1],verts[fa[1]][2],
           verts[fa[2]][0],verts[fa[2]][1],verts[fa[2]][2]);
}}
geo.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));
geo.computeVertexNormals();
const mat=new THREE.MeshPhysicalMaterial({{
  color:0x6366f1,metalness:0.1,roughness:0.3,
  clearcoat:0.8,clearcoatRoughness:0.2,
  side:THREE.DoubleSide
}});
const mesh3d=new THREE.Mesh(geo,mat);mesh3d.castShadow=true;mesh3d.receiveShadow=true;
const wireGeo=new THREE.WireframeGeometry(geo);
const wireMat=new THREE.LineBasicMaterial({{color:0x22d3ee,transparent:true,opacity:0.25}});
const wireframe=new THREE.LineSegments(wireGeo,wireMat);wireframe.visible=false;
const group=new THREE.Group();group.add(mesh3d);group.add(wireframe);
geo.computeBoundingBox();const cen=new THREE.Vector3();
geo.boundingBox.getCenter(cen);group.position.sub(cen);
scene.add(group);
const grid=new THREE.GridHelper(180,18,0x6366f1,0x1a1a3e);scene.add(grid);
const axes=new THREE.AxesHelper(50);scene.add(axes);
let autoRot=false;
function animate(){{
  requestAnimationFrame(animate);
  if(autoRot)group.rotation.y+=0.008;
  controls.update();renderer.render(scene,camera);
}}
animate();
window.addEventListener('resize',()=>{{
  camera.aspect=document.getElementById('c').clientWidth/{h};
  camera.updateProjectionMatrix();
  renderer.setSize(document.getElementById('c').clientWidth,{h});
}});
</script></body></html>"""

# ═════════════════════════════════════════════════════════════════
#  SESSION
# ═════════════════════════════════════════════════════════════════

def init_state():
    defaults = {
        'student_name':'','exam_on':False,'done':False,
        'task':None,'t0':None,'tr':0,'mesh':None,
        'history':[],'scores':[],'score':None,
        'all_students':[],'admin':False,'uploaded_img':None
    }
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v

# ═════════════════════════════════════════════════════════════════
#  PAGES
# ═════════════════════════════════════════════════════════════════

def page_login():
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="app-header">
      <h1>🎓 AI 3D Exam Platform</h1>
      <div class="tagline">منصة تقييم مهارات Prompt Engineering & AI-Driven Development</div>
      <div class="brand">DEVELOPPINI — Formation Agentic AI</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,2.2,1])
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 👤 تسجيل الدخول للامتحان")
        name = st.text_input("", placeholder="الاسم الكامل (مثال: أحمد بن علي)", key="nm", label_visibility="collapsed")

        st.markdown("### 📋 اختيار المهمة")
        tg = TaskGenerator()
        tasks = tg.get_all()
        opts = [f"{t['id']}. {t['title']} — {t['diff']}" for t in tasks]
        sel = st.selectbox("", opts, label_visibility="collapsed")
        tid = int(sel.split('.')[0])
        task = tg.get(tid)

        diff_map = {'سهل':'badge-easy','متوسط':'badge-medium','صعب':'badge-hard'}
        badge = diff_map.get(task['diff'], 'badge-medium')
        reqs_html = ''.join([f'<li style="margin:4px 0;color:#9ca3af;">• {r}</li>' for r in task['reqs']])

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border-radius:14px;padding:18px;margin:14px 0;border:1px solid rgba(99,102,241,0.15);">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <span style="font-weight:700;color:#f3f4f6;font-size:1.05rem;">{task['title']}</span>
            <span class="badge {badge}">{task['diff']}</span>
          </div>
          <p style="color:#9ca3af;margin:0 0 10px 0;font-size:0.92rem;">{task['desc']}</p>
          <div style="font-size:0.85rem;"><strong style="color:#818cf8;">المتطلبات:</strong><ul style="margin:6px 0;padding-right:16px;">{reqs_html}</ul></div>
          <div style="color:#fbbf24;font-size:0.85rem;margin-top:8px;">⏱️ الوقت المحدد: {task['time']//60} دقيقة</div>
        </div>
        """, unsafe_allow_html=True)

        admin_code = st.text_input("🔐 كود المشرف (اختياري)", type="password", key="adm")

        b1, b2 = st.columns(2)
        with b1:
            if st.button("🚀 بدء الامتحان", key="start"):
                if name.strip():
                    st.session_state.student_name = name.strip()
                    st.session_state.task = task
                    st.session_state.exam_on = True
                    st.session_state.t0 = time.time()
                    st.session_state.tr = task['time']
                    st.session_state.history = []
                    st.session_state.scores = []
                    st.session_state.mesh = None
                    st.session_state.score = None
                    st.rerun()
                else:
                    st.error("❌ يرجى إدخال الاسم")
        with b2:
            if st.button("📊 لوحة المشرف", key="admin_btn"):
                if admin_code == "dev2024":
                    st.session_state.admin = True
                    st.rerun()
                elif admin_code:
                    st.error("❌ كود خاطئ")
        st.markdown('</div>', unsafe_allow_html=True)

def page_exam():
    st.markdown(CSS, unsafe_allow_html=True)
    task = st.session_state.task

    # Timer logic
    if st.session_state.exam_on and not st.session_state.done:
        elapsed = int(time.time() - st.session_state.t0)
        st.session_state.tr = max(0, task['time'] - elapsed)
        if st.session_state.tr <= 0:
            st.session_state.done = True
            st.rerun()

    mins = st.session_state.tr // 60
    secs = st.session_state.tr % 60
    timer_color = "#ef4444" if st.session_state.tr < 60 else "#fbbf24" if st.session_state.tr < 120 else "#10b981"

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;padding:16px 0 20px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:20px;">
      <div>
        <div style="font-size:1.3rem;font-weight:800;color:#f3f4f6;">👤 {st.session_state.student_name}</div>
        <div style="color:#9ca3af;font-size:0.9rem;margin-top:2px;">المهمة: {task['title']}</div>
      </div>
      <div style="background:linear-gradient(135deg,{timer_color},#b91c1c);color:white;padding:14px 24px;border-radius:14px;text-align:center;font-size:1.9rem;font-weight:800;font-family:monospace;box-shadow:0 4px 20px rgba(239,68,68,0.3);">
        {mins:02d}:{secs:02d}
      </div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1,1.1])

    with left:
        # ── Prompt Area ──
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📝 أوامر التصميم النصية")
        st.caption("اكتب وصفاً دقيقاً للنموذج ثلاثي الأبعاد — بالعربية أو الإنجليزية")
        prompt = st.text_area("", placeholder="مثال: مكعب طول 50 وعرض 30 وارتفاع 20 ملم مع حواف منحنية radius 3 ملم وثقب في المنتصف قطر 10 ملم", height=110, key="prompt_txt", label_visibility="collapsed")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1: sc = st.slider("تكبير", 0.3, 4.0, 1.0, 0.1, key="sc")
        with c2: rot = st.slider("دوران Y", 0, 360, 0, 5, key="rt")
        with c3: sm = st.checkbox("تنعيم Smooth", key="sm")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        b1, b2 = st.columns([2,1])
        with b1:
            if st.button("▶️  تنفيذ الأمر", key="exec", use_container_width=True):
                if prompt.strip():
                    with st.spinner("جاري بناء النموذج ثلاثي الأبعاد..."):
                        st.session_state.history.append({'prompt': prompt, 't': time.time()-st.session_state.t0})
                        mesh = Mesh3D.from_prompt(prompt)
                        if sc != 1.0: mesh.apply_scale([sc,sc,sc])
                        if rot != 0: mesh.apply_transform(trimesh.transformations.rotation_matrix(np.radians(rot), [0,1,0]))
                        if sm: mesh = mesh.smoothed()
                        st.session_state.mesh = mesh
                        scorer = PromptScorer()
                        st.session_state.score = scorer.analyze(prompt, task['reqs'])
                        st.session_state.scores.append(st.session_state.score)
                        st.toast("✅ تم بناء النموذج بنجاح!", icon="🎉")
                else:
                    st.warning("يرجى كتابة أمر أولاً")
        with b2:
            if st.button("🏁 إنهاء", key="fin", use_container_width=True):
                st.session_state.done = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Image Upload ──
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📷 تحويل صورة إلى 3D")
        st.caption("ارفع صورة وسنحولها إلى نموذج ثلاثي الأبعاد (Height Map Extrusion)")
        up = st.file_uploader("", type=['png','jpg','jpeg','bmp','webp'], key="img_up", label_visibility="collapsed")
        if up:
            from PIL import Image
            img = Image.open(up)
            st.image(img, use_column_width=True)
            c1, c2 = st.columns(2)
            with c1: hgt = st.slider("ارتفاع الـ Extrusion", 1.0, 50.0, 15.0, 1.0, key="hgt")
            with c2: res = st.slider("الدقة", 50, 250, 120, 10, key="res_img")
            inv = st.checkbox("عكس الألوان (نقش غائر)", key="inv")
            if st.button("🔄 تحويل الصورة إلى 3D", key="conv_img", use_container_width=True):
                with st.spinner("جاري تحويل الصورة..."):
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                        img.save(tmp.name)
                        mesh = Mesh3D.from_image(tmp.name, height=hgt, res=res, invert=inv)
                        st.session_state.mesh = mesh
                        st.session_state.history.append({'prompt': f'[صورة] {up.name}', 't': time.time()-st.session_state.t0})
                        st.toast("✅ تم تحويل الصورة بنجاح!", icon="🖼️")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── History ──
        if st.session_state.history:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📜 سجل الأوامر")
            for i, h in enumerate(st.session_state.history, 1):
                st.markdown(f'<div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:10px 14px;margin:6px 0;border-right:3px solid #6366f1;font-size:0.9rem;"><span style="color:#818cf8;font-weight:700;">#{i}</span> <span style="color:#d1d5db;">{h["prompt"][:90]}{"..." if len(h["prompt"])>90 else ""}</span> <span style="color:#6b7280;font-size:0.75rem;">({h["t"]:.0f}s)</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with right:
        # ── 3D Viewer ──
        st.markdown('<div class="glass-card" style="padding:0;overflow:hidden;">', unsafe_allow_html=True)
        st.markdown(f'<div style="padding:16px 20px 0;"><h4 style="margin:0;color:#f3f4f6;">🎮 المعاينة ثلاثية الأبعاد</h4><p style="margin:4px 0 0;color:#6b7280;font-size:0.8rem;">🖱️ يسار: تدوير  |  يمين: تحريك  |  عجلة: تقريب</p></div>', unsafe_allow_html=True)
        if st.session_state.mesh is not None:
            html = threejs_html(st.session_state.mesh, h=480)
            st.components.v1.html(html, height=480, scrolling=False)
            info = Mesh3D.info(st.session_state.mesh)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("النقاط", f"{info['vertices']:,}")
            c2.metric("الوجوه", f"{info['faces']:,}")
            c3.metric("الحجم", f"{info['volume']:.1f} mm³")
            c4.metric("المساحة", f"{info['area']:.1f} mm²")

            # Exports
            st.markdown("<div style='padding:0 20px 16px;'>", unsafe_allow_html=True)
            st.markdown("<p style='color:#9ca3af;font-size:0.8rem;margin-bottom:8px;'>📤 تصدير النموذج:</p>", unsafe_allow_html=True)
            e1, e2, e3 = st.columns(3)
            with e1:
                st.download_button("🔷 STL", Mesh3D.export_stl(st.session_state.mesh), file_name="model.stl", mime="application/octet-stream", use_container_width=True)
            with e2:
                st.download_button("📄 OBJ", Mesh3D.export_obj(st.session_state.mesh), file_name="model.obj", mime="text/plain", use_container_width=True)
            with e3:
                st.download_button("🔶 PLY", Mesh3D.export_ply(st.session_state.mesh), file_name="model.ply", mime="application/octet-stream", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:center;padding:100px 20px;color:#4b5563;"><div style="font-size:4rem;margin-bottom:16px;">🎨</div><p style="font-size:1.1rem;margin:0;">اكتب أمراً أو ارفع صورة<br>لرؤية النموذج هنا</p></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Live Score ──
        if st.session_state.score:
            sc = st.session_state.score
            grade_colors = {'A+':'#10b981','A':'#10b981','B':'#3b82f6','C':'#f59e0b','D':'#ef4444','F':'#7c2d12'}
            gc = grade_colors.get(sc['grade'], '#f59e0b')

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="text-align:center;margin-bottom:16px;">
              <div style="width:130px;height:130px;border-radius:50%;margin:0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(145deg,{gc}22,{gc}44);border:3px solid {gc};">
                <div style="font-size:2.6rem;font-weight:900;color:white;line-height:1;">{sc['total']}</div>
                <div style="font-size:0.75rem;color:rgba(255,255,255,0.8);margin-top:2px;">من 100</div>
              </div>
              <div style="margin-top:10px;font-size:1.3rem;font-weight:800;color:{gc};">{sc['grade']}</div>
              <div style="font-size:0.85rem;color:#9ca3af;">{sc['level']}</div>
            </div>
            """, unsafe_allow_html=True)

            crits = [
                ("الدقة", sc['precision'], 25, "#6366f1"),
                ("الكفاءة", sc['efficiency'], 20, "#3b82f6"),
                ("الوضوح", sc['clarity'], 20, "#8b5cf6"),
                ("الاكتمال", sc['completeness'], 20, "#ec4899"),
                ("الإبداع", sc['creativity'], 15, "#10b981")
            ]
            for name, val, mx, col in crits:
                pct = (val/mx)*100
                st.markdown(f"""
                <div style="display:flex;align-items:center;margin:8px 0;font-size:0.85rem;">
                  <span style="width:60px;color:#d1d5db;">{name}</span>
                  <div style="flex:1;background:rgba(255,255,255,0.06);border-radius:6px;height:8px;margin:0 10px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{col};border-radius:6px;transition:width 0.5s;"></div>
                  </div>
                  <span style="width:45px;text-align:left;color:{col};font-weight:700;font-size:0.8rem;">{val}/{mx}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top:12px;'>", unsafe_allow_html=True)
            for txt, typ in sc['feedback']:
                bg = {'success':'rgba(16,185,129,0.12)','warning':'rgba(245,158,11,0.12)','error':'rgba(239,68,68,0.12)'}[typ]
                cl = {'success':'#34d399','warning':'#fbbf24','error':'#f87171'}[typ]
                st.markdown(f'<div style="background:{bg};color:{cl};padding:8px 12px;border-radius:8px;margin:4px 0;font-size:0.85rem;">{txt}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def page_results():
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="app-header">
      <h1>🎓 نتائج الامتحان</h1>
      <div class="tagline">تقرير الأداء النهائي — DEVELOPPINI</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.scores:
        st.error("❌ لم يتم إرسال أي أوامر خلال الامتحان")
        if st.button("🔄 العودة", key="back0"):
            reset_exam()
        return

    avg = sum(s['total'] for s in st.session_state.scores) / len(st.session_state.scores)
    best = max(s['total'] for s in st.session_state.scores)
    n_prompts = len(st.session_state.history)
    total_t = int(time.time() - st.session_state.t0)

    if avg >= 90: g, lv, gc = 'A+', 'ممتاز — جاهز للتوظيف فوراً', '#10b981'
    elif avg >= 80: g, lv, gc = 'A', 'جيد جداً — يعمل باستقلالية', '#10b981'
    elif avg >= 70: g, lv, gc = 'B', 'جيد — يحتاج توجيه بسيط', '#3b82f6'
    elif avg >= 60: g, lv, gc = 'C', 'مقبول — تدريب إضافي مطلوب', '#f59e0b'
    elif avg >= 50: g, lv, gc = 'D', 'ضعيف — مراجعة أساسيات', '#ef4444'
    else: g, lv, gc = 'F', 'راسب — غير جاهز', '#7c2d12'

    st.session_state.all_students.append({
        'name': st.session_state.student_name, 'task': st.session_state.task['title'],
        'avg': round(avg,1), 'best': best, 'grade': g, 'level': lv,
        'prompts': n_prompts, 'time': total_t, 'ts': datetime.now().isoformat()
    })

    c1, c2, c3 = st.columns([1,2.2,1])
    with c2:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
          <div style="width:180px;height:180px;border-radius:50%;margin:0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(145deg,{gc}18,{gc}35);border:4px solid {gc};box-shadow:0 0 50px {gc}33;">
            <div style="font-size:3.5rem;font-weight:900;color:white;line-height:1;">{avg:.1f}</div>
            <div style="font-size:0.9rem;color:rgba(255,255,255,0.8);">من 100</div>
          </div>
          <div style="margin-top:16px;font-size:2rem;font-weight:800;color:{gc};">{g}</div>
          <div style="font-size:1rem;color:#9ca3af;margin-top:4px;">{lv}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📈 إحصائيات الأداء")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📝 الأوامر", n_prompts)
    c2.metric("⭐ أفضل درجة", f"{best}/100")
    c3.metric("⏱️ الوقت", f"{total_t//60}د {total_t%60}ث")
    c4.metric("🎯 الكفاءة", f"{best/max(n_prompts,1):.1f}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📋 تفاصيل كل أمر")
    for i, (h, s) in enumerate(zip(st.session_state.history, st.session_state.scores), 1):
        with st.expander(f"الأمر #{i} — {s['total']}/100  ({s['grade']})"):
            st.write(f"**النص:** {h['prompt']}")
            st.write(f"**الوقت:** {h['t']:.1f} ثانية  |  **الكلمات:** {s['words']}  |  **متقدمة:** {', '.join(s['advanced']) or 'لا يوجد'}")
            cc = st.columns(5)
            for c, (name, val, mx) in zip(cc, [("الدقة",s['precision'],25),("الكفاءة",s['efficiency'],20),("الوضوح",s['clarity'],20),("الاكتمال",s['completeness'],20),("الإبداع",s['creativity'],15)]):
                c.metric(name, f"{val}/{mx}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💡 تقييم المشرف")
    if avg >= 85:
        st.success("✅ **الطالب جاهز للتوظيف فوراً كـ AI-Driven Developer**\n\nيملك مهارات عالية في صياغة الأوامر الدقيقة، وفهم متطلبات المهام بسرعة، وإنتاج نتائج عملية من المحاولة الأولى.")
    elif avg >= 70:
        st.info("✅ **الطالب يملك إمكانيات جيدة**\n\nيحتاج تدريب عملي 2–4 أسابيع على تحسين دقة الأوامر وتقليل عدد المحاولات.")
    else:
        st.warning("⚠️ **الطالب يحتاج تدريب مكثف**\n\nنقاط الضعف: الأوامر غامضة، يحتاج عدة محاولات، يجب مراجعة أساسيات Prompt Engineering.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📤 تصدير التقرير")
    scorer = PromptScorer()
    report = f"تقرير تقييم: {st.session_state.student_name}\n{'='*50}\n"
    report += f"المتوسط: {avg:.1f}/100 | التقدير: {g}\n\n"
    for i, s in enumerate(st.session_state.scores, 1):
        report += f"الأمر #{i}: {s['total']}/100 ({s['grade']})\n"
        for txt, _ in s['feedback']: report += f"  {txt}\n"
        report += "\n"
    report += f"\nالتوصية: {lv}\n"
    st.download_button("⬇️ تحميل التقرير (TXT)", report, file_name=f"report_{st.session_state.student_name.replace(' ','_')}.txt", mime="text/plain")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔄 امتحان جديد", key="new_ex"):
        reset_exam()

def page_admin():
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="app-header">
      <h1>📊 لوحة المشرف</h1>
      <div class="tagline">مراقبة أداء الطلاب واختيار الأفضل</div>
    </div>
    """, unsafe_allow_html=True)

    studs = st.session_state.all_students
    if not studs:
        st.info("📝 لا يوجد طلاب قاموا بالامتحان بعد")
        if st.button("🔙 العودة", key="bk_ad"):
            st.session_state.admin = False
            st.rerun()
        return

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📈 إحصائيات الدفعة")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 الطلاب", len(studs))
    c2.metric("⭐ المتوسط", f"{sum(s['avg'] for s in studs)/len(studs):.1f}")
    c3.metric("🥇 الأعلى", max(s['avg'] for s in studs))
    c4.metric("⏱️ متوسط الوقت", f"{sum(s['time'] for s in studs)//len(studs)//60}د")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🏆 لوحة المتصدرين")
    sorted_studs = sorted(studs, key=lambda x: x['avg'], reverse=True)
    for i, s in enumerate(sorted_studs, 1):
        rc = f"rank-{i}" if i <= 3 else ""
        medal = "🥇" if i==1 else ("🥈" if i==2 else ("🥉" if i==3 else f"#{i}"))
        st.markdown(f"""
        <div class="leaderboard-row {rc}">
          <div style="display:flex;align-items:center;gap:14px;">
            <span style="font-size:1.6rem;">{medal}</span>
            <div>
              <div style="font-weight:800;color:#f3f4f6;font-size:1.05rem;">{s['name']}</div>
              <div style="color:#9ca3af;font-size:0.82rem;">{s['task']}</div>
            </div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:1.4rem;font-weight:800;color:#818cf8;">{s['avg']}/100</div>
            <div style="color:#6b7280;font-size:0.8rem;">{s['grade']} | {s['prompts']} أمر | {s['time']//60}د</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📤 تصدير النتائج")
    try:
        import csv
        out = io.StringIO()
        w = csv.writer(out)
        w.writerow(['الاسم','المهمة','الدرجة','التقدير','المستوى','الأوامر','الوقت','التاريخ'])
        for s in sorted_studs:
            w.writerow([s['name'],s['task'],s['avg'],s['grade'],s['level'],s['prompts'],s['time'],s['ts']])
        st.download_button("⬇️ تحميل CSV", out.getvalue(), file_name="exam_results.csv", mime="text/csv")
    except Exception as e:
        st.error(f"خطأ التصدير: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 العودة للرئيسية", key="back_admin"):
        st.session_state.admin = False
        st.rerun()

def reset_exam():
    for k in ['exam_on','done','task','t0','tr','mesh','history','scores','score']:
        st.session_state[k] = None if k not in ['tr'] else 0
    st.session_state.exam_on = False
    st.session_state.done = False
    st.rerun()

# ═════════════════════════════════════════════════════════════════
#  ROUTER
# ═════════════════════════════════════════════════════════════════

init_state()

if st.session_state.admin:
    page_admin()
elif st.session_state.done:
    page_results()
elif st.session_state.exam_on:
    page_exam()
else:
    page_login()

st.markdown("""
<div class="app-footer">
  🎓 AI 3D Exam Platform &nbsp;|&nbsp; DEVELOPPINI — Formation Agentic AI<br>
  <span style="opacity:0.5;">تقييم مهارات AI-Driven Developer</span>
</div>
""", unsafe_allow_html=True)
