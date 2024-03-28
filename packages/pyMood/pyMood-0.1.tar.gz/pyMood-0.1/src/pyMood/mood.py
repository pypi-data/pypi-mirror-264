import random

from .affirmations import affirmations
from .coffee_types import coffee_types
from .relaxation_tips import relaxation_tips
from .jokes import jokes
from .highfives import highfives




def get_affirmation():
    """
    Returns a random positive affirmation to boost the user's mood and confidence.
    """
    return random.choice(affirmations)

def cat_mood_generator():
    """
    Randomly generates a cat's mood.
    """
    moods = ["Playful", "Sleepy", "Hungry", "Grumpy"]
    return random.choice(moods)


def tell_me_a_joke():
    """
        Returns a random joke to lighten up the user's mood. 
    """
    joke = random.choice(jokes)
    return joke


def relaxation_tip(category=None):
    """
        Returns a random relaxation tip from a specified category to help the user relax.
        If no category is specified, return a random tip.
    """
    if category and category in relaxation_tips:
        tips = relaxation_tips[category]
    else:
        #If no specific category is given or the category doesn't exist, choose a random tip
        all_tips = [tip for tips in relaxation_tips.values() for tip in tips]
        tips = all_tips

    return random.choice(tips)

   

def coffee_suggestion():
    """
        Returns a random cup of coffee as a suggestion. 
    """
    suggestion = random.choice(coffee_types)
    return f"How about a cup of {suggestion} today?"


def high_five():
    ## Return random highfive ASCII Art
    hf = random.choice(highfives)
    return hf



