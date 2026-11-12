!pip install gradio google-generativeai -q

import gradio as gr
import google.generativeai as genai
from google.colab import userdata

# 1. جلب المفتاح وتنظيفه
raw_key = userdata.get('GEMINI_API_KEY')
api_key = raw_key.strip().split()[0] if raw_key else ""

if not api_key:
    print("⚠️ خطأ: لم يتم العثور على المفتاح في الخزنة.")
else:
    genai.configure(api_key=api_key)
    print("✅ تم الاتصال بالعقل السحابي.")

# 2. دالة التحليل
def get_financial_analysis(news_text):
    if not news_text:
        return "الرجاء إدخال خبر أو نص اقتصادي."
    
    # نستخدم نموذج gemini-flash-latest المستقر
    model = genai.GenerativeModel('gemini-flash-latest') 
    prompt = f"""
    أنت مستشار اقتصادي خبير في أسواق النفط والغاز.
    اقرأ هذا الخبر الاقتصادي وحلله:
    
    النص: {news_text}
    
    المطلوب:
    1. تحديد الاتجاه (إيجابي/سلبي/محايد).
    2. شرح السبب.
    3. توقع حركة السعر.
    أجب باللغة العربية بأسلوب احترافي.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"حدث خطأ: {e}"

# 3. بناء الواجهة
app = gr.Interface(
    fn=get_financial_analysis,
    inputs=gr.Textbox(lines=5, label="أدخل خبراً اقتصادياً (مثلاً: أوبك تخفض الإنتاج)"),
    outputs=gr.Textbox(label="تحليل المستشار المالي الذكي"),
    title="📈 AI Financial Consultant",
    description="نظام ذكاء اصطناعي سحابي لتحليل أخبار النفط."
)

app.launch(share=True, debug=False)
