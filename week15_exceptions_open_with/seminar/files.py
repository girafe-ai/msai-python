# file reading (in bytes mode)
f = open('exception_learning.py', 'rb')
file_content = f.read(3)
print(file_content)
file_content = f.read(3)
print(file_content)
f.seek(0)
file_content = f.read(3)
print(file_content)
f.close()

# file writing (in text mode)
f = open('new_file.txt', mode='w')
f.write('123457890')
f.seek(3)
f.write('aa')
# f.flush()  # make sure buffered bytes flushed to file
f.close()  # flush and release file descriptor


# file descriptors are limited (that block raises OSError)
files = []
for i in range(100000):
    f = open('exception_learning.py')
    files.append(f)
    print(i)


# use context manager not to think about file closing and descriptors leak
files = []
for i in range(100000):
    with open('exception_learning.py') as f:  # there f.__enter__() called
        files.append(f.read())
    # there f.__exit__() called (f.close())
    print(i)

print(files[50000][:100])
