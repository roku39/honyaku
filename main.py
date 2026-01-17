import os
from PIL import Image
import pytesseract
import deepl

# ======== 設定 ========
INPUT_FOLDER = "screenshots"      # スクショ画像を入れるフォルダ
OUTPUT_FILE = "translated_book.md" # 出力Markdownファイル
DEEPL_API_KEY = os.environ["DEEPL_AUTH_KEY"]

# Tesseractパス（Macは不要／Windowsのみ必要）
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ======== DeepL初期化 ========
translator = deepl.Translator(DEEPL_API_KEY)

# ======== OCR + 翻訳処理 ========
with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
    f_out.write("# Translated Book\n\n")

    for i, filename in enumerate(sorted(os.listdir(INPUT_FOLDER)), start=1):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        img_path = os.path.join(INPUT_FOLDER, filename)
        print(f"OCR中: {filename}")

        # 英文抽出
        text = pytesseract.image_to_string(Image.open(img_path), lang="eng")
        if not text.strip():
            continue

        # Markdownページタイトル
        f_out.write(f"\n## Page {i}\n\n")

        # 翻訳（段落ごと）
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        for paragraph in paragraphs:
            try:
                # DeepL翻訳（英語→日本語）
                result = translator.translate_text(paragraph, source_lang="EN", target_lang="JA")
                f_out.write(f"**EN:** {paragraph}\n\n")
                f_out.write(f"**JA:** {result.text}\n\n")
            except Exception as e:
                f_out.write(f"**EN:** {paragraph}\n\n")
                f_out.write(f"**JA:** （翻訳エラー: {e}）\n\n")

print(f"\n✅ 完了: {OUTPUT_FILE} に保存しました！")
