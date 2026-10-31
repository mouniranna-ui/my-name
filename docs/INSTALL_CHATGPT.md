# Photo to AutoCAD داخل ChatGPT

[الصفحة الرئيسية](../README.md) · **[ابدأ بلا تثبيت](CHATGPT_START.md)** · [English](../README.en.md)

![طرق استعمال Photo to AutoCAD داخل ChatGPT](images/chatgpt-steps.svg)

## 1. الاستعمال المباشر من الويب أو الهاتف

افتح [ChatGPT](https://chatgpt.com/)، زيد صورة الرسم، وانسخ [الطلب الجاهز](CHATGPT_START.md). تقدر تزيد [ملف TXT الشامل](../prompts/Photo-to-AutoCAD-ChatGPT.txt) باش تعطيه التعليمات والأدوات فمرفق واحد. ما تحتاجش تثبيت فالحاسوب.

```text
تبع ملف Photo to AutoCAD المرفق وقرا هاد الرسم.
صنع DXF قابل للتعديل بجميع القياسات المقروءة والعبارات، ومعاه PDF.
راجع الملفات فعلياً وبيّن ليا شنو باقي ناقص أو غير واضح.
```

هاد المسار كيعطي تعليمات وأدوات للمحادثة. إنشاء الملفات كيحتاج قراءة الصور، تنفيذ Python وإمكانية إرجاع الملفات. إلا هاد الإمكانيات ما متوفراش، النتيجة تكون جدول القياسات وبرنامج كامل قابل للتشغيل. [شرح بالصور وخطوات بسيطة](CHATGPT_START.md).

## 2. Plugin داخل دليل ChatGPT

الاسم: **Photo to AutoCAD**. الحزمة كتحتوي skill `draft-cad-from-images`، التعليمات، أدوات DXF/PDF والأيقونة المختارة. ما كتحتاجش حساباً فخدمة خارجية خاصة بالمشروع، وما فيهاش MCP server.

**الحالة الحالية: الحزمة مبنية ومتاحة للتحميل؛ لم يتم تقديمها أو نشرها بعد فالدليل العمومي.** ما كاينش رابط «ثبت الآن» للإضافة حتى يتوثق الإدراج الحقيقي. [حالة النشر والتجهيز](PLUGIN_PUBLICATION.md).

من بعد الموافقة والنشر، المستخدم يفتح **Plugins**، يلقى الإضافة، يثبتها، ويختارها أو يختار الـskill باستعمال `@`. هادي خطوات ما بعد النشر، ماشي إعلان أن الإدراج موجود دابا. إعدادات الحساب والمنصة كتحدد الأدوات المتاحة.

## 3. Plugin محلي فبيئة desktop مدعومة

المشروع فيه marketplace جاهز:

- `.agents/plugins/marketplace.json`
- `plugins/photo-to-autocad/plugin.json`
- `plugins/photo-to-autocad/skills/draft-cad-from-images/`

فتح مجلد المشروع فبيئة محلية مدعومة من ChatGPT desktop. أعد تشغيل التطبيق إذا ما ظهرش marketplace، ثم افتح **Plugins** واختار **Photo to AutoCAD** من المصدر المحلي وثبّتو. افتح محادثة جديدة واختار الـskill أو الـplugin بـ`@`.

إلا ما ظهرتش marketplaces محلية فنسختك، استعمل [الطريقة المباشرة](CHATGPT_START.md) أو [Codex CLI](INSTALL_CODEX.md). رفع ZIP فمحادثة عادية ما كيُثبتش Plugin، والنشر فـGitHub ما كيديرش إدراج تلقائي فدليل ChatGPT.

## مثال المخرجات

![معاينة مثال DXF](../examples/plate/preview.png)

طلب DXF الأصلي وPDF، وراجع ملاحظة المعلومات الناقصة. DWG كيحتاج تطبيق CAD أو محوّل حقيقي. المشروع ما كيثبتش AutoCAD وما كيمنحش رخصتو.

المراجع الرسمية: [Plugins](https://learn.chatgpt.com/docs/plugins) · [تغليف الإضافة](https://developers.openai.com/plugins/build/plugins) · [النشر والمراجعة](https://developers.openai.com/plugins/deploy/submission).
