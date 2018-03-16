---
title: ILNumerics.NET Best Practices
date: 11/04/2015
tags: 
- Technology
- C#
---

I have been working with [ILNumerics.NET](http://ilnumerics.net/) for quite a while. It is a fine piece of mathmatical library which provides better performance than most of the other .NET numeric libraries. Used properly, it's performance can also surpass that of MATLAB.

<!--more-->

However, since the user base for this library is quite small and it went commercial after version 3.3.3 , it is not very easy to get help. Moreover, the official guide is somewhat scattered around their instructions, tutorials and blog, sometimes, when you notice some problem, you are already late in the development cycle so you have to go back and do a lot of code refactoring, which, if known in the beginning, can be totally avoided. I am summarizing the best practices and tricks I have with this library so if you happen to start using this library, this guide can help you avoid some mistakes I made.

1. Follow the function rule:
    * Use In Array type as input (such as ILInArray<T>) and do not mutate the value of this;
    * Use Out Array type as output (such as ILOutArray<T>, comparable with out keyword in C#), use assigner (.a) notation to mutate the value, also make sure initializing before passing in as Out Array;
    * Use Ret Array for return value, this array will be destroyed after first use. [Reference](http://ilnumerics.net/FunctionRules.html)
2. *Important* wrap everything within using(ILScope.Enter()), if you want to hold the input array Reference, put them as parameters inside Enter(); Consider wrapping the for loop for better performance;[Reference](http://ilnumerics.net/PerfMemoryOpt.html)
3. if you want to use ILArray<T> as class member, declare it as readonly then initialize with ILMath.localMember. [Reference](http://ilnumerics.net/blog/using-ilarray-as-class-attributes/)
4. Two Settings switches are very important:
Everything is summarized in the attached code `Settings.AllowInArrayAssignments = false;`, `Settings.MaxNumberThreads = 1;` Refer to the code for explanation.

~~~~{.csharp}
using System;
using ILNumerics;

namespace ilnumerics_tricks
{
    /// <summary>
    /// We extend ILMath class so we don't need to prefix all the functions with ILMath. static class name
    /// </summary>
    class SampleClass : ILMath, IDisposable
    {
        /// <summary>
        /// By default, all the ILArrays are disposed after they went out of the ILScope,
        /// but sometimes we want to keep them as a class member and live with the class
        /// to do this, we need to declare them as localMember<T>(), then our class needs to
        /// implement IDisposable interface and explicitly destroy this ILArray Instance
        /// </summary>
        private ILArray<double> classMember = localMember<double>();

        static SampleClass()
        {
            //Performance switch, dis-/allow direct assignments to input parameters
            //- brings more efficient memory management, default: true (safer, less efficient)
            Settings.AllowInArrayAssignments = false;

            // By default, ILNumerics.NET sets this to 2 on all multicore machines.
            // Therefore, this setting should be set manually for better processor utilization
            // on multicore machines.
            // This setting is very important if you want to use C# Parallel functions,
            // you have to set it to 1 and manage parallelism by yourself, otherwise,
            // you may get random null object reference error.
            Settings.MaxNumberThreads = 1;
        }

        /// <summary>
        /// Below is a useless function to demonstrate the function concept
        /// </summary>
        /// <param name="data1">The input array has to have "In", this makes a contract
        /// that this is an input data, which should not be mutable,  if we follow this rule,
        /// we can use Settings.AllowInArrayAssignments = false;  to make an agreement with
        /// the library that we are not alternating the input data, this will result in a
        /// performance gain from 1% to 30%(http://ilnumerics.net/apidoc/html/P_ILNumerics_Settings_AllowInArrayAssignments.htm)</param>
        /// <param name="data2">The output array (much like out keyword) serve as additional,
        /// optional, output parameter of a function,  it is fully mutable, it is suggested
        /// to use array accessor ".a" to access  by convention, we put ILOutArray as the last
        ///  arguments and set their default values to false.</param>
        /// <returns>the return value has to have "Ret", this makes a contract that this
        /// return value will be disposed and garbage collected after first use</returns>
        public ILRetArray<double> BasicFunctionStructure(ILInArray<double> data1, ILOutArray<double> data2 = null)
        {
            // Function bodies of any computational function must be enclosed with a
            // construct according to the following scheme:
            using (ILScope.Enter(data1))
            {
                ILArray<double> summation = sum(data1);

                for (int i = 0; i < 1000; ++i)
                {
                    // you may consider wrapping your function with ILScope inside a loop
                    // for better memory management
                    using (ILScope.Enter())
                    {
                        ILArray<double> trash = sqrt(data1);
                    }
                }


                if (!isnull(data2))
                {
                    data2.a = ones(data1.S);
                }
                return summation;
            }
        }

        /// <summary>
        /// It is always a good idea to wrap all your ILNumerics.NET code within
        /// a using(ILScope.Enter()) block  Here we use check function and use a
        /// lambda function to get the result, here we reused the memory space of data1,
        /// then transfer the result directly to the return value, this saves our effort
        /// of allocating extra memory
        /// </summary>
        /// <param name="data1"></param>
        /// <returns></returns>
        public ILRetArray<double> InPlaceArrayManipulation(ILInArray<double> data1)
        {
            using (ILScope.Enter(data1))
            {
                return check(data1, todouble);
            }
        }


        public void Dispose()
        {
            // this is important if we want to use ILArray as a class Member
            if (!isnull(classMember)) { classMember.Dispose(); }
        }

        static void Main(string[] args)
        {
            using (ILScope.Enter())
            {
                SampleClass smapleClass = new SampleClass();
                ILArray<double> input = new[] {1.0, 2.0};
                ILArray<double> output = empty();

                ILArray<double> returnValue = smapleClass.BasicFunctionStructure(input, output);
            }
        }
    }
}
~~~~
