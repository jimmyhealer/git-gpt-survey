import os
import shutil
import subprocess
import logging


def run_command(command, cwd=None):
    """
    執行 Shell 或 Bash 指令，並回傳執行結果。

    Args:
        command (str): 要執行的指令。
        cwd (str, optional): 指令執行的目錄。如果為 None，則使用當前目錄。

    Returns:
        str: 指令執行的標準輸出與錯誤輸出的合併結果。
    """
    try:
        result = subprocess.run(
            command, cwd=cwd, shell=True, text=True, capture_output=True
        )
        if result.returncode != 0:
            logging.warning(f"Error executing command: {result.stderr}")

        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        logging.error(f"Exception occurred while executing command: {e}")
        return str(e)


class Scenario:
    MERGE_TO_MAIN = "merge_to_main"
    FILE_DELETION = "file_deletion"
    LOOKUP_WHO_CHANGED = "lookup_who_changed"


class TestFramework:
    def __init__(self, repo_path=None):
        self.repo_path = "./test_git_repo" if repo_path == None else repo_path
        self.actions = []  # 儲存場景操作
        self.validations = [[]]  # 儲存驗證條件
        self.validation_add_order = 0
        self.validation_run_order = 0

        self.task = self.scenario()

    def run_command(self, command):
        stdout, _ = run_command(command, cwd=self.repo_path)
        return stdout.strip()

    def scenario(self):
        """定義場景，由子類實現"""
        raise NotImplementedError("Subclasses must implement scenario.")

    def valid(self):
        """執行驗證條件"""
        for validation in self.validations[self.validation_run_order]:
            validation()
        self.validation_run_order += 1

    def add_validation(self, validation):
        self.validations[self.validation_add_order].append(validation)

    def add_validation_order(self):
        self.validation_add_order += 1
        self.validations.append([])

    def action(self):
        """執行所有操作並驗證"""
        for action in self.actions:
            action()
        return self.task

    # 操作聲明方法
    def init_directory(self):
        def action():
            if os.path.exists(self.repo_path):
                logging.warning(
                    f"Directory {self.repo_path} already exists. Deleting and recreating."
                )
                shutil.rmtree(self.repo_path)
            os.makedirs(self.repo_path)

        self.actions.append(action)
        return self

    def git_init(self):
        def action():
            self.run_command("git init")

        self.actions.append(action)
        return self

    def write_file(self, content, file):
        def action():
            with open(os.path.join(self.repo_path, file), "w") as f:
                f.write(content)

        self.content = content
        self.file = file
        self.actions.append(action)
        return self

    def git_add_all_and_commit(self, commit):
        def action():
            self.run_command("git add .")
            self.run_command(f"git commit -m '{commit}'")

        self.actions.append(action)
        return self

    def git_switch_and_create(self, branch):
        def action():
            self.run_command(f"git checkout -b {branch}")

        self.actions.append(action)
        return self

    def git_switch(self, branch):
        def action():
            self.run_command(f"git checkout {branch}")

        self.actions.append(action)
        return self

    # 驗證聲明方法
    def valid_content(self, file=None, expected_content=None):
        if file is None or expected_content is None:
            file = self.file
            expected_content = self.content

        def validation():
            with open(os.path.join(self.repo_path, file), "r") as f:
                content = f.read().strip()
                self.assert_equal(content, expected_content)

        self.add_validation(validation)
        return self

    def valid_branches(self, branches):
        def validation():
            stdout = self.run_command("git branch")
            branch_list = [
                line.strip().replace("* ", "") for line in stdout.splitlines()
            ]
            for branch in branches:
                if branch == "master":
                    branch = "main"
                self.assert_in(branch, branch_list)

        self.add_validation(validation)
        return self

    def valid_current_branch(self, branch):
        def validation():
            current_branch = self.run_command("git branch --show-current")
            if current_branch == "master":
                current_branch = "main"
            self.assert_equal(current_branch, branch)

        self.add_validation(validation)
        return self

    def assert_equal(self, actual, expected):
        assert actual == expected, f"Assertion failed: {actual} != {expected}"

    def assert_not_equal(self, actual, unexpected):
        assert actual != unexpected, f"Assertion failed: {actual} == {unexpected}"

    def assert_in(self, element, container):
        assert element in container, f"Assertion failed: {element} not in {container}"
