import time
import json
import logging
from git_test import TestFramework
from scenario import InitGitRepo, MergeToMain, ResetCheck

def log_error(scenario_name, error_message):
    """紀錄錯誤信息到錯誤日志"""
    with open("error.log", "a") as log_file:
        log_file.write(f"[SCENARIO: {scenario_name}] {error_message}\n")


def run_scenario(scenario_class: TestFramework, method, scenario_name, results):
    """執行一個測試場景"""
    prompt_log = []
    retry_count = 0
    error_messages = []
    elapseds = []
    success = False

    while True:
        scenario = scenario_class()
        task_description, checkpoints = scenario.task

        print(f"開始 {method} {scenario_name}\n")
        print(task_description)

        try:
            scenario.action()
            input("確保測試環境正確後，按 Enter 開始執行測試。")
            start_time = time.time()
            for idx, checkpoint in enumerate(checkpoints):
                input(f"檢核點 {idx + 1}: {checkpoint}，按 Enter 檢核。")
                scenario.valid()
                print("檢核通過！\n")

            end_time = time.time()
            elapsed_time = end_time - start_time
            elapseds.append(elapsed_time)
            if method == "使用 GitGPT 插件輔助":
                prompt = input("請輸入第一個的 prompt: ")
                prompt_log.append(prompt)
            print(f"完成 {method} {scenario_name}。耗時: {elapsed_time:.2f} 秒。\n\n")
            success = True

            return

        except Exception as e:
            error_message = str(e)
            print(f"發生錯誤: {error_message}")
            log_error(scenario_name, error_message)
            error_messages.append(error_message)
            end_time = time.time()
            elapsed_time = end_time - start_time
            elapseds.append(elapsed_time)

            retry = input("是否重試？(y/n): ").strip().lower()

            if method == "使用 GitGPT 插件輔助":
                prompt = input("請輸入第一個的 prompt: ")
                prompt_log.append(prompt)
            if retry != "y":
                break
            retry_count += 1
        finally:
            results[scenario_name][method] = {
                "elapsed_time": elapseds,
                "retry_count": retry_count,
                "error_log": error_messages,
                "success": success,
                "prompts": prompt_log if method == "使用 GitGPT 插件輔助" else None,
            }
            print("----------------------------------------------------------\n")


def main():
    logging.basicConfig(filename="error.log", level=logging.ERROR)
    scenarios = [
        (InitGitRepo, "情境 1: 初始化 Git 儲存庫"),
        (MergeToMain, "情境 2: 將 feature 分支合併到 main"),
        (ResetCheck, "情境 3: 回到前兩個 commit 並檢查程式碼後返回"),
    ]

    results = {}

    for scenario_class, scenario_name in scenarios:
        results[scenario_name] = {}
        print(f"\n===== 開始測試 {scenario_name} =====\n")

        for method in ["自行完成", "使用 GitGPT 插件輔助"]:
            run_scenario(scenario_class, method, scenario_name, results)

    print("恭喜！測試結束！，請到 https://forms.gle/L1EvJmd91rKZ4MoSA 作答問卷，感謝您。")

    with open("submit.json", "w") as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
