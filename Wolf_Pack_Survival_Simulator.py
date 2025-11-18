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

# --- SECTION 1: SETUP ---
# Sets the starting stats for your wolf.
wolf_health = 100
wolf_hunger = 0
pack_size = 0
day = 1
game_running = True

print("Welcome to the Wolf Pack Survival Game!")
print("You are a lone wolf. Survive as long as you can.")

# --- SECTION 3: THE MAIN LOOP ---
# This loop will continue to run until wolf_health is 0 or game_running is false.
while wolf_health > 0 and game_running == True:

    # A. Display Status
    print("-" * 30)
    print(f"DAY: {day} | HEALTH: {wolf_health} | HUNGER: {wolf_hunger} | PACK SIZE: {pack_size}")
    print("Options: [1] Hunt  [2] Rest  [3] Recruit  [4] Quit")

    # B. Get User Input
    choice = input("What do you want to do?")

    # C. Logic Handling (The "Brain")
    if choice == "1":
        print("\n--- THE HUNT ---")
        print("You creep silently into the forest, sniffing the air...")

        # 1. Define Your Prey List
        possible_prey = ["Rabbit", "Deer", "Wild Turkey", "Bison"]

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

        # 5. Clamping (Data Validation)
        # This prevents weird bugs like: "Hunger -20" or "Health: 105"
        if wolf_hunger < 0:
            wolf_hunger = 0
        if wolf_health > 100:
            wolf_health = 100

    elif choice == "2":
        # This is where the resting logic goes
        print("\n--- RESTING ---")
        print("You curl up in your den to rest. The sun sets and rises again.")

        day += 1

        # The Basic Math
        wolf_health += 15
        wolf_hunger += 5

        # --- CLAMPING LOGIC ---
        # If Health goes over 100, reset it to 100.
        if wolf_health > 100:
            wolf_health = 100
            print("You feel fully rested! (Health maxed out)")

        # Warn the user if they are getting too hungry while they sleep.
        if wolf_hunger > 80:
            print("WARNING: You are waking up extremely hungry!")

    elif choice == "3":
        print("\n--- SEARCHING FOR PACK ---")
        print("You howl into the night, waiting for a response...")

        # 50% Chance to find a friend vs. a rival/nothing
        search_roll = random.randint(1, 10)

        if search_roll > 5:
            print("A stray wolf emerges from the shadows and bows to you.")
            print("You gained a pack member!")
            pack_size += 1
        else:
            print("Silence. Or worse... a rival pack chases you off!")
            print("You ran away, but lost energy.")
            wolf_health -= 10

        # Searching always makes you hungry, success or fail
        wolf_hunger += 10

    elif choice == "4":
        print("The forest fades away...")
        print("You have chosen to give up.")
        game_running = False

    else:
        # Error handling for bad input
        print("That is not a valid choice. Try again.")

    # D. Check for Death (Safety Check)
    if wolf_health <= 0:
        print("\n--- GAME OVER ---")
        print("You have sustained too many injuries. Your wolf fades away.")
        game_running = False

    if wolf_hunger >= 100:
        print("\n--- GAME OVER ---")
        print("You starved to death")
        wolf_health = 0 # Kill the wolf to stop the loop

# --- SECTION 3: GAME OVER ---
print("-" * 30)
print(f"GAME OVER. You survived for {day} days!")
print("Thanks for playing!")