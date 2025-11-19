"""
Kassie's "Wolf Pack" Survival Simulator Game

In this text-based adventure game, you are a lone wolf trying to survive and build a pack.

The concept: The user plays as a wolf. They start with 100 health and 0 pack members. They must
choose to hunt, explore or rest. Random events occur based on their choices. (e.g. "You found an elk! +20 Food"
or "You encountered a bear! -30 Health").

This game will use the 'random' Python library to keep the game unpredictable.
"""
# This grabs the 'random' toolkit.
import random

def load_high_score():
    # The 'try' block attempts the normal operation.
    try:
        # 'r' is for Read mode.
        with open("highscore.txt", "r") as f:
            # Files store text (strings), so we convert it to an integer (int).
            return int(f.read())
    # The 'except' block handles the expected error if the file doesn't exist.
    except FileNotFoundError:
        return 0 # If the file isn't found, the score is 0.

# Load the score and store it in a variable for comparison later.
high_score = load_high_score()

# --- SECTION 1: SETUP ---
# Sets the starting stats for your wolf.
wolf_health = 100
wolf_hunger = 0
pack_size = 0
day = 1
game_running = True

print("🐾 Welcome to the Wolf Pack Survival Game! 🐾")
print("You are a lone wolf 🐺. Survive as long as you can.")

def display_status(high_score, day, wolf_health, wolf_hunger, pack_size):
    print("-" * 30)
    print(f"HIGH SCORE: {high_score}")
    print(f"DAY: {day} ☀️ | HEALTH: {wolf_health} ❤️ | HUNGER: {wolf_hunger} 🥩 | PACK SIZE: {pack_size} 🐾")
    print("Options: [1] Hunt  [2] Rest  [3] Recruit  [4] Quit")

def handle_hunt(wolf_health, wolf_hunger, pack_size):
        print("\n--- THE HUNT ---")
        print("You creep silently into the forest 🌳, sniffing the air...")

        # 1. Define Your Prey List
        possible_prey = ["Rabbit 🐇", "Deer 🦌", "Wild Turkey 🦃", "Bison 🦬"]

        # 2. Pick a Random Animal
        prey = random.choice(possible_prey)
        print(f"You spot a {prey} grazing nearby!")

        # 3. The Hunt Roll (1 - 10)
        # We simulate the chaos of the hunt
        # Higher numbers represent better performance by the wolf.
        # Base Roll
        hunt_roll = random.randint(1, 10)

        # THE BUFF: Add 1 point for every pack member
        total_roll = hunt_roll + pack_size
        print(f"You lunged at the {prey}... (Rolled: {hunt_roll} + Pack: {pack_size} = {total_roll})")

        # 4. Determine Success (Logic Gate)
        # --- Difficulty Tweak ---
        # OLD: If hunt_roll >= 4: (Too Easy)
        # NEW: If hunt_roll >= 7: (Harder - 40% Success Rate)
        if total_roll >= 7:
            print(f"SUCCESS! You took down the {prey}.")
            print("You feast on the meat.")

            # Rewards
            wolf_hunger -= 30 # Hunger goes down (You are full)
            wolf_health += 5 # Eating restores a little health.

        else:
            print(f"FAILURE. The {prey} was too fast and escaped.")
            print("You wasted energy chasing it.")

            # --- PENALTY TWEAK ---
            wolf_hunger += 10
            # Old wolf_health -= 5
            # New wolf_health -= 15 (Much More Dangerous)
            wolf_health -= 15

        return wolf_health, wolf_hunger

def handle_rest(day, wolf_health, wolf_hunger):
    # This is where the resting logic goes
    print("\n--- RESTING ---")
    print("You curl up in your den to rest. The sun sets and rises again.")
    print("🌞🌝🌞")

    day += 1

    # The Basic Math
    wolf_health += 15
    wolf_hunger += 5

    return day, wolf_health, wolf_hunger

def handle_recruit(wolf_health, wolf_hunger, pack_size):
    print("\n--- SEARCHING FOR PACK ---")
    print("You howl into the night, waiting for a response...")

    # 50% Chance to find a friend vs. a rival/nothing
    search_roll = random.randint(1, 10)

    if search_roll > 5:
        print("🐺 A stray wolf emerges from the shadows and bows to you.")
        print("🐾 You gained a pack member!")
        pack_size += 1
    else:
        print("Silence. Or worse... a rival pack chases you off!")
        print("You ran away, but lost energy.")
        wolf_health -= 10

    # Searching always makes you hungry, success or fail
    wolf_hunger += 10
    return wolf_health, wolf_hunger, pack_size

def check_death_status(wolf_health, wolf_hunger):
    """Checks if the wolf is dead by injury or starvation and returns True if Game Over"""
    if wolf_health <= 0:
        print("\n--- GAME OVER ---")
        print("You have sustained too many injuries. Your wolf fades away.")
        return True

    if wolf_hunger >= 100:
        print("\n--- GAME OVER ---")
        print("You starved to death")
        return True

    else:
        return False

# --- SECTION 3: THE MAIN LOOP ---
# This loop will continue to run until wolf_health is 0 or game_running is false.
while wolf_health > 0 and game_running == True:

    # A. Display Status
    display_status(high_score, day, wolf_health, wolf_hunger, pack_size)

    # B. Get User Input
    choice = input("What do you want to do?")

    # C. Logic Handling (The "Brain")
    if choice == "1":
        wolf_health, wolf_hunger = handle_hunt(wolf_health, wolf_hunger, pack_size)

        # 5. Clamping (Data Validation)
        # This prevents weird bugs like: "Hunger -20" or "Health: 105"
        if wolf_hunger < 0:
            wolf_hunger = 0
        if wolf_health > 100:
            wolf_health = 100

    elif choice == "2":
        day, wolf_health, wolf_hunger = handle_rest(day, wolf_health, wolf_hunger)

        # --- CLAMPING LOGIC ---
        # If Health goes over 100, reset it to 100.
        if wolf_health > 100:
            wolf_health = 100
            print("You feel rested, full health has been restored.")

        # Warn the user if they are getting too hungry while they sleep.
        if wolf_hunger > 80:
            print("WARNING: You are waking up extremely hungry!")

    elif choice == "3":
        # The variables receive the updated values returned by the function.
        wolf_health, wolf_hunger, pack_size = handle_recruit(wolf_health, wolf_hunger, pack_size)

        if wolf_hunger < 0:
            wolf_hunger = 0
        if wolf_health > 100:
            wolf_health = 100

    elif choice == "4":
        print("The forest fades away...")
        print("You have chosen to give up.")
        game_running = False

    else:
        # Error handling for bad input
        print("That is not a valid choice. Try again.")

    # D. Check for Death (Safety Check)
    # The game_running variable is set to False only if the function returns True (dead)
    if check_death_status(wolf_health, wolf_hunger):
        game_running = False
        
# Check if the player set a new record.
if day > high_score:
    print("🏆 NEW HIGH SCORE! 🏆")

    with open("highscore.txt", "w") as f:
        # We must convert the integer back to a string before writing to the file.
        f.write(str(day))

# --- SECTION 3: GAME OVER ---
print("-" * 30)
print(f"GAME OVER. You survived for {day} days!")
print("Thanks for playing!")