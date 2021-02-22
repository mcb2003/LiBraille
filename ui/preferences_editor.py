import wx

class PreferencesEditor(wx.PreferencesEditor):
    def __init__(self, config):
        # Initialise the superclass
        super().__init__()
        # Save a reference to the configuration manager for reading and writing settings
        self.config = config
