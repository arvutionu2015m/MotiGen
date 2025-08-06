import openai
from django.conf import settings
import pdfplumber
import docx

def extract_text_from_file(file):
    if file.name.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() or '' for page in pdf.pages)
    elif file.name.endswith('.docx'):
        doc = docx.Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("Toetatud failivormingud on .pdf ja .docx")


def generate_ai_response(cv_input):
    openai.api_key = settings.OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sa oled professionaalne karjäärinõustaja. Kasutaja sisestab oma CV.\n"
                        "Vasta alati kolmes selges osas markdown-formaadis:\n\n"
                        "## Motivatsioonikiri\n(Täiesti isikupärane ja hästi struktureeritud motivatsioonikiri)\n\n"
                        "## Töösoovitused\n(Nimeta 2-3 sobivat töörolli koos lühikese kirjelduse ja miks need sobivad)\n\n"
                        "## Soovitused CV parandamiseks\n(Konkreetne ja otsekohene tagasiside)"
                    )
                },
                {
                    "role": "user",
                    "content": f"Siin on minu CV info:\n{cv_input}"
                }
            ],
            temperature=0.7,
            max_tokens=1200
        )

        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"⚠️ Tekkis viga AI päringuga: {str(e)}"


