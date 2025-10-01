import io
import re
from typing import List, Tuple

import streamlit as st
from pypdf import PdfReader
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

# Make langdetect deterministic
DetectorFactory.seed = 0


def extract_text_from_pdf(file_bytes: bytes) -> str:
	"""Extract text from a PDF file given as bytes using pypdf.

	Returns an empty string if no text is found or on failure.
	"""
	try:
		reader = PdfReader(io.BytesIO(file_bytes))
		texts: List[str] = []
		for page in reader.pages:
			try:
				texts.append(page.extract_text() or "")
			except Exception:
				# Skip pages that fail to extract
				continue
		return "\n".join(t.strip() for t in texts if t)
	except Exception:
		return ""


def split_sentences(text: str) -> List[str]:
	"""Split text into sentences for both English and Korean heuristically."""
	if not text:
		return []

	# Normalize whitespace
	text = re.sub(r"\s+", " ", text).strip()

	# Heuristic: split on end punctuation for English/Korean/Chinese
	pattern = r"(?<=[\.!?。！？])\s+"
	sentences = re.split(pattern, text)

	# Additionally break on frequent Korean sentence endings like '다.' if not already caught
	refined: List[str] = []
	for s in sentences:
		parts = re.split(r"(?<=다\.)\s+", s)
		refined.extend(parts)

	# Cleanup
	refined = [s.strip() for s in refined if s and len(s.strip()) > 1]
	return refined


def tokenize_words(text: str) -> List[str]:
	"""Very light word tokenizer that works for Latin scripts and approximates for CJK/Korean.

	For Korean, we approximate by splitting on spaces and punctuation (no morphological analysis).
	"""
	if not text:
		return []
	# Lowercase for English-like languages; keep others as-is
	lowered = text.lower()
	# Replace punctuation with spaces
	normalized = re.sub(r"[^\w가-힣一-龯ぁ-ゔァ-ヴー々〆〤]+", " ", lowered)
	# Split on whitespace
	return [w for w in normalized.split() if w]


def get_stopwords() -> set:
	# Minimal English and Korean stopwords to avoid extra dependencies
	english = {
		"the","is","in","at","of","and","a","to","for","on","with","as","by","an","be","or","it","that","this","from","are","was","were","but","not","have","has","had","we","you","they","their","our","your","can","will","would","should","could","about",
	}
	korean = {
		"그리고","그러나","하지만","또한","및","등","이는","그","이","저","것","수","있는","있는지","있다","하였다","했다","으로","에서","에게","까지","부터","보다","또","또는","때문에","즉","또한","그러므로","따라서","하며","하며","하며","우리","너","여러","등의"," 등의",
	}
	return set(list(english) + list(korean))


def build_word_frequencies(sentences: List[str]) -> dict:
	stopwords = get_stopwords()
	frequencies: dict = {}
	for sentence in sentences:
		for word in tokenize_words(sentence):
			if word in stopwords:
				continue
			frequencies[word] = frequencies.get(word, 0) + 1
	# Normalize frequencies
	if not frequencies:
		return {}
	max_freq = max(frequencies.values())
	for word in list(frequencies.keys()):
		frequencies[word] = frequencies[word] / max_freq
	return frequencies


def score_sentences(sentences: List[str], word_freq: dict) -> List[Tuple[str, float, int]]:
	"""Return list of (sentence, score, index)."""
	scored: List[Tuple[str, float, int]] = []
	for idx, sentence in enumerate(sentences):
		if not sentence.strip():
			continue
		words = tokenize_words(sentence)
		if not words:
			continue
		score = sum(word_freq.get(w, 0.0) for w in words) / (len(words) + 1e-6)
		scored.append((sentence, score, idx))
	return scored


def summarize_text(text: str, max_sentences: int = 5) -> str:
	"""Simple extractive summarization by word-frequency scoring.

	- Scores sentences by average of normalized word frequencies
	- Selects top-K sentences while preserving original order
	"""
	sentences = split_sentences(text)
	if not sentences:
		return ""
	word_freq = build_word_frequencies(sentences)
	if not word_freq:
		# Fallback: return first K sentences
		return " " .join(sentences[:max(1, max_sentences)])
	# Score and pick top K
	scored = score_sentences(sentences, word_freq)
	if not scored:
		return " " .join(sentences[:max(1, max_sentences)])
	# Sort by score desc, then take top K, and reorder by original index
	top_k = sorted(sorted(scored, key=lambda x: x[1], reverse=True)[:max(1, max_sentences)], key=lambda x: x[2])
	ordered_sentences = [s for s, _, _ in top_k]
	return " " .join(ordered_sentences)


def format_stats(text: str) -> Tuple[int, int, int]:
	chars = len(text)
	words = len(tokenize_words(text))
	sents = len(split_sentences(text))
	return chars, words, sents


def detect_language(text: str) -> str:
	"""Detect language code like 'en', 'ko'. Returns 'unknown' on failure."""
	try:
		if not text or len(text.strip()) < 20:
			return "unknown"
		return detect(text[:5000])
	except Exception:
		return "unknown"


def chunk_text(text: str, max_chars: int = 4500) -> List[str]:
	chunks: List[str] = []
	start = 0
	length = len(text)
	while start < length:
		end = min(start + max_chars, length)
		# try to break on whitespace for nicer chunks
		if end < length:
			ws = text.rfind(" ", start, end)
			if ws != -1 and ws - start > 500:  # avoid tiny tail
				end = ws
		chunks.append(text[start:end])
		start = end
	return chunks


def translate_to_korean(text: str) -> str:
	"""Translate long English text to Korean by chunking."""
	translator = GoogleTranslator(source="auto", target="ko")
	parts = chunk_text(text)
	translated_parts: List[str] = []
	for part in parts:
		try:
			translated_parts.append(translator.translate(part))
		except Exception:
			# If one chunk fails, keep original to avoid data loss
			translated_parts.append(part)
	return "\n".join(translated_parts)


def main() -> None:
	st.set_page_config(page_title="PDF 요약기", page_icon="📝", layout="centered")
	st.title("📝 PDF 요약기 (Streamlit)")
	st.write("PDF 파일을 업로드하면 내용을 추출하여 간단히 요약해 드립니다. 인터넷 연결이나 대형 모델 없이 로컬에서 동작합니다.")

	with st.sidebar:
		st.header("설정")
		max_sentences = st.slider("요약 문장 수", min_value=2, max_value=15, value=5, step=1)
		st.caption("간단한 빈도 기반 추출 요약입니다. 원문 품질과 언어에 따라 결과가 달라질 수 있습니다.")

	uploaded = st.file_uploader("PDF 파일을 선택하세요", type=["pdf"], accept_multiple_files=False)

	if uploaded is None:
		st.info("왼쪽 설정에서 요약 길이를 선택하고, PDF를 업로드하세요.")
		return

	# Read bytes first (works for large files as well; Streamlit provides a buffer)
	file_bytes = uploaded.read()
	with st.spinner("PDF에서 텍스트 추출 중..."):
		text = extract_text_from_pdf(file_bytes)

	if not text or len(text.strip()) == 0:
		st.error("텍스트를 추출할 수 없습니다. 스캔본(PDF 이미지)일 수 있습니다. 텍스트 기반 PDF를 사용해 주세요.")
		return

	# 언어 감지
	detected_lang = detect_language(text)
	if detected_lang == "en":
		st.info("영어 문서로 감지되었습니다. 아래에서 한국어 번역 파일을 생성할 수 있습니다.")
		if st.button("한글 번역 파일 생성"):
			with st.spinner("영→한 번역 중..."):
				translated = translate_to_korean(text)
			st.success("번역이 완료되었습니다. 아래 버튼으로 저장하세요.")
			st.download_button(
				"번역 텍스트 저장 (TXT)",
				data=translated.encode("utf-8"),
				file_name="translated_ko.txt",
				mime="text/plain",
			)

	orig_chars, orig_words, orig_sents = format_stats(text)
	st.subheader("원문 통계")
	col1, col2, col3 = st.columns(3)
	col1.metric("문자 수", f"{orig_chars:,}")
	col2.metric("단어 수(대략)", f"{orig_words:,}")
	col3.metric("문장 수(대략)", f"{orig_sents:,}")

	if st.button("요약하기", type="primary"):
		with st.spinner("요약 생성 중..."):
			summary = summarize_text(text, max_sentences=max_sentences)
		if not summary:
			st.warning("요약 결과가 비어 있습니다. 요약 문장 수를 늘려보세요.")
			return

		st.subheader("요약")
		st.text_area("요약 결과", value=summary, height=240)
		st.download_button("요약 저장 (TXT)", data=summary.encode("utf-8"), file_name="summary.txt", mime="text/plain")

		sum_chars, sum_words, sum_sents = format_stats(summary)
		st.caption(f"요약 통계 — 문자 {sum_chars:,}, 단어 {sum_words:,}, 문장 {sum_sents:,}")


if __name__ == "__main__":
	main()


