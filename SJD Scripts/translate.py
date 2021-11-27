from deep_translator import (GoogleTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeepL,
                             QCRI,
                             single_detection,
                             batch_detection)

sjd_api_key = "a2ee4e0830ec480b8c9e8c3582e95523"
docPath = "C:\Hugo\Sites\Life For Liberia\content\English\Teaching\Becoming a Christian\Baptism.md"
translated = MicrosoftTranslator(api_key=sjd_api_key, source = 'english', target='french', region ='westeurope').translate_file(docPath)
print(translated)