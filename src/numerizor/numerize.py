from typing import Optional


def numerize(string_number: str) -> Optional[int]:
    # 60 sufixes
    conversion_dictionary: dict = {
        "K": 1e3, "M": 1e6, "B": 1e9
    }
    num = None
    for k, v in conversion_dictionary.items():
        if k in string_number:
            num = int(string_number.split(k)[0]) * v
    if num is None:
        try:
            num = int(string_number.replace(',', ''))
        except Exception as e:
            print(e)
    return num
