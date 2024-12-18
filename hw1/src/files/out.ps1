# out.ps1

# Функция для эмуляции команды ls
Function LS {
    Param (
        [string]$Path = "."
    )
    Get-ChildItem -Path $Path | Format-Wide -Column 1
}

# Функция для эмуляции команды cd
Function CD {
    Param (
        [string]$Path
    )
    Set-Location -Path $Path
}

# Функция для эмуляции команды cat
Function CAT {
    Param (
        [string]$FileName
    )
    Get-Content -Path $FileName
}

# Меняем рабочий каталог на /files
Set-Location '/files'

# Список файлов в корневой директории
LS -Path "/"

# Переходим в домашнюю директорию
CD -Path "home"

# Список файлов в домашней директории
LS

# Просмотр содержимого файла example.txt
CAT -FileName "example.txt"