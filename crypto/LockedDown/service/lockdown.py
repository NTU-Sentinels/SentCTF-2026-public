import os
import time

#The following are the helper functions of this program

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.02):
    for c in text:
        print(c, end="", flush = True)
        time.sleep(delay)
    print()


#Player attributes

inventory = []
recovered_evidence = {}

visited = set()

current_room = "Lobby"

#Rooms

rooms = {
    "Lobby": {
        "description":
            "The archive building is eerily quite.\n"
            "Emergency lights illuminate the hallway.",
        
        "connections":
            ["Security Office",
             "Storage Room",
             "Maintenance Room"],
        

        "searched": False,

        "item":
            ("Security Keycard",
             "A level 2 security keycard. It might be useful for accessing restricted areas.")

    },

    "Storage Room":{
        "description":
            "The storage room is filled with boxes and shelves.\n"
            "You notice a faint humming sound coming from one of the shelves.",
        
        "connections":
            ["Lobby"],
        
        "searched": False,

        "item":
            ("incident_report.txt",
             "detailed incident report of the lockdown event.")
        
    },

    "Maintenance Room":{
        "description":
            "A small workshop used by the technicians. Tools and equipment are scattered around.\n",

        "connections":
            ["Lobby"],
        
        "searched": False,

        "item":
            ("maintenance_log.txt",
             "A log file that contains routine maintenance records.")
    },

    "Security Office":{
        "description":
            "Security monitoring room.\n",
        
        "connections":
            ["Lobby",
             "Server Room"],
        
        "searched": False,

        "item":
            ("developer_notes.txt",
             "A developer notes has been recovered.")
    },

    "Server Room":{
        "description":
            "There are rows of servers that still hums despite the attack.\n",
        
        "connections":
            ["Security Office",
            "Exit Door",
            "Server Room's Locker"],
        
        "searched": False,

        "locked": True,

        "item":
            ("public.txt",
             "An RSA public key recovered.")
    },

    "Exit Door":{
        "description":
            "A heavy emergency blast door that leads you outside.\n",
        
        "connections":
            ["Server Room"],

        "searched": False,

        "locked": False
    },

    "Server Room's Locker":{
        "description":
            "A metallic locker at the corner of the room which is left unlocked.\n",

        "connections":
            ["Server Room"],
        
        "searched": False,
        
        "item":
            ("encrypted_token.txt",
             "It seems like it is a ciphertext. What could it mean?")
    }
        
}


def load_evidence_text(item):

    filepath = os.path.join("evidence", item)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    except FileNotFoundError:
        return None

#Searching rooms

def search_room():
    room = rooms[current_room]

    if room["searched"]:
        slow_print("Nothing else was found.")
        return
    
    room["searched"] = True

    slow_print("Searching room. . .")
    time.sleep(1)

    if "item" not in room:
        slow_print("Nothing was found.")
        return
    
    item, desc = room["item"]

    inventory.append(item)
    slow_print(f"You found {item}!")

    
    content = load_evidence_text(item)

    if content is not None:
        recovered_evidence[item] = item

        slow_print(f"{item} has been added to your recovered evidence.")
    
    if item == "Security Keycard":
        slow_print("Server Room access unlocked!")

        rooms["Server Room"]["locked"] = False

def read_evidence():

    files = [item for item in inventory if item in recovered_evidence]

    if not files:
        slow_print("No evidence has been recovered yet.")
        return

    print("\nRecovered Evidence\n")

    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    try:
        choice = int(input("\nSelect file: ")) - 1
    except:
        return

    if choice < 0 or choice >= len(files):
        return

    filename = files[choice]

    clear()

    print("=" * 60)
    print(filename)
    print("=" * 60)

    content = load_evidence_text(filename)

    if content is None:
        print("[Evidence file missing.]")
    else:
        print(content)

    input("\nPress Enter to continue...")


#Movement between rooms

def move():
    global current_room

    room = rooms[current_room]
    print()

    for i, r in enumerate(room["connections"], 1):
        print(f"{i}. {r}")
    
    try:
        choice = int(input("Choose a room to move to: ")) - 1
        target = room["connections"][choice]
    except:
        return

    if rooms[target].get("locked", False):
        slow_print(f"{target} is locked. You need a keycard to access it.")
        return
    
    current_room = target


#Inventory management

def show_inventory():
    print()

    if not inventory:
        print("Your inventory is empty.")
        return
    
    for item in inventory:
        print("-", item)

#Exit Door access

def exit_terminal():

    token = input("Enter Emergency Access Token:\n")

    with open("access_token.txt", "r") as f:
        ACCESS_TOKEN = f.read().strip()
    
    if token == ACCESS_TOKEN:
        slow_print("Access granted. The door opens.")

        with open("flag.txt", "r") as f:
            print("\n", f.read())
        
        exit()
    
    slow_print("Access denied. The door remains closed.")


#Main loop

if __name__ == "__main__":
    while True:
        clear()

        print("=" * 50)
        print("      ARCHIVE LOCKDOWN SYSTEM")
        print("=" * 50)

        print(f"\nCurrent Room : {current_room}\n")

        print(rooms[current_room]["description"])

        print("\n")

        print("1. Move")

        print("2. Search Room")

        print("3. Inventory")

        print("4. Read Evidence")

        if current_room == "Exit Door":

            print("5. Enter Access Token")

            print("6. Quit")

        else:

            print("5. Quit")

        choice = input("\n> ")

        if choice == "1":

            move()
            input("\nPress Enter...")

        elif choice == "2":

            search_room()
            input("\nPress Enter...")

        elif choice == "3":

            show_inventory()
            input("\nPress Enter...")

        elif choice == "4":
            read_evidence()

        elif choice == "5" and current_room == "Exit Door":

            exit_terminal()
            input()

        elif (choice == "5" and current_room != "Exit Door") or \
            (choice == "6" and current_room == "Exit Door"):

            break
