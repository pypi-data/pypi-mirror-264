# Monte-Carlo-Neural-Nets

## Overview
A very lightweight machine learning package.

Has models that use a unique and simple Monte Carlo approach to training. This method used is
very generalizable and can therefore be extended to a variety of models both known and new. 

The primary model, the 'NeuralNetwork' class, is on par with other similar models such as the 
MLPRegressor/MLPClassifier featured in SciKit-Learn, but has more customizability.

In V2.0.5 the list of models avaliable and some of their features includes:
- NeuralNetwork
    - Complete hidden layer size and activations customization
    - Supports externally defined activation functions
    - Allows customizing the input and output activations
    - Easy-access hyperparam ranges for Optuna (via .get_param_ranges_for_optuna)
- SoupRegressor
    - A unique combination of many various functions with trainable coefficients
    - Typically on-par with the NeuralNetwork; slightly more interpretable
    - Many hyperparams to adjust, with more to come

Some QoL functions and features included are:
- TTSplit: Included train-test splitter
- cross_val: Simple cross validation system
- Built-in scorer functions with support for external functions
- Ability to save and load models at any point (.save & load_model)
- Ability to copy a model via .copy

## GitHub and QuickStart
More explanations, examples, and technicals can be found on the GitHub page:
https://github.com/SciCapt/Monte-Carlo-Neural-Nets

