

# Lightweight and Rapid Bidirectional Search (LiteRBS)
![alt text](./portion.gif)
<video width="630" height="300" src="https://user-images.githubusercontent.com/.../video.mp4" controls></video>
![alt text](./LiteRBS_Turtlebot3.mp4)
## Introduction
This project makes use of python version *3.12.6*.
The project includes a requirements.txt for all the dependencies and their versions.
Before running commands, be sure to run:

```
pip3 install -r requirements.txt
```

The entry point to the project is *./main.py*.

## Animate Mode
The goal of this mode is to visualise different algorithms.
The server will host a html web page on port *5005*.
You can then use the interface to compare the behaviour of the algorithms which you have selected.

You can run it like so:

```
python3 main.py -m animate
```

A link running on localhost (port 5005) should present a web page, where you can visualise & compare.

## Quick Compare and View Code Names
The goal of this mode is to quickly compare the performance of different algorithms.
A table will be produced, presenting various metrics.

You can run it like so:

```
python3 main.py -m quick-compare \
--grid-type robustness \
--grid-size 20 \
--grid-density 10 \
--grid-seed 100 \
--grid-algorithms '*'
```

*--grid-density* is only needed when the *--grid-type* is *robustness*.

If you want a subset of algorithms to compare instead of the full list, you can use the command below to see the codename - full name relationship, then use the codename to select your preference:
```
python3 main.py -m view-code-names
```

Following on, you run the command like the following:

```
python3 main.py -m quick-compare \
--grid-type robustness \
--grid-size 20 \
--grid-density 10 \
--grid-seed 100 \
--grid-algorithms literbs-8-pythag-pruned da2
```

Note that ***LiteRBS 8 Pythag*** (literbs-8-pythag) edition was used during analysis, but the pruning process in the ***LiteRBS 8 Pythag Pruned*** (literbs-8-pythag-pruned) edition can improve path size in some cases with little impact to time and memory.
The algorithm: ***LITRBS (Using 1 instance)*** (sh) represents 1 instance of LiteRBS.

## Record Tests
The goal of this mode, is to record the performance of algorithms over a variety of different graphs. The params *initialSeed*, *seedIncriment* and *gridSize* can be used to reproduce the tests.

To allow for flexibility, the tests are defined in a yaml file. 
You can find an example in *./testConfig.yaml*.

The following fields are only valid for 'type' of *robustness*:
1. *densityStart*: what density to start from
2. *densityIncrimentAfter*: after N iterations, the density should be increased
3. *densityIncriment*: after N iterations, the density should be increased by the value defined here, e.g. 1

In the case that the test terminates unintentionally, re-running the commands continues the tests where they left of as they
append to the output csv files, rather than overriding them. This is assuming the name of the test does not change in the config.
One caveat, this does not apply to the *robustness* tests.

You can run it like so:

```
python3 main.py -m record-tests --test-config testConfig.yaml
```

When running the program, *--test-config* argument specifies the file path to the test config.
Test results are stored in *./results/TEST_NAME* where *TEST_NAME* corresponds to the *name* field in the config.
