from fun import magic_8_ball, affirmations, copypasta, make_me_laugh

def main():
    print("Welcome to the 4fun package demonstration!")
    eight_ball_question_count = 0

    while True:
        print("\nChoose an option:")
        print("1. Ask the magic 8 ball a question")
        print("2. Get affirmations based on your mood")
        print("3. Get a text or image copypasta")
        print("4. Make me laugh!" )
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            question = input("Ask the magic 8 ball a question: ")
            print("\n" + magic_8_ball(question, eight_ball_question_count))
            eight_ball_question_count += 1
        elif choice == '2':
            mood = input("How are you feeling today? (happy/sad): ")
            print("\n" + affirmations(mood))
        elif choice == '3':
            output_type = input("Do you want a text or image copypasta? (type \"text\" or \"image\"): ")
            print("\n" + copypasta(output_type))
        elif choice == '4': 
            joke = input("Do you want a fun fact or a joke?")
            print("\n" + make_me_laugh(joke))
        elif choice == '5':
            print("\nGoodbye!\n")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()