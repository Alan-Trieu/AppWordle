# network.py
import requests

class WordChecker:
    def __init__(self):
        self._word_cache = {}

    def check_word_api(self, word):
        """Kiểm tra từ vựng qua API và lưu cache"""
        word = word.lower()
        
        # Nếu đã kiểm tra rồi thì trả về kết quả cũ
        if word in self._word_cache:
            return self._word_cache[word] 

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            res = requests.get(url, timeout=2) # Tăng timeout lên một chút
            exists = res.status_code == 200
        except:
            exists = False

        self._word_cache[word] = exists
        return exists