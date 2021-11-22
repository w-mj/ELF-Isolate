
objs := main.o external_lib2.o


all: $(objs) build_lib
	ar rcs libext2.a external_lib2.o
	g++ main.o libmylib.a libext2.a -o exec
	./exec

build_lib:
	g++ -c -o lib.o lib.cpp

	g++ -c -o external_lib1.o external_lib1.cpp
	ar rcs libext1.a external_lib1.o

	python ../isolate.py lib.o libext1.a -p interface* -o mylib.o

	ar rcs libmylib.a mylib.o

clean:
	-rm *.o
	-rm *.a