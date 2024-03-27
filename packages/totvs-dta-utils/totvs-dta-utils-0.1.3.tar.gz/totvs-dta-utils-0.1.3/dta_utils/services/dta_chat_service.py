import os
from typing import List, Optional


class DtaChatService:

    @classmethod
    def serve_chat(
        cls,
        api_config: Optional[dict] = None,
        sample_questions: Optional[List[str]] = None,
    ) -> str:
        html = cls.read_chat()

        html = html.replace(
            "/* API_CONFIG */",
            f"{api_config or cls.chat_api_config()};",
        )

        if sample_questions and len(sample_questions):
            html = html.replace(
                "/* SAMPLE_QUESTIONS */",
                f"{sample_questions};",
            )

        return html

    @classmethod
    def chat_api_config(cls) -> dict:
        baseUrl = "."

        _str = """{
            "apiInit": {
                "url": "{baseUrl}/welcome",
                "headers": {
                    "X-User-Auth": "localbypass",
                },
            },
            "apiMessage": {
                "url": "{baseUrl}/completion",
                "method": "POST",
            },
            "apiAudioTranscript": {
                "url": "{baseUrl}/audio",
                "method": "POST",
            },
            "apiFeedback": {
                "url": "{baseUrl}/feedback",
                "method": "POST",
            },
        }"""

        return _str.replace("{baseUrl}", baseUrl)

    @classmethod
    def read_chat(cls):
        file_path = "./assets/dta_chat.html"

        docs_path = os.path.join(os.path.dirname(__file__), file_path)

        with open(docs_path, "r") as file:
            html = file.read()

        return html
