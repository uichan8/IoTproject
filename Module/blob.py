import os
import subprocess
import time
import glob

def _delete_files_in_folder(folder_path):
    # 지정된 폴더 내의 모든 파일에 대한 경로를 가져옵니다.
    files = glob.glob(os.path.join(folder_path, '*'))
    
    # 각 파일을 순회하며 삭제합니다.
    for file in files:
        try:
            # 파일인 경우에만 삭제합니다.
            if os.path.isfile(file):
                os.remove(file)
                print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

def load(path = "./Sensor_Data"):
    current_time = time.localtime()
    year = current_time.tm_year
    month = current_time.tm_mon
    day = current_time.tm_mday

    _delete_files_in_folder(path)

    command = [
    'azcopy',
    'copy',
    f'https://sensordatablob.blob.core.windows.net/sensordatacontainer/temp/{year}/{month}/{day}/*',
    path,
    '--recursive']
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = result.stdout.decode()
    errors = result.stderr.decode()
    #print("Output:", output)
    if errors:
        print("Errors:", errors)

    json_path = os.path.join(path,os.listdir(path)[0])
    with open(json_path, 'r') as file:
        data = file.readlines()

    new_data = "["
    for d in data:
        new_data+=(d + ',')
    new_data = new_data[:-1] + ']'

    with open(json_path, 'w') as file:
        file.write(new_data)
    
def upload(account = 'sensordatablob', container = 'surmary', blob_path = 'gpt.txt', local_path = './Text/gpt.txt'):
    command = [
        'az',
        'storage',
        'blob',
        'upload',
        '--account-name',
        account,
        '--container-name',
        container,
        '--name',
        blob_path,
        '--file',
        local_path,
        '--overwrite']

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = result.stdout.decode()
    errors = result.stderr.decode()
    print("Output:", output)
    if errors:
        print("Errors:", errors)


if __name__ == '__main__':
    while True:
        try:
            load()
        except:
            continue
        time.sleep(60)
        
