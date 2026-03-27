# ./src/services/result_saver.py

import csv


class ResultSaver:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, results: list[dict]) -> None:
        with open(self.file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "url",
                    "method",
                    "status",
                    "latency",
                    "content_length",
                    "error",
                ],
            )
            writer.writeheader()

            for r in results:
                writer.writerow(r.to_dict())
