import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango


class WarningDialog(Gtk.Dialog):
    def __init__(self, parent, text):
        Gtk.Dialog.__init__(self, "Warning!", parent, 0,
                            (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                             Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        self.set_default_size(150, 100)
        self.label = Gtk.Label(text)

        self.label.modify_font(Pango.FontDescription("Tahoma 12"))  # размер и стиль шрифта

        box = self.get_content_area()
        image = Gtk.Image(stock=Gtk.STOCK_DIALOG_WARNING, icon_size=6)
        box.pack_start(image, False, False, 0)
        box.pack_start(self.label, False, False, 0)
        self.show_all()


if __name__ == '__main__':
    WarningDialog(Gtk.Window(), "Удалить траекторию(и)?")
    Gtk.main()
