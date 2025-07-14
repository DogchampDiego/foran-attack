1. # Create a wrapper class
    - include the commands from the implemented Tools 
2. # Create a env class
    - must inherit from /environment/tool_base.py Tool Class
3. # Create a Tool class
    - must inherit from /tools/environment_base.py environment Class
4. # Create a install bash Script
    - includes the install instructions of the Tool
5. # Add Tool in /state/menu_state 
    - under Tools 40-60 add the name of the Tool in CAPS and give it the next free number
    - when the next free number is > 60 you need to adjust the def print_menu() in /help/helper.py
6. # Add Menu in TOOLS dict in /help/helper
    - add the name of the Tool in CAPS at the end of the dict TOOLS
7. # Add Tool in OPTIONS_BASE /help/helper under TOOLS
    - add the name of the Tool in CAPS at the end of the dict OPTIONS_BASE in the sub-dict Tools
7. # Add Tool in OPTIONS_BASE /help/helper under OPTIONS_ATTACK 
    - add the name of the Tool in CAPS at the end of the dict OPTIONS_ATTACK in the phase the tool is in
8. # Add the Tool in /menu/{phase/<phase>|startmenu/tools.py}
    - add the option for the tool in the Tool(Menu) Class and in the Phase Class you want to add the Tool in.