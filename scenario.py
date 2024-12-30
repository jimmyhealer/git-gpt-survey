from git_test import TestFramework


class InitGitRepo(TestFramework):
    def __init__(self):
        super().__init__("./scenario_1")

    def scenario(self):
        self.init_directory()
        self.write_file("This is a README file.", "README.md")

        self.valid_branches(["main"])
        self.valid_current_branch("main")
        self.valid_commit_length(1)
        self.valid_nth_commit_message(1, "Initial commit")

        return f"""您創建一個新的資料夾，並在其中建立一個 README.md 檔案。
您現在要初始化這個 Git 儲存庫，並確保只有一個 commit，commit 訊息為 "Initial commit"（大小寫要完全符合）。

資料夾位置：{self.repo_path}
""", [
            '確認擁有一個名為 main (master) 的分支，且只有一個 commit 為 "Initial commit"。'
        ]

    def valid_nth_commit_message(self, n, expected_message):
        """
        驗證第 n 個 commit 的訊息是否正確。
        n=1 表示最新的 commit，n=2 表示倒數第二個 commit，依此類推。
        """

        def validation():
            # 使用 git log 從最新開始列出所有 commit message
            nth_commit_message = self.run_command(
                f"git log --format=%B --skip={n - 1} -n 1"
            )
            self.assert_equal(nth_commit_message.strip(), expected_message)

        self.add_validation(validation)
        return self

    def valid_commit_length(self, expected_length):
        def validation():
            commit_count = self.run_command("git rev-list --count HEAD")
            self.assert_equal(int(commit_count), int(expected_length))

        self.add_validation(validation)
        return self


class MergeToMain(TestFramework):
    def __init__(self):
        super().__init__("./scenario_2")

    def scenario(self):
        self.init_directory()
        self.git_init()
        self.write_file("This is a README file.", "README.md")
        self.git_add_all_and_commit("Initial commit")
        self.git_switch_and_create("feat/new-file")
        self.write_file("This is a feature file.", "feature.txt")
        self.git_add_all_and_commit("Add feature file")
        self.git_switch("main")

        self.valid_branches(["main", "feat/new-file"])
        self.valid_current_branch("main")
        self.valid_content("feature.txt", "This is a feature file.")
        self.valid_content("README.md", "This is a README file.")
        self.valid_merge_by_feature()

        return f"""您已經初始化了一個 Git 儲存庫，並創建了兩個 commit。
您現在要將 feat/new-file 分支合併到 main 分支。
註：feat/new-file 分支不要刪除，該專案初始分支已經設定為 main。

資料夾位置：{self.repo_path}
""", [
            '確認現在在 main 分支，並且有 feature.txt 檔案內容為 "This is a feature file."。',
        ]

    def valid_merge_by_feature(self):
        def validation():
            merge_base = self.run_command("git merge-base main feat/new-file")
            feature_commit = self.run_command("git rev-parse feat/new-file")
            self.assert_equal(merge_base, feature_commit)

        self.add_validation(validation)


class ResetCheck(TestFramework):
    def __init__(self):
        super().__init__("./scenario_3")

    def scenario(self):
        self.init_directory()
        self.git_init()
        self.write_file("Version 1", "file.txt")
        self.git_add_all_and_commit("Commit 1")
        self.write_file("Version 2", "file.txt")
        self.git_add_all_and_commit("Commit 2")
        self.write_file("Version 3", "file.txt")
        self.git_add_all_and_commit("Commit 3")
        self.write_file("Version 4", "file.txt")

        self.valid_branches(["main"])
        self.valid_commit_message_in_now("Commit 1")
        self.valid_content("file.txt", "Version 1")

        self.add_validation_order()
        self.valid_branches(["main"])
        self.valid_current_branch("main")
        self.valid_commit_message_in_now("Commit 3")
        self.valid_content("file.txt", "Version 4")

        return f"""您已經初始化了一個 Git 儲存庫，並創建了三個 commit，現在有修改 file.txt 檔案。
您現在要回到第一個 commit，看一下之前寫的文件 (檢核點 1)，然後返回最新的 commit 並且恢復之前修改的紀錄 (檢核點 2)。
此場景有兩個檢核點，請依序完成。
註：該專案初始分支已經設定為 main。

資料夾位置：{self.repo_path}
""", [
            '確認擁有一個名為 main 的分支，檢查現在的 commit 訊息為 "Commit 1"，且檔案內容為 "Version 1"。',
            '確認目前的 commit 訊息為 "Commit 3"，且檔案內容為 "Version 4"。',
        ]

    def valid_commit_message_in_now(self, expected_message):
        def validation():
            message = self.run_command("git log -1 --pretty=%B")
            self.assert_equal(message.strip(), expected_message)

        self.add_validation(validation)
        return self

class RestoreFile(TestFramework):
    def __init__(self):
        super().__init__("./scenario_4")

    def scenario(self):
        self.init_directory()
        self.git_init()
        self.write_file("Version 1", "file.txt")
        self.git_add_all_and_commit("Commit 1")
        self.rm_file("file.txt")

        self.valid_current_branch("main")
        self.valid_content("file.txt", "Version 1")

        return f"""您現在寫了一個檔案，您不小心把它刪除了。您希望從上一個 commit 中恢復這個檔案。
註：該專案初始分支已經設定為 main。

資料夾位置：{self.repo_path}
""", [
            '確認現在在 main 分支，且 file.txt 的內容為上一個 commit 的內容。',
]
    
    def rm_file(self, file):
        def action():
            import os
            os.remove(os.path.join(self.repo_path, file))
        self.actions.append(action)