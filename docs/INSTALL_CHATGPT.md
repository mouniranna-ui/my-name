# الاستعمال فـChatGPT

[الصفحة الرئيسية](../README.md) · [English quick start](../README.en.md)

![طرق الاستعمال داخل ChatGPT](images/chatgpt-steps.svg)

## الطريقة المتاحة لأي محادثة كتقبل الصور والتعليمات

1. حمّل المشروع وفك الضغط.
2. افتح [chatgpt-instructions.txt](../prompts/chatgpt-instructions.txt)، وانسخ المحتوى فمحادثة جديدة.
3. زيد صورة الرسم. يمكن تزيد [portable-knowledge.txt](../prompts/portable-knowledge.txt) وملف `cad_tools.py` كموارد إذا كانت المحادثة كتقبلهم.
4. طلب DXF قابل للتعديل، PDF وملاحظة القياسات الناقصة.

```text
تبع تعليمات Photo to AutoCAD المرفقة، وقرا هاد الرسم.
إلا كان عندك تنفيذ Python، استعمل الأدوات باش تنتج DXF وPDF فعلياً وتراجعهم.
إلا ما كانش، عطيني جدول القياسات وبرنامج كامل قابل للتشغيل مع أوامره.
```

هاد الطريقة كتضيف **تعليمات للمحادثة**؛ ما كتثبتش plugin. توفر Python والمكتبات وإرجاع الملفات كيتبدل حسب البيئة والصلاحيات. إلا ما كاينش تنفيذ، تقدر تشغّل البرنامج محلياً بالبيئة المذكورة فالصفحة الرئيسية.

## Plugin محلي فـChatGPT desktop / Codex desktop

المشروع فيه marketplace جاهز:

- `.agents/plugins/marketplace.json`
- `plugins/photo-to-autocad/plugin.json`
- `plugins/photo-to-autocad/skills/draft-cad-from-images/`

افتح مجلد المشروع فبيئة محلية مدعومة من تطبيق ChatGPT desktop. أعد تشغيل التطبيق إذا ما ظهرش marketplace، وافتح **Plugins** واختار **Photo to AutoCAD** من المصدر المحلي، ثم ثبّتو. افتح محادثة جديدة واختار الـskill أو الـplugin بـ`@`.

إذا النسخة أو إعدادات الحساب ما كتبيّنش marketplaces محلية، استعمل طريقة التعليمات أعلاه أو Codex CLI. ما نفترضوش وجود زر لاستيراد ZIP فكل حساب.

## الويب والهاتف والنشر العام

الـplugins المنشورة والمتاحة لحسابك تقدر تستعملها فالسطوح اللي كتدعمها. لكن وجود هاد المستودع فـGitHub **ما كينشرش** الحزمة تلقائياً فدليل Plugins العمومي، ورفع ZIP فمحادثة عادية ما كيحوّلوش لـplugin مثبتة.

هاد الإصدار كيقدّم ملفات قابلة للتحميل وmarketplace محلي وتعليمات محمولة. أي نشر لاحق فالدليل العمومي خاص يتوثق برابط حقيقي للإدراج.

## مثال النتيجة المنتظرة

![معاينة DXF لمثال اللوحة](../examples/plate/preview.png)

طلب الملف الأصلي DXF، ماشي الصورة فقط. للتعامل مع DWG، خاص أداة CAD حقيقية. ما كاين حتى تثبيت لبرنامج AutoCAD ضمن المشروع.

المراجع: [Skills وPlugins](https://learn.chatgpt.com/docs/skills-and-plugins)، [المنصات المدعومة](https://learn.chatgpt.com/docs/plugins)، [marketplace محلي](https://developers.openai.com/plugins/build/plugins).
