# 🎨 AI 3D Designer

## المصمم الذكي ثلاثي الأبعاد

تطبيق ويب متكامل لتحويل الصور إلى نماذج 3D مع تحرير تفاعلي وتصدير متعدد الصيغ.

### ✨ الميزات

- 📷 **تحويل الصور**: حوّل أي صورة 2D إلى نموذج 3D قابل للتحرير
- 🤖 **أوامر ذكية**: صف ما تريد باللغة الطبيعية (عربي/إنجليزي/فرنسي...)
- 🎮 **عرض 3D تفاعلي**: تدوير، تقريب، وتحريك بكل حرية (Three.js)
- 🌐 **متعدد اللغات**: دعم 10 لغات عبر Google Translate
- 📤 **تصدير متعدد**: STL, PDF, STEP, OBJ, PLY
- ⚙️ **بارامترات كاملة**: تحكم كامل في الأبعاد والتدوير والإزاحة
- 🎨 **واجهة زاهية**: تصميم عصري بألوان متناسقة
- ☁️ **SaaS-Ready**: جاهز للرفع على السحابة

### 🚀 التشغيل

```bash
pip install -r requirements.txt
streamlit run app.py
```

### 📁 هيكل المشروع

```
ai_designer_3d/
├── app.py                    # التطبيق الرئيسي
├── requirements.txt          # المكتبات
├── components/
│   ├── translator.py         # الترجمة المتعددة اللغات
│   ├── prompt_processor.py   # معالج الأوامر النصية
│   ├── mesh_generator.py     # توليد الـ 3D من الصور
│   └── exporters.py          # التصدير
└── README.md
```

### 🛠️ التقنيات المستخدمة

- **Frontend**: Streamlit + Three.js (WebGL)
- **Backend**: Python + Trimesh
- **AI**: معالجة نصية محلية (بدون API Key)
- **Translation**: Google Translate (مجاني)
- **Export**: STL, PDF (ReportLab), STEP (CadQuery)

### 📝 أمثلة الأوامر

```
مكعب 20x30x15
كرة نصف قطر 10
أسطوانة نصف قطر 5 وارتفاع 20
كبر 2 أضعاف
دور 45 درجة على محور Y
```

### 👨‍💻 المطور

**DEVELOPPINI** - Conseil et accompagnement en Intelligence Artificielle
