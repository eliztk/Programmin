#Завдання 1: Аналізатор лог-файлів
def analyze_log_file(log_file_path):
    try:
        result_dict = {}

        with open(log_file_path, "r", encoding="utf-8") as file:
            for line in file:
                split_result = line.split()
                if len(split_result) >= 9:
                    status_code = split_result[8]  # саме тут код відповіді
                    if status_code.isdigit():
                        if status_code in result_dict:
                            result_dict[status_code] += 1
                        else:
                            result_dict[status_code] = 1

        return result_dict

    except FileNotFoundError:
        print("Source file was not found")
    except IOError:
        print("An error occurred while writing to the output file")

results = analyze_log_file("apache_logs.txt")
print(results)

#Завдання 2: Генератор хешів файлів
import hashlib

def generate_file_hashes(*file_paths):
    result_dict = {}

    for path in file_paths:
        try:
            with open(path, "rb") as file:
                content = file.read()
                file_hash = hashlib.sha256(content).hexdigest()
                result_dict[path] = file_hash

        except FileNotFoundError:
            print("Source file was not found")
        except IOError:
            print("An error occurred while writing to the output file")

    return result_dict

hashes = generate_file_hashes("apache_logs.txt", "result.txt")
print(hashes)

#Завдання 3: Фільтрація IP-адрес з файлу
allowed_ips = ["90.220.199.149", "66.249.73.135", "70.127.254.161"]

def filter_ips(input_file_pass, output_file_pass, allowed_ips):
    try:
        result_dict = {}
        with open (input_file_pass) as file:
            for line in file:
                split_result = line.split()
                ipaddress = split_result[0]
                if ipaddress in allowed_ips:
                    # dict {key=IP: counter}
                    if ipaddress in result_dict:
                        result_dict[ipaddress] += 1
                    else:
                        result_dict[ipaddress] = 1
        print(result_dict)

        with open(output_file_pass, "w") as file:
            for k,v in result_dict.items():
                file.writelines(k + " " + str(v) + "\n")

    except FileNotFoundError:
        print("Source file was not found")
    except IOError:
        print("An error occurred while writing to the output file")

filter_ips("apache_logs.txt", "result.txt", allowed_ips)