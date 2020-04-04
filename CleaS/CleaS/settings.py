API_ENDPOINT = """https://api.wit.ai/speech"""
TOKEN = 'KGGUQ7FLCEPEB47MH2UUIVKQICAKZL2H'
ALLOWED_SYMBOLS = [x for x in filter(lambda key: key is not None, [chr(x) if not [i for i in range(91, 97)].__contains__(x) else None for x in range(65, 123)])]
if __name__ == "__main__":
    print(API_ENDPOINT)
    print(TOKEN)
    print(ALLOWED_SYMBOLS)