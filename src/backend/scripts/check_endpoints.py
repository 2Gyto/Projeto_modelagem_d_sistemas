import httpx

def main():
    try:
        r = httpx.get('http://127.0.0.1:8000/api/v1/health', timeout=10.0)
        print('HEALTH STATUS:', r.status_code)
        print(r.text)
    except Exception as e:
        print('HEALTH ERROR', e)

    try:
        r2 = httpx.get('http://127.0.0.1:8000/app', timeout=10.0)
        print('\nAPP STATUS:', r2.status_code)
        print(r2.text[:500])
    except Exception as e:
        print('APP ERROR', e)

if __name__ == '__main__':
    main()
