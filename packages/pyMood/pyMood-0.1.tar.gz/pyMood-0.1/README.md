# Python Mood Enhancer (pyMood)

![Build Status](https://img.shields.io/github/actions/workflow/status/software-students-spring2024/3-python-package-exercise-team-frabtanah/event-logger.yml)

## Description

pyMood is a python package designed to give a quick mood boost to programmers. With simple commands, users can get positive affirmations, quick jokes, or even a virtual high five among other things. It's perfect for when you need a quick pick-me-up during a coding session.

## Instructions

For any developers who want to import pyMood into their own code, follow the steps below:

To install the module from PyPI, run the command:

``pip install -i https://test.pypi.org/PATH TO pyMood``

### Contributions

A virtual environment is required to build and test.
To start the virtual environment, first you must install pipenv and then run:<br>
```pip install pipenv```<br>
```pipenv install -e .```<br>
```pipenv shell```



Then install pyMood in your virtual environment:
```pipenv install pyMood```

To install the dependencies of pyMood:
```pipenv install pytest build twine```

To run the main file and our project: 
```python3 -m pyMood```

To run the unit tests provided you can then simply run:
```pytest```

## Usage

We have several functions to use from within pyMood.

```python

relaxation_tip(category)
# Returns a random relaxation tip from a specified category to help the user relax.
# If no category is specified, return a random tip.
```

```python
tell_me_a_joke()
# Returns a random joke to lighten up the user's mood
```

```python
get_affirmation()
# Returns a random positive affirmation to boost the user's mood and confidence
```

```python
coffee_suggestion()
# Returns a random cup of coffee as a suggestion, to help motivate the user.
```

```python
cat_mood_generator()
# Returns a random cat emotion.
```

```python
high_five()
# Returns a random high five ASCII.
```

Here we have included a link to the [example program](src/pyMood/__main__.py) that uses these functions.
To run it from within the package, use:
```python -m pyMood.__main__```

Otherwise use:
```python __main__.py```

## Team Members

- Francisco Cunningham - [fctico11](https://github.com/fctico11)
- Ahmad Almesned - [ahmadhcs](https://github.com/ahmadhcs)
- Tanuj Sistla - [tanuj123-cyber](https://github.com/tanuj123-cyber)
- Abhi Vachani - [avachani](https://github.com/avachani)

Link to [pyMood](link) on the PyPI website.
