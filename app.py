from flask import Flask, request, jsonify
import os
import pickle
from dotenv import load_dotenv
from qa_engine import answer_from_book  # ถ้าแยกไปแล้ว (แนะนำให้แยกไว้ใน qa_engine.py)

load_dotenv()
app = Flask(__name__)

@app.route("/botnoi-callback", methods=["POST"])
def botnoi_callback():
    data = request.get_json()
    query = data.get("message", "")
    answer = answer_from_book(query)
    return jsonify({"reply": answer})

# ✅ ถ้ายังไม่ได้แยกออกไปที่ qa_engine.py ก็ใช้ฟังก์ชันนี้ในไฟล์เดียวกันได้:
def answer_from_book(query):
    with open("book_chunks.pkl", "rb") as f:
        book = pickle.load(f)

    # ทำอย่างง่าย: เช็คว่า query อยู่ในเนื้อหา
    joined_book = " ".join(book)  # สมมุติ book เป็น list ของ chunks
    if query.lower() in joined_book.lower():
        return "✅ พบในหนังสือ!"
    else:
        return "❌ ไม่พบคำตอบในไฟล์"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
