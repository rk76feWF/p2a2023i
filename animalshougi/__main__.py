if __name__ == "__main__":
    from animalshougi.model import Piece, Game

    def parse_coord(s: str) -> tuple[int, int] | None:
        if len(s) != 2:
            return None
        c = s[0]
        if c == "A":
            file = 0
        elif c == "B":
            file = 1
        elif c == "C":
            file = 2
        else:
            return None
        c = s[1]
        if c == "1":
            rank = 0
        elif c == "2":
            rank = 1
        elif c == "3":
            rank = 2
        elif c == "4":
            rank = 3
        else:
            return None
        return (file, rank)

    def input_line(*args, **kargs) -> str | None:
        try:
            return input(*args, **kargs)
        except KeyboardInterrupt:
            print()
            return None
        except EOFError:
            print()
            return None

    def prompt_input(*args, **kargs) -> str | None:
        a = input_line(*args, **kargs)
        if a is None:
            return a
        a = a.strip()
        while len(a) == 0:
            a = input_line(*args, **kargs)
            if a is None:
                return a
            a = a.strip()
        return a

    g = Game()
    while True:
        cmd = prompt_input("command, drop piece, or move from? ")
        if not cmd:
            break
        cmd = cmd.upper()

        x: Piece | tuple[int, int] | None

        if "HELP".startswith(cmd):
            print(
                end="""\
  help: show this help
  show: show the serial
  load: load game with a serial
  quit: quit the game
  [GgEeCc]: drop the hand piece
  [AaBbCc][123]: move from/to the coord
"""
            )
            continue
        elif "SHOW".startswith(cmd):
            print(g)
            continue
        elif "LOAD".startswith(cmd):
            print(end="read 6 lines.\n")
            lines = []
            for _ in range(6):
                line = input_line()
                if line is None:
                    break
                lines.append(line)
            if len(lines) == 6:
                try:
                    g = Game("\n".join(lines))
                except:
                    print(end="cannot parse game.\n")
            continue
        elif "QUIT".startswith(cmd):
            break
        elif cmd == "G":
            x = Piece.GIRAFFE
        elif cmd == "E":
            x = Piece.ELEPHANT
        elif cmd == "C":
            x = Piece.CHICK
        else:
            x = parse_coord(cmd)

        player = bool(g.turn % 2)

        if type(x) is Piece:
            if 0 < g.hands[player][x]:
                coord_in = prompt_input("                          drop to? ")
                if coord_in:
                    coord = parse_coord(coord_in.upper())
                    if coord:
                        try:
                            g.drop(x, coord)
                            print(g)
                        except ValueError as e:
                            print(e)
                    else:
                        print(end="invalid coord.\n")
            else:
                print(end=f"The player {player} has no {x}.\n")
        elif type(x) is tuple:
            coord_in = prompt_input("                          move to? ")
            if coord_in:
                coord = parse_coord(coord_in.upper())
                if coord:
                    try:
                        g.move(x, coord)
                        print(g)
                    except ValueError as e:
                        print(e)
                else:
                    print(end="invalid coord.\n")
        else:
            print(end="invalid command. type `help` to show usage.\n")
