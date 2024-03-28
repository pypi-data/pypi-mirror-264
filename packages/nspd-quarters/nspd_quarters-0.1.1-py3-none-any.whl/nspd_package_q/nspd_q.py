import requests
import json
import logging
import time
import warnings
import argparse
from urllib3.exceptions import InsecureRequestWarning

def parse_args():
    parser = argparse.ArgumentParser(description='Fetch and save data from nspd.gov.ru.')
    parser.add_argument('--num', required=True, help='Кадастровый номер')
    parser.add_argument('--output_directory', required=True, help='Путь к директории для сохранения файлов')
    return parser.parse_args()

def collect_data(num, output_filename, url, headers):
    pageNumber = 1
    pageSize = 25
    cad_nums = []  # Собираем номера в список
    while True:
        data = {"text": num, "pageNumber": pageNumber, "pageSize": pageSize}
        response = requests.post(url, headers=headers, json=data, verify=False)
        if response.status_code == 200:
            response_data = response.json()
            total_pages = response_data.get('metadata', {}).get('totalPages', 0)
            cad_nums.extend([result['cad_num'] for result in response_data.get('result', []) if 'cad_num' in result])
            logging.info(f"Страница {pageNumber}/{total_pages} обработана.")
            if pageNumber >= total_pages:
                break
            pageNumber += 1
            time.sleep(1)
        else:
            logging.error(f"Ошибка при выполнении запроса. Код состояния: {response.status_code}")
            break

    # Записываем собранные данные в файл
    with open(output_filename, 'w') as file:
        for cad_num in cad_nums:
            file.write(f"{cad_num}\n")
    logging.info(f"Данные сохранены в файл: {output_filename}")

def main():
    warnings.filterwarnings('once', category=InsecureRequestWarning)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    args = parse_args()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://nspd.gov.ru',
        'Referer': 'https://nspd.gov.ru/map',
    }

    url = 'https://nspd.gov.ru/map_api/s_search/search'

    # Путь к файлу для сохранения результатов
    output_filename = args.output_directory + args.num.replace(":", "_") + "_quarters.txt"

    # Запускаем процесс сбора данных
    collect_data(args.num, output_filename, url, headers)

if __name__ == '__main__':
    main()
