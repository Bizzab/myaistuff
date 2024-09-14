import random
import time

choices = ["Rock", "Paper", "Scissors", "Oil", "Fire", "Water"]

class Player:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.points = 0
        self.streak = 0
        self.history = []
        self.double_points_used = False
        self.total_wins = 0

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

def play_round(player1, player2, previous_games):
    player1_choice = predict_choice(player1.history, player2.history, previous_games)
    player2_choice = predict_choice(player2.history, player1.history, previous_games)
    
    # Adjust choices to avoid ties
    player1_choice = avoid_tie_choice(player1_choice, player2_choice)
    player2_choice = avoid_tie_choice(player2_choice, player1_choice)
    
    player1.history.append(player1_choice)
    player2.history.append(player2_choice)
    previous_games.append(player1_choice)
    previous_games.append(player2_choice)
    print(f"{player1.name}: {player1_choice} | {player2.name}: {player2_choice}")

    if player1_choice == player2_choice:
        print("It's a tie!")
        player1.streak = 0
        player2.streak = 0
        player1.points -= 3  # Deduct more points for a tie
        player2.points -= 3
    elif (player1_choice == "Rock" and (player2_choice == "Scissors" or player2_choice == "Fire" or player2_choice == "Water")) or \
         (player1_choice == "Paper" and (player2_choice == "Rock" or player2_choice == "Water")) or \
         (player1_choice == "Scissors" and (player2_choice == "Paper" or player2_choice == "Oil")) or \
         (player1_choice == "Oil" and player2_choice == "Paper") or \
         (player1_choice == "Fire" and (player2_choice == "Oil" or player2_choice == "Paper")) or \
         (player1_choice == "Water" and (player2_choice == "Scissors" or player2_choice == "Fire")):
        print(f"{player1.name} wins the round!")
        player1.streak += 1
        player2.streak = 0
        if player1.streak == 10 and not player1.double_points_used:
            player1.points += 10  # Double points for 10-win streak
            player1.double_points_used = True
        else:
            player1.points += 5
        player2.points -= 6
    else:
        print(f"{player2.name} wins the round!")
        player2.streak += 1
        player1.streak = 0
        if player2.streak == 10 and not player2.double_points_used:
            player2.points += 10  # Double points for 10-win streak
            player2.double_points_used = True
        else:
            player2.points += 5
        player1.points -= 6

    # Reward for variety in choices
    player1.points += reward_for_variety(player1.history)
    player2.points += reward_for_variety(player2.history)

    print(f"{player1.name} Points: {player1.points} | {player2.name} Points: {player2.points}")

def play_match(player1, player2):
    previous_games = []
    while player1.points < 50 and player2.points < 50:
        play_round(player1, player2, previous_games)
        time.sleep(1)
    
    if player1.points >= 50:
        print(f"{player1.name} wins the match!")
        player1.total_wins += 1
        return player1
    else:
        print(f"{player2.name} wins the match!")
        player2.total_wins += 1
        return player2

def tournament(players):
    while len(players) > 1:
        next_round = []
        for i in range(0, len(players), 2):
            winner = play_match(players[i], players[i+1])
            next_round.append(winner)
        players = next_round
    
    print(f"{players[0].name} wins the tournament!")
    return players[0]

def main():
    player_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack", "Kathy", "Leo", "Mona", "Nina", "Oscar", "Paul"]
    players = [Player(name) for name in player_names]
    most_wins = {player.name: 0 for player in players}

    while True:
        winner = tournament(players)
        most_wins[winner.name] += 1
        print(f"Most Wins Record: {most_wins}")
        time.sleep(6)
        for player in players:
            player.wins = 0
            player.points = 0
            player.streak = 0
            player.history = []
            player.double_points_used = False

if __name__ == "__main__":
    main()
