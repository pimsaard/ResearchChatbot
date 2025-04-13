import pickle
import os
import requests
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# โหลด .env เพื่ออ่าน API KEY
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# โหลดฐานข้อมูลจากไฟล์
with open("book_chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# ใช้ TF-IDF แปลงเป็นเวกเตอร์
vectorizer = TfidfVectorizer().fit(chunks)
X = vectorizer.transform(chunks)

# หาข้อความที่ใกล้เคียงกับคำถาม
def find_relevant_chunks(query, top_k=3):
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, X).flatten()
    top_indices = scores.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_indices]

# ฟังก์ชันหลักให้ตอบจากหนังสือ
def answer_from_book(query):
    context = "\n\n".join(find_relevant_chunks(query))
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-base",
        headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
        json={"inputs": prompt}
    )

    try:
        return response.json()[0]["generated_text"]
    except Exception as e:
        print("⚠️ HuggingFace API error:", e)
        return "ขออภัย ระบบไม่สามารถตอบคำถามนี้ได้ในขณะนี้"
