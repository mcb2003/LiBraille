import wx

from .preference_value import PreferenceValue

class PreferencesEditor(wx.PreferencesEditor):
    def __init__(self, config):
        # Initialise the superclass
        super().__init__()
        # Create and add the pages
        self.general = GeneralPreferencesPage(config)
        self.AddPage(self.general)

class GeneralPreferencesPage(wx.StockPreferencesPage):
    def __init__(self, config):
        super().__init__(wx.StockPreferencesPage.Kind_General)
        self.config = config

    def CreateWindow(self, parent):
        # THe main container window
        panel = wx.Panel(parent)
        # Create a grid bag sizer to lay out our components
        grid = wx.GridBagSizer(hgap=5, vgap=5) # hgap and vgap add spacing between items
        # Wrap width:
        wr_lbl1 = wx.StaticText(panel, label="Braille Wrap Width")
        # This is a SpinCtrl because is *must* be an integer
        wr_val = wx.SpinCtrl(panel)
        # Mirror the currently set width from saved settings
        wr_val.SetValue(self.config.ReadInt("engine/wrap-width", 40))
        # Update settings when the SpinCtrl is changed
        wr_val.Bind(wx.EVT_SPINCTRL, self.on_wr_update)
        wr_val.SetMin(2)
        wr_lbl2 = wx.StaticText(panel, label="characters")
        # Register all the widgets with the sizer
        grid.Add(wr_lbl1, pos=(0, 0))
        grid.Add(wr_val, pos=(0, 1))
        grid.Add(wr_lbl2, pos=(0, 2))

        # Heading labels
        grid.Add(wx.StaticText(panel, label="Heading Conversion:"), pos=(1, 0), span=(1, 3))
        grid.Add(wx.StaticText(panel, label="Level"), pos=(2, 0))
        grid.Add(wx.StaticText(panel, label="Prefix"), pos=(2, 1))
        grid.Add(wx.StaticText(panel, label="SUffix"), pos=(2, 2))
        # Heading preferences
        heading_prefs = []
        for i in range(6):
            heading_prefs.append(HeadingPreferences(panel, i+1, self.config))
            heading_prefs[i].add_to(grid, i+3) # First row already taken

        # Let the sizer recalculate the positions and sizes of all items
        panel.SetSizerAndFit(grid)

        return panel

    def on_wr_update(self, evt):
        """ Called when the user changes the wrap width. """
        self.config.WriteInt("engine/wrap-width", evt.GetPosition())
        evt.Skip()

class HeadingPreferences(object):
    def __init__(self, parent, level: int, config):
        self.level = level
        self.label = wx.StaticText(parent, label=str(self.level))
        self.prefix = PreferenceValue(config, f"engine/heading-{self.level}/prefix", "", parent)
        self.suffix = PreferenceValue(config, f"engine/heading-{self.level}/suffix", "", parent)

    def add_to(self, grid: wx.GridBagSizer, row: int):
        """ Add all elements to the specified row of the grid. """
        grid.Add(self.label, pos=(row, 0))
        grid.Add(self.prefix, pos=(row, 1))
        grid.Add(self.suffix, pos=(row, 2))
