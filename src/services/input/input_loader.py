# ./src/services/input/input_loader.py
from .deps import URLUtils, URLs, pd, logger


class URLInputLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    # ===== PUBLIC PIPELINE =====
    def run(self) -> URLs:
        data = self._load()
        urls = self._extract(data)
        total = len(urls)
        urls = self._deduplicate(urls)
        duplicates = total - len(urls)
        urls, invalid = self._validate(urls)
        valid = len(urls)
        logger.storage.load_summary(total, valid, duplicates, invalid)
        return urls

    # ===== STEPS =====
    def _load(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.file_path, header=None)

        except FileNotFoundError as e:
            logger.storage.load_failure("file not found", self.file_path)
            raise e
        except pd.errors.EmptyDataError as e:
            logger.storage.load_failure("empty file", self.file_path)
            raise e
        except pd.errors.ParserError as e:
            logger.storage.load_failure("parser error", self.file_path)
            raise e
        except Exception as e:
            logger.storage.load_failure(str(e), self.file_path)
            raise e

    def _extract(self, df: pd.DataFrame) -> URLs:
        return (
            df.iloc[:, 0]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

    def _deduplicate(self, urls: URLs) -> URLs:
        # preserves order (faster than manual loop)
        return list(dict.fromkeys(urls))

    def _validate(self, urls: URLs) -> tuple[URLs, int]:
        valid = []
        invalid = 0

        for url in urls:
            if URLUtils.is_valid(url):
                valid.append(url)
            else:
                invalid += 1

        return valid, invalid

    # ===== OPTIONAL API =====
    def get_urls(self) -> URLs:
        return self.run()
