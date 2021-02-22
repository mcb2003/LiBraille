import wx

class PreferenceValue(wx.TextCtrl):
    """ A text box that is bound to , and kept in sync with,a configuration value. """
    def __init__(self, config, config_path, default = "", *args, **kwargs):
        # Initialise the base class
            super().__init__(*args, **kwargs)
            self.config = config
            self.config_path = config_path
            self.default = default
            # Initialise with the current value of the setting
            self.SetValue(self.config.Read(self.config_path, self.default))
            # Register an event handler on text-change events
            self.Bind(wx.EVT_TEXT, self.on_update)

    def on_update(self, evt):
        # Update the specified config value
        self.config.Write(self.config_path, self.GetValue())
        # This event is processed
        evt.Skip()
