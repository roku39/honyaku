from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import re

# 入力（DeepL翻訳済みMarkdown）
INPUT_FILE = "para-translated_book.md"
# 出力PDF
OUTPUT_FILE = "para-translated_book.pdf"

# 日本語フォントを登録
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

# スタイル設定
styles = getSampleStyleSheet()
style_en = ParagraphStyle(
    'English',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.black,
)
style_ja = ParagraphStyle(
    'Japanese',
    parent=styles['Normal'],
    fontName='HeiseiMin-W3',  # 登録された日本語フォント
    fontSize=10,
    leading=14,
    textColor=colors.darkblue,
)

# ページ設定
doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
elements = []

# Markdownの内容を読み込み
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# Markdown内の "EN:" と "JA:" ペアを抽出
pairs = re.findall(r"\*\*EN:\*\*\s*(.*?)\n\n\*\*JA:\*\*\s*(.*?)\n", content, re.DOTALL)

current_page = ""
for en_text, ja_text in pairs:
    # 空行削除・整形
    en_text = en_text.strip().replace("\n", " ")
    ja_text = ja_text.strip().replace("\n", " ")

    # 二段組み（左＝英語、右＝日本語）
    table_data = [[Paragraph(en_text, style_en), Paragraph(ja_text, style_ja)]]
    table = Table(table_data, colWidths=[8.5*cm, 8.5*cm])
    table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LINEBELOW", (0,0), (-1,-1), 0.25, colors.grey),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 6))

# PDF生成
doc.build(elements)
print(f"✅ 完了！PDFファイルを生成しました → {OUTPUT_FILE}")
