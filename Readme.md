# ⚙️ Compiler for COOL language
 
[![Tests](https://github.com/matcom-school/cool-compiler-2021/actions/workflows/tests.yml/badge.svg)](https://github.com/matcom-school/cool-compiler-2021/actions/workflows/tests.yml)


## 🤔 What's it?

Compiler for the COOL language, you can see its official documentation [here](https://github.com/matcom-school/cool-compiler-2021/tree/master/doc). 
The COOL language is a static and strongly typed tool, with imperative syntax and influenced by 
the object-oriented design pattern. In this project a compiler is developed that transforms 
plain text code into executable [MIPS](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjr4bytrL_7AhXZi7AFHVj3D-QQFnoECAoQAQ&url=https%3A%2F%2Fwww.mips.com%2F&usg=AOvVaw0pNYEgrs30qfMWUUI1txqH) 
code. To perform this transformation, the system is 
composed of 4 main modules that represent the 4 main phases of language theory 
(lexer, parser, semantic checking and code generation). \
**Principal Skills**: `Python` `Metaprogramming` `AST` `Visitor Pattern` `Sly` `MIPS`

## 🤓 Motivation 

This project was developed as part of a compilation course at the University of Havana. 
With the educational foundation of knowing the main aspects of a compiler or interpreter, 
tools that developers use on a daily basis.

## 🧐 How to use it?

First download the project  

```bash
$ git clone https://github.com/matcom-school/cool-compiler-2021.git
$ pip install -r requirements.txt
```
Check that all tests are working properly 

```bash
$ cd src
$ make test
```

Then type your COOL code and save the changes in .cl and execute the following commands

```bash
$ make <name_file>.cl
```

