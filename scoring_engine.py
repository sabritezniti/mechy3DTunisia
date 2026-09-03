"""
╔═══════════════════════════════════════════════════════════════╗
║  AI 3D Exam Scoring Engine                                   ║
║  محرك تقييم أداء الطالب في Prompt Engineering              ║
╚═══════════════════════════════════════════════════════════════╝
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Tuple

class PromptScorer:
    """محرك تقييم جودة الأوامر النصية"""

    def __init__(self):
        self.criteria = {
            'precision': {  # الدقة
                'weight': 25,
                'description': 'وضوح الأبعاد والقياسات'
            },
            'efficiency': {  # الكفاءة
                'weight': 20,
                'description': 'عدد الأوامر مقابل النتيجة'
            },
            'clarity': {  # الوضوح
                'weight': 20,
                'description': 'عدم الغموض أو التكرار'
            },
            'completeness': {  # الاكتمال
                'weight': 20,
                'description': 'تغطية جميع المتطلبات'
            },
            'creativity': {  # الإبداع
                'weight': 15,
                'description': 'استخدام أوامر متقدمة أو مبتكرة'
            }
        }

        self.advanced_keywords = [
            'subdivide', 'smooth', 'chamfer', 'fillet', 'pattern',
            'mirror', 'boolean', 'extrude', 'revolve', 'loft',
            'shell', 'draft', 'sweep', 'helix', 'array'
        ]

        self.basic_shapes = ['box', 'cube', 'sphere', 'cylinder', 'cone', 'torus']

    def analyze_prompt(self, prompt: str, task_requirements: List[str]) -> Dict:
        """
        تحليل الأمر النصي وتقييمه

        Returns:
            Dict مع الدرجات والتعليقات
        """
        prompt_lower = prompt.lower()
        scores = {}
        feedback = []

        # 1. تقييم الدقة (Precision) - هل يحتوي على أرقام ووحدات؟
        numbers = re.findall(r'\d+\.?\d*', prompt)
        units = re.findall(r'(mm|cm|m|inch|ft|px|%|x)', prompt_lower)

        if len(numbers) >= 3:
            scores['precision'] = 25
            feedback.append("✅ أبعاد دقيقة وواضحة")
        elif len(numbers) >= 1:
            scores['precision'] = 15
            feedback.append("⚠️ بعض الأبعاد موجودة لكن غير كاملة")
        else:
            scores['precision'] = 5
            feedback.append("❌ لا يوجد أبعاد رقمية واضحة")

        if len(units) > 0:
            scores['precision'] += 5
            feedback.append("✅ وحدات القياس محددة")

        scores['precision'] = min(scores['precision'], 25)

        # 2. تقييم الكفاءة (Efficiency) - عدد الأوامر vs النتيجة
        words = prompt.split()
        if len(words) <= 10:
            scores['efficiency'] = 20
            feedback.append("✅ أمر موجز وفعال")
        elif len(words) <= 20:
            scores['efficiency'] = 15
            feedback.append("⚠️ أمر مقبول لكن يمكن اختصاره")
        elif len(words) <= 35:
            scores['efficiency'] = 10
            feedback.append("⚠️ أمر طويل، يحتاج تبسيط")
        else:
            scores['efficiency'] = 5
            feedback.append("❌ أمر مُبالغ في طوله، غير فعال")

        # 3. تقييم الوضوح (Clarity) - هل هناك غموض أو تكرار؟
        vague_words = ['شيء', 'حاجة', 'كذا', 'يعني', 'مثلا', 'something', 'thing', 'etc']
        vague_count = sum(1 for w in vague_words if w in prompt_lower)

        if vague_count == 0 and len(words) > 5:
            scores['clarity'] = 20
            feedback.append("✅ الأمر واضح تماماً بدون غموض")
        elif vague_count <= 1:
            scores['clarity'] = 15
            feedback.append("⚠️ وضوح جيد مع بعض التحفظ")
        elif vague_count <= 3:
            scores['clarity'] = 10
            feedback.append("⚠️ يوجد بعض الغموض في الأمر")
        else:
            scores['clarity'] = 5
            feedback.append("❌ الأمر غامض ويحتاج توضيح")

        # 4. تقييم الاكتمال (Completeness) - هل غطى جميع المتطلبات؟
        covered = 0
        for req in task_requirements:
            req_keywords = req.lower().split()
            if any(kw in prompt_lower for kw in req_keywords):
                covered += 1

        coverage = covered / len(task_requirements) if task_requirements else 1.0
        scores['completeness'] = int(coverage * 20)

        if coverage >= 0.8:
            feedback.append("✅ جميع المتطلبات مغطاة")
        elif coverage >= 0.5:
            feedback.append("⚠️ معظم المتطلبات مغطاة")
        else:
            feedback.append("❌ متطلبات ناقصة")

        # 5. تقييم الإبداع (Creativity) - أوامر متقدمة؟
        advanced_used = [kw for kw in self.advanced_keywords if kw in prompt_lower]
        if len(advanced_used) >= 2:
            scores['creativity'] = 15
            feedback.append(f"✅ استخدام أوامر متقدمة: {', '.join(advanced_used)}")
        elif len(advanced_used) == 1:
            scores['creativity'] = 10
            feedback.append(f"✅ أمر متقدم واحد: {advanced_used[0]}")
        else:
            scores['creativity'] = 5
            feedback.append("⚠️ لا يوجد أوامر متقدمة، أمر أساسي")

        # الدرجة الإجمالية
        total = sum(scores.values())

        # التصنيف
        if total >= 90:
            grade = 'A+'
            level = 'ممتاز - مطور AI محترف'
        elif total >= 80:
            grade = 'A'
            level = 'جيد جداً - قادر على العمل باستقلالية'
        elif total >= 70:
            grade = 'B'
            level = 'جيد - يحتاج بعض التوجيه'
        elif total >= 60:
            grade = 'C'
            level = 'مقبول - يحتاج تدريب إضافي'
        elif total >= 50:
            grade = 'D'
            level = 'ضعيف - يحتاج مراجعة أساسيات'
        else:
            grade = 'F'
            level = 'راسب - غير جاهز حالياً'

        return {
            'scores': scores,
            'total': total,
            'grade': grade,
            'level': level,
            'feedback': feedback,
            'word_count': len(words),
            'numbers_found': len(numbers),
            'advanced_commands': advanced_used,
            'coverage': coverage,
            'timestamp': datetime.now().isoformat()
        }

    def compare_prompts(self, prompts: List[str], task_requirements: List[str]) -> List[Dict]:
        """مقارنة عدة أوامر وتصنيفها"""
        results = []
        for prompt in prompts:
            result = self.analyze_prompt(prompt, task_requirements)
            results.append(result)

        # ترتيب حسب الدرجة
        results.sort(key=lambda x: x['total'], reverse=True)
        return results

    def generate_report(self, student_name: str, results: List[Dict]) -> str:
        """توليد تقرير PDF نصي"""
        report = f"""
╔═══════════════════════════════════════════════════════════════╗
║  تقرير تقييم Prompt Engineering                              ║
║  الطالب: {student_name:<45} ║
╚═══════════════════════════════════════════════════════════════╝

التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}

{'='*65}
 النتائج:
{'='*65}
"""
        for i, res in enumerate(results, 1):
            report += f"""
الأمر #{i}:
  الدرجة الإجمالية: {res['total']}/100
  التقدير: {res['grade']} - {res['level']}
  عدد الكلمات: {res['word_count']}
  الأوامر المتقدمة: {', '.join(res['advanced_commands']) or 'لا يوجد'}

  التفصيل:
    - الدقة: {res['scores']['precision']}/25
    - الكفاءة: {res['scores']['efficiency']}/20
    - الوضوح: {res['scores']['clarity']}/20
    - الاكتمال: {res['scores']['completeness']}/20
    - الإبداع: {res['scores']['creativity']}/15

  الملاحظات:
"""
            for fb in res['feedback']:
                report += f"    {fb}
"

        # متوسط الأداء
        avg = sum(r['total'] for r in results) / len(results) if results else 0
        report += f"""
{'='*65}
 المتوسط العام: {avg:.1f}/100
{'='*65}

التوصية:
"""
        if avg >= 85:
            report += "✅ الطالب جاهز للتوظيف فوراً كـ AI-Driven Developer"
        elif avg >= 70:
            report += "✅ الطالب يملك إمكانيات جيدة، يحتاج تدريب عملي 2-4 أسابيع"
        elif avg >= 60:
            report += "⚠️ الطالب يحتاج تدريب مكثف 1-2 شهر قبل التوظيف"
        else:
            report += "❌ الطالب غير جاهز حالياً، يحتاج إعادة التدريب الأساسي"

        return report


class TaskGenerator:
    """مولد مهام الامتحان"""

    TASKS = [
        {
            'id': 1,
            'title': 'تصميم غلاف هاتف',
            'description': 'صمم غلافاً ثلاثي الأبعاد لهاتف iPhone 15 Pro Max',
            'requirements': [
                'أبعاد 159.9 x 76.7 x 8.25 ملم',
                'فتحة كاميرا ثلاثية',
                'سمك 1.5 ملم',
                'حواف منحنية'
            ],
            'difficulty': 'متوسط',
            'time_limit': 300  # 5 دقائق
        },
        {
            'id': 2,
            'title': 'تصميم حامل كوب',
            'description': 'صمم حامل كوب مكتبي أنيق',
            'requirements': [
                'قطر داخلي 85 ملم',
                'ارتفاع 120 ملم',
                'قاعدة مستقرة',
                'تصميم مفتوح (بدون قاع)'
            ],
            'difficulty': 'سهل',
            'time_limit': 180
        },
        {
            'id': 3,
            'title': 'تصميم ترس (Gear)',
            'description': 'صمم ترساً ميكانيكياً',
            'requirements': [
                'قطر خارجي 50 ملم',
                '20 سن',
                'ثقب مركزي قطر 8 ملم',
                'سمك 5 ملم'
            ],
            'difficulty': 'صعب',
            'time_limit': 420
        },
        {
            'id': 4,
            'title': 'تصميم قالب طباعة 3D',
            'description': 'صمم قالباً لطباعة مجسم ديكوري',
            'requirements': [
                'أبعاد 100x100x50 ملم',
                'تفاصيل نقوش دقيقة',
                'جدران سمك 2 ملم',
                'قاعدة مسطحة'
            ],
            'difficulty': 'صعب',
            'time_limit': 600
        },
        {
            'id': 5,
            'title': 'تصميم مجسم معماري',
            'description': 'صمم نموذجاً مبسطاً لبرج مائل',
            'requirements': [
                'ارتفاع 200 ملم',
                'انحراف 15 درجة',
                'قاعدة مربعة 50x50 ملم',
                'تفاصيل نوافذ'
            ],
            'difficulty': 'متوسط',
            'time_limit': 360
        }
    ]

    def get_task(self, task_id: int = None, difficulty: str = None) -> Dict:
        """الحصول على مهمة"""
        if task_id:
            for task in self.TASKS:
                if task['id'] == task_id:
                    return task

        if difficulty:
            tasks = [t for t in self.TASKS if t['difficulty'] == difficulty]
            if tasks:
                import random
                return random.choice(tasks)

        import random
        return random.choice(self.TASKS)

    def get_all_tasks(self) -> List[Dict]:
        """جميع المهام"""
        return self.TASKS

    def evaluate_task_completion(self, mesh_info: Dict, task: Dict) -> Dict:
        """تقييم إنجاز المهمة"""
        # هذا تقييم بسيط - يمكن تطويره ليكون أكثر دقة
        score = 0
        checks = []

        # التحقق من وجود النموذج
        if mesh_info.get('vertices', 0) > 0:
            score += 30
            checks.append("✅ تم إنشاء نموذج")
        else:
            checks.append("❌ لم يتم إنشاء نموذج")

        # التحقق من الحجم المنطقي
        dims = mesh_info.get('dimensions', [0, 0, 0])
        if any(d > 0 for d in dims):
            score += 20
            checks.append("✅ النموذج له أبعاد منطقية")

        # التحقق من أن النموذج ليس فارغاً
        if mesh_info.get('volume', 0) > 0:
            score += 20
            checks.append("✅ النموذج له حجم")

        # التحقق من جودة الـ mesh
        if mesh_info.get('is_watertight', False):
            score += 15
            checks.append("✅ النموذج مغلق (watertight)")

        # التحقق من عدد الوجوه (ليس مفرطاً ولا قليلاً)
        faces = mesh_info.get('faces', 0)
        if 10 <= faces <= 100000:
            score += 15
            checks.append("✅ دقة الـ mesh مناسبة")

        return {
            'task_score': score,
            'checks': checks,
            'passed': score >= 60
        }
