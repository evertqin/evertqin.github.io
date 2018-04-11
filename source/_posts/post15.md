---
title: C# and C++ Interop Demonstration
date: 08/03/2015
tag: 
- Technology
- C#
---

One interesting feature of C# is that you can directly use unmanaged dlls from the managed code. There are different ways to do this, such as: 1) using a unsafe block and write unmanaged code directly. It is tested that the performance of these unmanaged codes is somewhate better than managed code. 2) use Marshall and dllimport from C# and dllexport from C++; 3) use 3rd party libraries such as swig.exe. Here I am going to introduce using dllimport because I think this is the most native way to deal with interop requirements.

<!--more-->

The C++ source files need to be specially wrapped to expose function interfaces to managed code: in the header file: (headers.hh), need to
* Wrap all the function signatures in `extern "C"` because we don't want C++ compiler to mangle the function name.
* append `__declspec(dllexport)` before function declearation.

a basic example, first creat an empty C++ dll project and add two files: headers.hh and source.cc. In header.hh file, add the following lines:

~~~~{.cpp}
#ifndef CPPLIB_HEADERS_HH
#define CPPLIB_HEADERS_HH

extern "C"
{
	__declspec(dllexport) void get_simple_type(int num);
}

#endif
~~~~

And in source.cc file, add the following lines:

~~~~{.cpp}
#include "headers.hh"
#include <iostream>
#include <fstream>

void get_simple_type(int num) {
	std::cout << "Number: \"" << num << "\"" << std::endl;
}
~~~~

Here we are passing a simple int from C# to C++ and print out.

In a separate C# project, created in the same solution, add the following lines

~~~~{.cs}
[DllImport("CppLib.dll", CallingConvention = CallingConvention.Cdecl)]
public static extern void get_simple_type(int num);

public void TransferSimpleType()
{
    int num = 5;
    get_simple_type(num);
}
~~~~

Run the project, we should be able to see "Number: "5"" from console window.

Getting return value is also very straight-forward. we add another line or function declearation into the extern "C":

~~~~{.cpp}
__declspec(dllexport) double return_simple_type(double num);
~~~~

Then implement the above function in source.cc

~~~~{.cpp}
double return_simple_type(double num) {
	return 4.9 * num;
}
~~~~

In C#, do the following to catch the return value:

~~~~{.cs}
[DllImport("CppLib.dll", CallingConvention = CallingConvention.Cdecl)]
public static extern double return_simple_type(double num);

public void RetriveSimpleType()
{
    double num = 5.0;
    double ret = return_simple_type(num);
    Console.WriteLine(string.Format("From RetriveSimpleType we get: \"{0}\"", ret));
}
~~~~

Run the above code, you should see "From RetriveSimple we get: "24.5"

The above examples are both quite easy to deal with, what's more interesting is dealing with customized data structures and arries, here we need to use functions in the Marshall class. Suppose we want to calculate on a double[] array and return a double[], we can not just write `double[] calculate(double[] input);` because in C++, we have no idea how large is the double array because what we are passing into C++ got converted to a double *.. Also C++ can only return a double *, and it up to us to figure out how large is the double[]. Therefore, we need to find a way to specify the size of the array.

The input arguments are simple, we only need to add another `int size` to the argument list. To pass back the return size of the array, we need to define same struct in both C# and C++.

in C++:

~~~~{.cpp}
struct OneDimRetArray
{
	double* content;
	int size;
};

typedef struct OneDimRetArray OneDimRetArray_t;
~~~~

in C#

~~~~{.cs}
struct OneDimRetArray
{
    public IntPtr content;
    public int size;
};
~~~~

Notice that all the pointer types in C++ got converted to System.IntPtr in C#.

Now let's define some functions:

In C++:

~~~~{.cpp}
__declspec(dllexport) OneDimRetArray_t* make_1d_array(const double* input, int size);
__declspec(dllexport) int release_one_dim(OneDimRetArray_t* toFree);
~~~~

Notice since we use pointers and we dynamically allocated memory, we need another function to clean the memory;

~~~~{.cpp}
OneDimRetArray_t * make_1d_array(const double * input, int size) {
	OneDimRetArray_t * result = new OneDimRetArray_t();
	result->content = new double[size * 2];
	result->size = size * 2;

	const double * p = input;
	for (int i = 0, j = 0; i < size; ++i) {
		result->content[j++] = *p;
		result->content[j++] = *p;
		p++;
	}
	return result;
}
int release_one_dim(OneDimRetArray_t * ptr_to_free) {
	if (ptr_to_free == NULL) {
		return -1;
	}

	if (ptr_to_free->content != NULL) {
		delete[] ptr_to_free->content;
		ptr_to_free->content = NULL;
	}

	delete ptr_to_free;
	ptr_to_free = NULL;
	return 0;
}
~~~~

in C#, we need to call the above function:

~~~~{.csharp}
[DllImport("CppLib.dll")]
public static extern IntPtr make_1d_array(double[] nums, int size);
[DllImport("CppLib.dll")]
public static extern int release_one_dim(IntPtr toFree);

public void RetriveArrayType()
{
    Console.WriteLine("Retriving Array");
    double[] nums = { 1, 2, 3, 4, 5 };
    IntPtr ptr = make_1d_array(nums, nums.Length);
    OneDimRetArray result = (OneDimRetArray)Marshal.PtrToStructure(ptr,
                            typeof(OneDimRetArray));

    double[] num = new double[result.size];
    Marshal.Copy(result.content, num, 0, result.size);
    foreach (double d in num)
    {
        Console.Write(d + ", ");
    }
    Console.WriteLine();

    int release = release_one_dim(ptr);
}
~~~~

Run the whole project, you should see the following output.

![Run Result](http://i.imgur.com/d0D0H74.png)

You can find the source code on [GitHub](https://github.com/evertqin/DotNetDemos/tree/master/SharpCppInterop)

<font color='red'>Comment (09/01/2015): I think there is something miss about releasing memory when I first wrote it. Now i think the correct way
to do it is by using the follong Marshal functions: `Marshal.DestroyStructure`, `Marshal.FreeHGlobal`.
</font>

For example, in my previous example, I created a struct called `OneDimRetArray ` . To proper release the memory, I need the folling function:

~~~~{cs}
struct OneDimRetArray
{
    public IntPtr content;
    public int size;
    
    public static void Free(OneDimRetArray result)
    {
        Marshal.FreeHGlobal(result.content);
        result.content = IntPtr.Zero;
    }

    public static void Free(IntPtr ptr)
    {
        OneDimRetArray result = (OneDimRetArray) Marshal.PtrToStructure(ptr, typeof (OneDimRetArray));
        Free(result);
        Marshal.DestroyStructure(ptr, typeof (OneDimRetArray));
        Marshal.FreeHGlobal(ptr);
        ptr = IntPtr.Zero;
    }
};
~~~~
