
@ECHO OFF
@REM 删除dist文件夹
rmdir /s /q dist

@REM 编译包
python -m build

@REM -t上传pypi
IF "%1%"=="-t" (
    twine upload dist/*
)