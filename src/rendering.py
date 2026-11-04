"""Own, scoped markup: no reliance on Gradio's inherited prose colors."""
from html import escape as E
RANKS=['النتيجة الأولى','النتيجة الثانية','النتيجة الثالثة']
def notice(message,title='قبل البحث',kind='info'):
 return f'<section class="notice {kind}" dir="rtl" role="status"><h2>{E(title)}</h2><p>{E(message)}</p></section>'
EMPTY=notice('اكتب وصفًا عربيًا للشخص، واختر الغرض الشعري، ثم اضغط «ابحث عن البيت الشعري». سنعرض ثلاثة أبيات مرشحة مع الشاعر والمصدر ودرجة التشابه.')
LOADING=notice('جارٍ البحث عن الأبيات الأقرب إلى وصفك. يرجى الانتظار قليلًا.','نبحث في المعنى','loading')
def render(result):
 status=result['status']
 if status!='uncalibrated_candidates':
  texts={'clarification':'أدخل وصفًا عربيًا واضحًا واختر الغرض الشعري. الاسم وحده لا يكفي لتحديد الصفات.','too_long':'الوصف يتجاوز 512 رمزًا للنموذج. اختصره مع الحفاظ على الصفات أو المشاعر الأساسية.','input_conflict':'الوصف يشير إلى شخص حي مع اختيار الرثاء. وضّح المقصود أو اختر غرضًا آخر؛ لم نعرض أبياتًا قد توحي بوفاته. هذا فحص محدود لاتساق المدخلات.','invalid_language':'اكتب الوصف باللغة العربية؛ يمكنك تضمين أسماء أو مصطلحات أخرى ضمنه.','error':'تعذّر إكمال البحث الآن. حاول مجددًا بعد لحظات. إذا استمرت المشكلة، راجع سجل التطبيق المحلي.'}
  return notice(texts.get(status,'لم تتوفر نتائج يمكن عرضها لهذا الطلب.'),'نحتاج إلى توضيح' if status!='error' else 'تعذّر البحث','error' if status=='error' else 'info')
 matches=result.get('matches',[])
 if not matches:return notice('لم تتوفر أبيات مرشحة ضمن الغرض المحدد. حاول وصف الصفات أو المشاعر بطريقة أوضح.','لا توجد نتائج متاحة')
 out=['<section class="results-list" dir="rtl" aria-label="نتائج الاسترجاع"><p class="results-note">أبيات مسترجعة من المجموعة، وليست أبياتًا مولّدة. قد لا يناسب أي مرشح طلبك؛ راجع معناه وسياقه.</p>']
 for i,m in enumerate(matches[:3]):
  r=m['record'];url=r.get('source_url') or ''
  source=f'<a href="{E(url,quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="فتح المصدر المنقول للنتيجة {i+1} في نافذة جديدة">قراءة المصدر المنقول</a>' if url.startswith(('https://','http://')) else '<span>المصدر غير متوفر</span>'
  out.extend([f'<article class="poetry-card" aria-labelledby="rank-{i}"><header class="card-heading"><h2 id="rank-{i}">{RANKS[i]}</h2><span class="genre-label">{E(r["genre"])}</span></header>',f'<div class="bayt" aria-label="البيت الشعري"><p class="bayt-line">{E(r["hemistich_1"])}</p><p class="bayt-line">{E(r["hemistich_2"])}</p></div>',f'<div class="card-meta"><p><span>الشاعر كما ورد في السجل:</span> <strong>{E(r.get("poet") or "غير متحقق")}</strong></p><p><span>الغرض الشعري:</span> {E(r["genre"])}</p><p>{source}</p></div>',f'<div class="score"><p>درجة التشابه الدلالي: <strong dir="ltr">{m["cosine"]:.4f}</strong></p><p class="score-note">إشارة ترتيب، وليست احتمالًا معايرًا لصحة المطابقة.</p></div>',f'<details class="ai-description"><summary>الوصف المقترح آليًا للبيت</summary><p>{E(r["biography"])}</p><p>هذا وصف آلي منفصل عن النص الشعري الأصلي، وليس حقيقة تاريخية موثقة.</p></details></article>'])
 out.append('<p class="provenance-note">النسبة والتصنيف والأوصاف تحتفظ بحالة التحقق الأصلية. إقرار الملاءمة الدلالية بالجملة لا يثبت توثيق المصدر أو حقوق التدريب.</p></section>')
 return ''.join(out)
