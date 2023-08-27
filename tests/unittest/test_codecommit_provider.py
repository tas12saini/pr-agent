import pytest
from pr_agent.git_providers.codecommit_provider import CodeCommitFile
from pr_agent.git_providers.codecommit_provider import CodeCommitProvider
from pr_agent.git_providers.git_provider import EDIT_TYPE


class TestCodeCommitFile:
    # Test that a CodeCommitFile object is created successfully with valid parameters.
    # Generated by CodiumAI
    def test_valid_parameters(self):
        a_path = "path/to/file_a"
        a_blob_id = "12345"
        b_path = "path/to/file_b"
        b_blob_id = "67890"
        edit_type = EDIT_TYPE.ADDED

        file = CodeCommitFile(a_path, a_blob_id, b_path, b_blob_id, edit_type)

        assert file.a_path == a_path
        assert file.a_blob_id == a_blob_id
        assert file.b_path == b_path
        assert file.b_blob_id == b_blob_id
        assert file.edit_type == edit_type
        assert file.filename == b_path


class TestCodeCommitProvider:
    def test_parse_pr_url(self):
        url = "https://us-east-1.console.aws.amazon.com/codesuite/codecommit/repositories/my_test_repo/pull-requests/321"
        repo_name, pr_number = CodeCommitProvider._parse_pr_url(url)
        assert repo_name == "my_test_repo"
        assert pr_number == 321

    # Test that an error is raised when an invalid CodeCommit URL is provided to the set_pr() method of the CodeCommitProvider class.
    # Generated by CodiumAI
    def test_invalid_codecommit_url(self):
        provider = CodeCommitProvider()
        with pytest.raises(ValueError):
            provider.set_pr("https://example.com/codecommit/repositories/my_test_repo/pull-requests/4321")

    def test_get_file_extensions(self):
        filenames = [
            "app.py",
            "cli.py",
            "composer.json",
            "composer.lock",
            "hello.py",
            "image1.jpg",
            "image2.JPG",
            "index.js",
            "provider.py",
            "README",
            "test.py",
        ]
        expected_extensions = [
            ".py",
            ".py",
            ".json",
            ".lock",
            ".py",
            ".jpg",
            ".jpg",
            ".js",
            ".py",
            "",
            ".py",
        ]
        extensions = CodeCommitProvider._get_file_extensions(filenames)
        assert extensions == expected_extensions

    def test_get_language_percentages(self):
        extensions = [
            ".py",
            ".py",
            ".json",
            ".lock",
            ".py",
            ".jpg",
            ".jpg",
            ".js",
            ".py",
            "",
            ".py",
        ]
        percentages = CodeCommitProvider._get_language_percentages(extensions)
        assert percentages[".py"] == 45
        assert percentages[".json"] == 9
        assert percentages[".lock"] == 9
        assert percentages[".jpg"] == 18
        assert percentages[".js"] == 9
        assert percentages[""] == 9

        # The _get_file_extensions function needs the "." prefix on the extension,
        # but the _get_language_percentages function will work with or without the "." prefix
        extensions = [
            "txt",
            "py",
            "py",
        ]
        percentages = CodeCommitProvider._get_language_percentages(extensions)
        assert percentages["py"] == 67
        assert percentages["txt"] == 33

        # test an empty list
        percentages = CodeCommitProvider._get_language_percentages([])
        assert percentages == {}

    def test_get_edit_type(self):
        assert CodeCommitProvider._get_edit_type("A") == EDIT_TYPE.ADDED
        assert CodeCommitProvider._get_edit_type("D") == EDIT_TYPE.DELETED
        assert CodeCommitProvider._get_edit_type("M") == EDIT_TYPE.MODIFIED
        assert CodeCommitProvider._get_edit_type("R") == EDIT_TYPE.RENAMED

        assert CodeCommitProvider._get_edit_type("a") == EDIT_TYPE.ADDED
        assert CodeCommitProvider._get_edit_type("d") == EDIT_TYPE.DELETED
        assert CodeCommitProvider._get_edit_type("m") == EDIT_TYPE.MODIFIED
        assert CodeCommitProvider._get_edit_type("r") == EDIT_TYPE.RENAMED

        assert CodeCommitProvider._get_edit_type("X") is None