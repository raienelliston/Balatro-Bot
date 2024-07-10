import modules.game_controller as gc

def main():
    controller = gc.Controller()
    if controller == False:
        print("Controller not created")
        return False

main()