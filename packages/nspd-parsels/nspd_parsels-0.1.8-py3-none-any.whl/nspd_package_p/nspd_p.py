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

def save_to_files(output_directory, num, results_by_class):
    for class_name, cad_nums in results_by_class.items():
        output_filename = output_directory + num.replace(":", "_") + f"_{class_name.replace('RR:', '')}.txt"
        with open(output_filename, 'a') as file:
            for cad_num in cad_nums:
                file.write(f"{cad_num}\n")
        logging.info(f"Данные по классу {class_name} добавлены в файл: {output_filename}")

def collect_data(quarter, headers, results_by_class):
    url = 'https://nspd.gov.ru/map_api/s_search/search'
    pageNumber = 1
    pageSize = 25

    while True:
        data = {"text": quarter, "pageNumber": pageNumber, "pageSize": pageSize}
        response = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
        if response.status_code == 200:
            response_data = response.json()
            total_pages = response_data.get('metadata', {}).get('totalPages', 0)

            for result in response_data.get('result', []):
                class_name = result.get('className', 'Unknown')
                cad_num = result.get('cad_num')
                if cad_num:
                    if class_name not in results_by_class:
                        results_by_class[class_name] = []
                    results_by_class[class_name].append(cad_num)

            logging.info(f"Страница {pageNumber} из {total_pages} обработана для квартала: {quarter}")
            if pageNumber >= total_pages:
                break
            pageNumber += 1
            time.sleep(1)
        else:
            logging.error(f"Ошибка при выполнении запроса. Код состояния: {response.status_code}")
            break

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

    results_by_class = {}

    cad_class = "parsels"  # Это значение можно также сделать параметром командной строки, если необходимо

    if cad_class == "parsels":
        input_filename = args.output_directory + args.num.replace(":", "_") + "_quarters.txt"
        with open(input_filename, 'r') as file:
            quarters = [line.strip() for line in file]

        for index,quarter in enumerate(quarters):
            logging.info(f"Обработка квартала: {quarter} ({index + 1}/{len(quarters)})")
            collect_data(quarter, headers, results_by_class)

        save_to_files(args.output_directory, args.num, results_by_class)

if __name__ == '__main__':
    main()
