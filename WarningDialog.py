import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class WarningDialog(Gtk.Dialog):
    def __init__(self, parent, text):
        Gtk.Dialog.__init__(self, "Warning!", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)
        self.label = Gtk.Label(text)
        box = self.get_content_area()
        image = Gtk.Image(stock=Gtk.STOCK_DIALOG_WARNING)
        box.pack_start(image, False, False, 0)
        box.pack_start(self.label, False, False, 0)
        self.add(box)
        self.show_all()


if __name__ == '__main__':
    WarningDialog(Gtk.Window(), "no")
    Gtk.main()
