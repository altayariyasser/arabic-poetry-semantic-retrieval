"""Editorial gpt-taste composition over the contrast-safe, verified Gradio backend."""
import sys,argparse,os
from pathlib import Path
os.environ['GRADIO_ANALYTICS_ENABLED']='False'
HERE=Path(__file__).resolve().parent
from src.content import HERO,SEARCH,NOTES,MARQUEE,FOOTER,showcase
from src.mocha import soften
from src import core

def create_app(engine):
 import gradio as gr
 css=(HERE/'assets/style.css').read_text(encoding='utf-8')
 with gr.Blocks(theme=soften(core.make_theme()),css=css,js=(HERE/'assets/motion.js').read_text(encoding='utf-8'),title='مشروع الاسترجاع الدلالي للشعر العربي',analytics_enabled=False,head='<meta name="color-scheme" content="light"><meta name="description" content="من وصف الإنسان إلى بيت شعري موجود في المجموعة، مع الشاعر والمصدر.">') as demo:
  with gr.Column(elem_id='poetry-app'):
   gr.HTML(HERO)
   gr.HTML(SEARCH)
   with gr.Row(elem_id='retrieval-panel'):
    with gr.Column(scale=4,min_width=250):
     bio=gr.Textbox(label='الوصف أو السيرة',placeholder='شخص كريم يساعد المحتاجين ويشتهر بحسن الضيافة.',lines=4,max_lines=9,elem_id='biography')
    with gr.Column(scale=1,min_width=200):
     genre=gr.Dropdown(list(core.GENRES),label='الغرض الشعري',value='مدح',filterable=False,elem_id='genre-select')
     search=gr.Button('ابحث عن البيت الشعري',variant='primary',elem_id='search-button')
   gr.HTML('<p class="input-hint" dir="rtl">اذكر الصفات أو المشاعر والعلاقة المقصودة. التشابه ليس ضمانًا للملاءمة، وقد لا تغطي المجموعة طلبك.</p>')
   with gr.Tabs(elem_id='poetry-tabs'):
    with gr.Tab('الاسترجاع الدلالي'):output=gr.HTML(core.EMPTY,elem_id='poetry-results')
    with gr.Tab('عن المشروع'):
     gr.HTML('<section class="info-section" dir="rtl"><h2>قراءة دلالية للشعر العربي</h2><p>يقارن E5 الصغير متعدد اللغات وصفك بالأوصاف المقترحة آليًا للأبيات، داخل الغرض المختار. تستخدم المجموعة ٣٬٠٠٠ سجل وفهارس محفوظة من ٣٨٤ بعدًا؛ لا يعاد بناؤها عند البحث.</p><p>النموذج مدرّب مسبقًا، ولم ينفّذ ضبط دقيق على الشعر. تبقى النصوص والمصادر وحقوق التدريب والتقسيمات والأوصاف كما وردت في السجلات الأصلية.</p></section>')
    with gr.Tab('المنهجية'):
     gr.HTML('<section class="info-section" dir="rtl"><h2>التشابه يساعد على الترتيب، ولا يمنح اليقين</h2><p>بعد ترشيح الغرض، نرتب الأبيات بتشابه جيب التمام في الوصف، مع منع تكرار النص الكامل في النتائج الثلاث. تبقى BM25، ودلالة نص البيت، والدمج RRF محفوظة في المشروع للمقارنة.</p><p>التقييم الحالي محدود بأحكام AI مؤقتة، وليس تقييمًا بشريًا مستقلاً. لا توجد عتبة قبول معايرة للمجموعة. فحص تعارض الشخص الحي مع الرثاء محدود، وقد تظل طلبات غير مدعومة تحصل على مرشحات غير ملائمة.</p><p>نستخدم خط ثمانية إن كان مثبتًا محليًا؛ البديل الحالي Tahoma للواجهة وTraditional Arabic للشعر. Outfit مطلوب للنص الإنجليزي إن توفر محليًا؛ ثم Arial. الرسوم زخرفية أصلية، وليست مخطوطات أو مصادر تاريخية.</p></section>')
   gr.HTML(NOTES)
   gr.HTML(showcase())
   gr.HTML(MARQUEE)
   gr.HTML(FOOTER)
  responder=core.Responder(engine)
  def prepare():return gr.update(value='جارٍ البحث…',interactive=False),core.LOADING
  def ready():return gr.update(value='ابحث عن البيت الشعري',interactive=True)
  def respond(bio,genre,progress=gr.Progress()):
   progress(0,desc='جارٍ البحث عن الأبيات');answer=responder(bio,genre);progress(1,desc='اكتمل البحث');return answer
  for trigger in [search.click,bio.submit]:
   trigger(prepare,None,[search,output],queue=False,api_name=False).then(respond,[bio,genre],output,api_name='retrieve' if trigger==search.click else False,concurrency_limit=1,concurrency_id='poetry-retrieval',show_progress='full',show_progress_on=output,scroll_to_output=True).then(ready,None,search,queue=False,api_name=False)
 return demo

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--host',default=os.environ.get('GRADIO_SERVER_NAME','127.0.0.1'));p.add_argument('--port',type=int,default=int(os.environ.get('PORT','7860')));a=p.parse_args()
 create_app(core.FinalEngine()).launch(server_name=a.host,server_port=a.port,share=False,show_api=False,show_error=False,inbrowser=False)
