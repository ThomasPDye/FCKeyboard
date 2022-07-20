import os
import FreeCADGui as Gui
import FreeCAD as App
from freecad.FCKeyboard import ICONPATH


class KeyboardWorkbench(Gui.Workbench):
    """
    class which gets initiated at startup of the gui
    """

    MenuText = "Keyboard Workbench"
    ToolTip = "a simple keyboard workbench"
    Icon = os.path.join(ICONPATH, "template_resource.svg")
    toolbox = []

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        """
        This function is called at the first activation of the workbench.
        here is the place to import all the commands
        """
        from freecad.FCKeyboard.klepy import keyboard
        App.Console.PrintMessage("switching to FCKeyboard\n")

        self.appendToolbar("Tools", self.toolbox)
        self.appendMenu("Tools", self.toolbox)

    def Activated(self):
        '''
        code which should be computed when a user switch to this workbench
        '''
        pass

    def Deactivated(self):
        '''
        code which should be computed when this workbench is deactivated
        '''
        pass


Gui.addWorkbench(KeyboardWorkbench())
