import pyMood.mood as mood

def main():
    print(f"random coffee suggestion:")
    print(mood.coffee_suggestion() + '\n')

    print(f"random positive affirmation:")
    print(mood.get_affirmation() + '\n')

    print(f"random cat mood")
    print(f"The cat's mood: {mood.cat_mood_generator()}\n")

    print(f"tell a random joke:")
    print(mood.tell_me_a_joke() + '\n')

    print(f"random relaxation tip without a specific category:")
    print(mood.relaxation_tip() + '\n')

    print(f"random elaxation tip with a specific category:")
    print(mood.relaxation_tip("nature") + '\n')

    print(f"random high five image:")
    print(mood.high_five() + '\n')

if __name__ == "__main__":
    main()