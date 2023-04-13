# Regex-Analyser

## Project Description
> The Regex Analyser is an academic assignment given in the course of Languages and Compilers `CMPN403` at Cairo University - Faculty of Engineering - Credit Hours System - Communication and Computer Engineering Program.
>
> The assignment covers the different functionalities for a regex analyser which is a basic component in a lexical analyser.

***

## Programming Language Used
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">

***

## Used Approach

### The implementation consists of 5 main elements which are:
>
> 1. Regex Validation
>> The first component in the pipeline is the validation process.
>
> 2. Regex Parsing
>> The regex is parsed into a feasible and programmer-friendly format for further processing.
>
> 3. Creation of NFA states
>> NFA states are created using Thompson's Algorithm.
>> The NFA states are presented visually using GraphViz python library and in a specific JSON format.
>
> 4. Creation of DFA states
>> Based on the specific JSON format, the NFA states are read and transformed into DFA states.
>
> 5. DFA minimization
>> The DFA is then reduced to a minimized DFA in which each state has a unique behaviour.

***

> You can run the Regex-Analyser flow in the [attached notebook](https://colab.research.google.com/drive/1K4ojwx7v7AmtHjgdMp_RvhCgtiugHa3R?usp=sharing).
> 
> Examples of [test cases](https://github.com/devyetii/Regex-Test-Cases). 
