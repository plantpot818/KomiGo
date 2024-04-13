def make_board():
  global board
  board = []
  topbar = []
  size = 9

  # Create top row for all the letters of the board
  for i in range(size + 1): # plus 1 to account for blank at the start
    if i == 0:
      topbar.append(" ")
    else:
      topbar.append(f"{chr(64 + i)}") # 64 since i increases to 1 during 2nd cycle
  board.append(topbar)

  # Create subsequent rows for the numbers and empty spaces in the board
  for i in range(size):
    # add a space at the end to use as border later
    board.append([i+1] + ["." for i in range(size)] + [" "])

  # Create last empty row for usage as border
  board.append([" " for i in range(size + 2)])

  # Create the player (starts with X)
  global player
  player = "X"
  # Create the points
  global xp
  xp = 0
  global op
  op = 0


def print_board():
  for row in board:
    for _i in row:
      print(_i, end = " ")
    print("")
  

def place_stone(row, col):
  board[row][col] = player


def switch_player():
  global player
  player = "O" if player == "X" else "X"


def dead_stones():
  # records points for captures and replaces captured stones
  global xp
  global op
  for i in friend_set:
    row1, col1 = i
    board[row1][col1] = "."
    if player == "X":
      xp += 1
    else:
      op += 1


def captures(row, col):
  # to store friendly neighbour stones
  global friend_set
  friend_set = set()
  # friendly stones that were visited
  global visited_friend
  visited_friend = set()
  # to store enemy neighbour stones
  global enemy_set
  enemy_set = set()
  # swtich adjacent_check to scanning for enemies/ friends
  friend_check = False

  def adjacent_check(ro, co):
    # to check up/down/left/right
    for i in range(4):
      c = 0
      r = 0
      # up
      if i == 0: 
        r = ro - 1
        c = co
      # down
      elif i == 1:
        r = ro + 1
        c = co
      # left
      elif i == 2:
        r = ro
        c = co - 1
      # right
      elif i == 3:
        r = ro
        c = co + 1
      
      # friend/ enemy check
      if friend_check is False:
        switch_player()
        if board[r][c] == player:
          enemy_set.add((r,c))
        switch_player()
      else: 
        switch_player()
        friend_set.add((ro,co))
        if board[r][c] == player:
          friend_set.add((r,c))
          
        if board[r][c] == ".": # check for stone liberty
          switch_player()
          return False
        switch_player()
  
  # check if any stones are captured for newly placed stone
  # find enemies around placed stone
  adjacent_check(row, col)

  for i in enemy_set:
    row2, col2 = i # location of first close enemy
  
    friend_check = True
    adjacent_check(row2, col2)
    if adjacent_check(row2, col2) is False:
      return False

    while True:
      for j in list(friend_set):
        row3, col3 = j # location of close friend
        if j in visited_friend:
          continue
        else:  
          adjacent_check(row3, col3)
          if adjacent_check(row3, col3) is False:
            return False
          visited_friend.add((row3,col3)) # record the visit after check
          
          # if all visited stones have no liberty (free spaces), they must be captured
          if visited_friend == friend_set:
            return True


def valid_move(move):
  def fixing():
    print("Your move was invalid")
    move = input(f"Player {player} make your move (eg. A1): ")
    return move
    
  while True:
    # quitting function
    if move == "quit": 
      return ("AMONG", "US")

    # checks length of input move
    if len(move) != 2:
      move = fixing()
      continue

    # checks if the move is in the correct format
    if not(move[0].isalpha() and move[1].isnumeric()): 
      move = fixing()
      continue

    # checks if the move is out of range
    if not (ord("A") <= ord(move[0]) <= ord("I")) and not (1 <= int(move[1]) <= 9):
      move = fixing()
      continue

    c, r = move
    row = int(r)
    col = ord(c) - 64

    # checks if space is valid for placement
    if board[row][col] != ".":
      move = fixing()
      continue

    return row, col


def play_komi():
  print("Welcome to Komi! Capture 5 enemy stones to win")
  make_board()
  print_board()

  # The game begins
  while True:
    move = input(f"Player {player} make your move (eg. A1): ")
    row, col = valid_move(move)   

    if row == "AMONG" and col == "US":
      print("Qutting...")
      return ""
    
    place_stone(row, col)
    # checks for captures
    if captures(row, col):
      dead_stones()
      if xp >= 5 or op >= 5:
        print(f"X: {xp}/O: {op}")
        print_board()
        print (f"Player {player} wins!")
        return ""
        
    switch_player()
    print(f"X: {xp}/O: {op}")
    print_board()
    continue


play_komi()