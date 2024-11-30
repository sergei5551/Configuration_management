import pytest
from hw1.src.emulator import VirtualFileSystem
import sys

@pytest.fixture
def vfs(request):
    archive_file = request.param
    return VirtualFileSystem(archive_file)

@pytest.mark.parametrize("vfs", ["src/filesystem.tar"], indirect=True)
def test_ls(capsys, vfs):
    vfs.handle_ls()
    captured = capsys.readouterr()
    assert captured.out != ""

@pytest.mark.parametrize("vfs", ["src/filesystem.tar"], indirect=True)
def test_cd(vfs):
    vfs.handle_cd(['cd', 'dir1'])
    assert vfs.current_dir == '/dir1'
@pytest.mark.parametrize("vfs", ["src/filesystem.tar"], indirect=True)
def test_echo(capsys, vfs):
    vfs.handle_echo(["echo", "Капуста", "1", "2", "3"])
    captured = capsys.readouterr()
    assert captured.out == "Капуста 1 2 3 \n"
@pytest.mark.parametrize("vfs", ["src/filesystem.tar"], indirect=True)
def test_clear(capsys, vfs):
    vfs.handle_clear()
    captured = capsys.readouterr()
    assert captured.out == ""
@pytest.mark.parametrize("vfs", ["src/filesystem.tar"], indirect=True)
def test_exit(vfs):
    old_exit = sys.exit
    exited = False

    def mock_exit(code):
        nonlocal exited
        exited = True

    sys.exit = mock_exit
    vfs.handle_exit()
    sys.exit = old_exit

    assert exited
