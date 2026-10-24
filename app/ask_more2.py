"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key
from google.genai import types

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"

history = []
def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    part = types.Part.from_text(text=question) # ユーザーの質問文は、そのままでは単なる文字列です。これを「発話の中身の部品」に変えます。
    history.append(types.Content(role="user", parts=[part]))
    response = client.models.generate_content(model=MODEL, contents=history) # APIを呼んでいる

    part = types.Part.from_text(text=response.text) 
    history.append(types.Content(role="model", parts=[part]))

    usage = response. usage_metadata
    print(f"[usage] input tokens: {usage.prompt_token_count}, output tokens: {usage.candidates_token_count}")

    return response.text

# argparse は起動時に1回だけ質問を受け取る仕組み。ループの中で毎回受け取るにはinput() を使う。
def main() -> None:
    print(f"[model] {MODEL}")
    try:
        while True:
            q = input("> ")        
            if q == "exit":              
                break
            print(ask(q))  
            
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)
    

if __name__ == "__main__":
    main()
