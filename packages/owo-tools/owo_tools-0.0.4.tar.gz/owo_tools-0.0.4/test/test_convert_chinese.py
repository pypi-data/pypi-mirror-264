import pytest
from owo_tools.convert_chinese import convert_chinese
import os

# 假設測試檔案和指令碼在同一目錄下
BASE_DIR = os.path.dirname(__file__)
print(BASE_DIR)
FIXTURES_DIR = os.path.join(BASE_DIR, 'fixtures')
EXPECTED_DIR = os.path.join(BASE_DIR, 'expected')
OUTPUT_DIR = os.path.join(BASE_DIR)

@pytest.fixture
def setup_test_files():
    input_path = os.path.join(FIXTURES_DIR, 'convert_chinese_s.txt')
    output_path = os.path.join(OUTPUT_DIR, 'convert_chinese_t.txt')
    expected_path = os.path.join(EXPECTED_DIR, 'convert_chinese_s2twp.txt')
    # 清理上一次測試可能遺留的輸出檔案
    if os.path.exists(output_path):
        os.remove(output_path)
    yield input_path, output_path, expected_path
    # 測試後清理輸出檔案，如果需要保留輸出檔案，則註釋掉下面這行
    os.remove(output_path)

def test_s2twp_conversion(setup_test_files):
    input_path, output_path, expected_path = setup_test_files
    convert_chinese(input_path, output_path, 's2twp', False)
    with open(output_path, 'r', encoding='utf-8') as output_file, \
         open(expected_path, 'r', encoding='utf-8') as expected_file:
        output_content = output_file.read()
        expected_content = expected_file.read()
    assert output_content == expected_content, "The conversion output does not match the expected output."
