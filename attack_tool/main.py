from controller.controller import MenuStateMachine
from commandline.commandlineparser import CommandLineParser
from environment.global_const import GlobalVariables

if __name__ == '__main__':
    
    # Init Classes
    command_line_parser = CommandLineParser()

    # Handle Commandline Input
    args = command_line_parser.get_options()
    

    if args.light_version:
        GlobalVariables.get_instance().set_lite_version(True)
        
    if args.tool and not args.attack or args.attack and not args.tool:
        print('Specify the Tool Name with --tool TOOL-NAME and --attack ATTACK to execute a attack.')
        command_line_parser.print_tool_help()

    elif args.tool and args.attack:
        # Commandline execute Attack
        command_line_parser.handle_tool()

    elif args.playbook:
        # Commandline run Playbook
        if args.playbook == "help":
            command_line_parser.show_playbooks()
        else:
            command_line_parser.run_playbook()
    elif args.testcase and not args.tactic:
        print('Specify the Tactic Name with --tactic TACTIC-NAME and --technique TECHNIQUE-NAME to execute a Testcase.')
        command_line_parser.print_testcase_help()
    elif args.testcase and args.tactic:
        command_line_parser.handle_testcase()
    else:
        # Start Menu
        menu_state_machine = MenuStateMachine()
        menu_state_machine.run()