import sqlite3
cricket=sqlite3.connect('fantasycricket.db')
objcricket=cricket.cursor()

# Creating a Table for Match
# objcricket.execute('''CREATE TABLE Match(
#     Player string(20) PRIMARY KEY,
#     Scored integer NOT NULL,
#     Faced integer NOT NULL,
#     Fours integer,
#     Sixes integer,
#     Bowled integer,
#     Maiden intger,
#     Given integer,
#     Wkts integer,
#     Catches integer,
#     Stumping integer,
#     RO integer
# )''')
# cricket.commit()

# Creating a Table for Teams
# objcricket.execute('''CREATE TABLE Teams(
#     Players string(20) References Match(Player),
#     Name varchar2 NOT NULL,
#     value integer
# )''')
# cricket.commit()

# Creating a Table for Stats
    # objcricket.execute('''CREATE TABLE Stats(
    #     Players string(20) References Match(Player),
    #     Matches integer,
    #     Runs integer,
    #     "100s" integer,
    #     "50s" integer,
    #     value integer,
    #     ctg text
    # )''')
# cricket.commit()

objcricket.execute('''INSERT INTO Match (Player, Scored, Faced, Fours, Sixes, Bowled, Maiden, Given, Wkts, Catches, Stumping, RO) VALUES ("Kohli", 102, 98, 8, 2, 0, 0, 0, 0, 0, 0, 1), ("Yuvraj", 12, 20, 1, 0, 48, 0, 36, 1, 0, 0, 0), ("Rahane", 49, 75, 3, 0, 0, 0, 0, 0, 1, 0, 0), ("Dhawan", 32, 35, 4, 0, 0, 0, 0, 0, 0, 0, 0), ("Dhoni", 56, 45, 3, 1, 0, 0, 0, 0, 3, 2, 0), ("Axar", 8, 4, 2, 0, 48, 2, 35, 1, 0, 0, 0), ("Pandya", 42, 36, 3, 3, 30, 0, 25, 0, 1, 0, 0), ("Jadeja", 18, 10, 1, 1, 60, 3, 50, 2, 1, 0, 1), ("Kedar", 65, 60, 7, 0, 24, 0, 24, 0, 0, 0, 0), ("Ashwin", 23, 42, 3, 0, 30, 2, 45, 6, 0, 0, 0), ("Umesh", 0, 0, 0, 0, 54, 0, 50, 4, 1, 0, 0), ("Bumrah", 0, 0, 0, 0, 60, 2, 49, 1, 0, 0, 0), ("Bhuwaneshwar", 15, 12, 2, 0, 60, 1, 46, 2, 0, 0, 0), ("Rohit", 46, 65, 5, 1, 0, 0, 0, 0, 1, 0, 0), ("Kartick", 29, 42, 3, 0, 0, 0, 0, 0, 2, 0, 1);''')
cricket.commit()

objcricket.execute('''INSERT INTO Stats (Players, Matches, Runs, 100s, 50s, value, ctg) VALUES ("Kohli", 189, 8257, 28, 43, "BAT"), ("Yuvraj", 86, 3589, 10, 21, "BAT"), ("Rahane", 158, 5435, 11, 31, "BAT"), ("Dhawan", 25, 565, 2, 1, "AR"), ("Dhoni", 78, 2573, 3, 19, "BAT"), ("Axar", 67, 208, 0, 0, "BWL"), ("Pandya", 70, 77, 0, 0, "BWL"), ("Jadeja", 16, 1, 0, 0, "BWL"), ("Kedar", 111, 675, 0, 1, "BWL"), ("Ashwin", 136, 1914, 0, 10, "AR"), ("Umesh", 296, 9496, 10, 645, "WK"), ("Bumrah", 73, 1365, 0, 8, "WK"), ("Bhuwaneshwar", 17, 289, 0, 2, "AR"), ("Rohit", 304, 8701, 14, 52, "BAT"), ("Kartick", 11, 111, 0, 0, "AR");''')
cricket.commit()


objcricket.execute('''SELECT Players,Name,value FROM Teams''')
# print(objcricket.fetchall())
for i in objcricket.fetchall():
    print(i[2])
cricket.close()