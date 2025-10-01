from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from datetime import timedelta
import os


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Secret key for session management
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-me")
    # Make session last a bit longer for chat continuity
    app.permanent_session_lifetime = timedelta(days=7)

    # Enable CORS for development (Live Server on 127.0.0.1:5500)
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}},
        supports_credentials=True,
    )

    @app.before_request
    def make_session_permanent() -> None:
        session.permanent = True

    def get_history() -> list:
        history = session.get("history")
        if history is None:
            history = []
            session["history"] = history
        return history

    def bot_reply(user_message: str) -> str:
        # Very simple rule-based bot for demo purposes.
        text = (user_message or "").strip().lower()
        if not text:
            return "안녕하세요! 무엇을 도와드릴까요?"
        if any(greet in text for greet in ["안녕", "hello", "hi", "ㅎㅇ"]):
            return "안녕하세요! 챗봇입니다. 무엇을 도와드릴까요?"
        if "이름" in text:
            return "저는 간단한 플라스크 챗봇이에요."
        if "지워" in text or "초기화" in text or "reset" in text:
            session["history"] = []
            return "대화 기록을 초기화했어요."
        return f"방금 하신 말씀은 이렇게 이해했어요: '{user_message}'. 더 자세히 알려주실래요?"

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/history")
    def api_history():
        return jsonify({"history": get_history()})

    @app.post("/api/chat")
    def api_chat():
        payload = request.get_json(silent=True) or {}
        user_message = payload.get("message", "")

        history = get_history()
        history.append({"role": "user", "content": user_message})

        reply = bot_reply(user_message)
        history.append({"role": "assistant", "content": reply})

        session["history"] = history

        return jsonify({"reply": reply, "history": history})

    @app.post("/api/reset")
    def api_reset():
        session["history"] = []
        return jsonify({"ok": True})

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=True)


