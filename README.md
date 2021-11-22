# ELF文件符号隔离工具

可根据简单规则批量将ELF文件中不需要导出的符号重命名，以防止污染项目造成链接错误。


## Usage

```
usage: isolate.py [-h] -o OUTPUT -p PATTERN FILES [FILES ...]

Isolate elf symbols.

positional arguments:
  FILES       待处理的ELF文件。

optional arguments:
  -h, --help  show this help message and exit
  -o OUTPUT   输出文件名，输出文件格式为可重定向(REL)文件。
  -p PATTERN  需要保留的符号，支持通配符*，可使用多个-p参数指定多条模式。
```

## Example

```
python isolate.py lib.o libext1.a -p interface* -o mylib.o
```

仅保留所有以interface开头的符号，其他自定义符号均会被重命名。
