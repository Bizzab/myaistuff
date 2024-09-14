import random
import time

choices = ["Rock", "Paper", "Scissors", "Oil", "Fire", "Water"]
john_wins = 0
arnold_wins = 0
john_points = 0
arnold_points = 0
john_streak = 0
arnold_streak = 0
john_history = []
arnold_history = []
john_double_points_used = False
arnold_double_points_used = False
rounds_without_tie = 0
previous_games = []
total_wins_john = 0
total_wins_arnold = 0

def get_random_choice():
    return random.choice(choices)

def predict_choice(own_history, opponent_history, previous_games):
    combined_history = own_history + opponent_history + previous_games
    
    if not combined_history:
        return get_random_choice()
    
    # Frequency analysis
    rock_count = combined_history.count("Rock")
    paper_count = combined_history.count("Paper")
    scissors_count = combined_history.count("Scissors")
    oil_count = combined_history.count("Oil")
    fire_count = combined_history.count("Fire")
    water_count = combined_history.count("Water")
    
    # Adaptive learning with randomness
    total_count = len(combined_history)
    if total_count == 0:
        return get_random_choice()
    
    probabilities = {
        "Rock": rock_count / total_count,
        "Paper": paper_count / total_count,
        "Scissors": scissors_count / total_count,
        "Oil": oil_count / total_count,
        "Fire": fire_count / total_count,
        "Water": water_count / total_count
    }
    
    # Choose based on weighted probabilities
    return random.choices(choices, weights=[probabilities[choice] for choice in choices], k=1)[0]

def avoid_tie_choice(ai_choice, opponent_choice):
    if ai_choice == opponent_choice:
        return get_random_choice()
    return ai_choice

def reward_for_variety(history):
    if len(history) < 4:
        return 0
    last_four = history[-4:]
    if len(set(last_four)) > 2:
        return 2  # Reward for variety
    return 0

def play_game():
    global john_wins, arnold_wins, john_points, arnold_points, john_streak, arnold_streak, john_double_points_used, arnold_double_points_used, rounds_without_tie, previous_games, total_wins_john, total_wins_arnold
    john_choice = predict_choice(john_history, arnold_history, previous_games)
    arnold_choice = predict_choice(arnold_history, john_history, previous_games)
    
    # Adjust choices to avoid ties
    john_choice = avoid_tie_choice(john_choice, arnold_choice)
    arnold_choice = avoid_tie_choice(arnold_choice, john_choice)
    
    john_history.append(john_choice)
    arnold_history.append(arnold_choice)
    previous_games.append(john_choice)
    previous_games.append(arnold_choice)
    print(f"John: {john_choice} | Arnold: {arnold_choice}")

    if john_choice == arnold_choice:
        print("It's a tie!")
        john_streak = 0
        arnold_streak = 0
        john_points -= 3  # Deduct more points for a tie
        arnold_points -= 3
        rounds_without_tie = 0
    elif (john_choice == "Rock" and (arnold_choice == "Scissors" or arnold_choice == "Fire" or arnold_choice == "Water")) or \
         (john_choice == "Paper" and (arnold_choice == "Rock" or arnold_choice == "Water")) or \
         (john_choice == "Scissors" and (arnold_choice == "Paper" or arnold_choice == "Oil")) or \
         (john_choice == "Oil" and arnold_choice == "Paper") or \
         (john_choice == "Fire" and (arnold_choice == "Oil" or arnold_choice == "Paper")) or \
         (john_choice == "Water" and (arnold_choice == "Scissors" or arnold_choice == "Fire")):
        print("John wins!")
        john_wins += 1
        john_streak += 1
        arnold_streak = 0
        if john_streak == 10 and not john_double_points_used:
            john_points += 10  # Double points for 10-win streak
            john_double_points_used = True
        else:
            john_points += 5
        arnold_points -= 6
        rounds_without_tie += 1
    else:
        print("Arnold wins!")
        arnold_wins += 1
        arnold_streak += 1
        john_streak = 0
        if arnold_streak == 10 and not arnold_double_points_used:
            arnold_points += 10  # Double points for 10-win streak
            arnold_double_points_used = True
        else:
            arnold_points += 5
        john_points -= 6
        rounds_without_tie += 1

    # Reward for not tying over a certain number of rounds
    if rounds_without_tie >= 5:
        john_points += 2
        arnold_points += 2
        rounds_without_tie = 0

    # Reward for variety in choices
    john_points += reward_for_variety(john_history)
    arnold_points += reward_for_variety(arnold_history)

    print(f"John Wins: {john_wins} | Arnold Wins: {arnold_wins}")
    print(f"John Points: {john_points} | Arnold Points: {arnold_points}")

    # Check for game winner
    if john_points >= 50:
        print("John wins the game!")
        total_wins_john += 1
        reset_game()
    elif arnold_points >= 50:
        print("Arnold wins the game!")
        total_wins_arnold += 1
        reset_game()

    print(f"Record: John - {total_wins_john}, Arnold - {total_wins_arnold}")

def reset_game():
    global john_points, arnold_points, john_streak, arnold_streak, john_double_points_used, arnold_double_points_used, rounds_without_tie, john_history, arnold_history
    john_points = 0
    arnold_points = 0
    john_streak = 0
    arnold_streak = 0
    john_double_points_used = False
    arnold_double_points_used = False
    rounds_without_tie = 0
    john_history = []
    arnold_history = []
    time.sleep(10)  # Wait for 10 seconds before starting a new game

if __name__ == "__main__":
    while True:
        play_game()
        time.sleep(4)
