from flask import Flask, request, jsonify
from qa_engine import answer_from_book
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
    return "Research Chatbot is running."

@app.route("/botnoi-callback", methods=["POST"])
def botnoi_callback():
    data = request.get_json()
    query = data.get("message", "")
    answer = answer_from_book(query)  # อ่านจาก .pkl ซึ่งมาจากไฟล์ .txt
    def answer_from_book(query):
    with open("Research Writing AI.txt", "r", encoding="utf-8") as f:
        book = f.read()
    # ทำอย่างง่าย: เช็คว่า query อยู่ตรงไหน
    if query.lower() in book.lower():
        return "✅ พบในหนังสือ!"
    else:
        return "ขออภัย ไม่พบคำตอบในไฟล์นี้"

    return jsonify({"reply": answer})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
