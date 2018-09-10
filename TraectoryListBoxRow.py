import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango


# Доработанный словарь цветов по-умолчанию с генератором и геттером
class __DefaultColorDictionary(dict):
    # геттер по ключу
    def get(self, key, default=0):
        return Gdk.RGBA(*dict.get(self, key, default))

    # генератор, выдает кортеж из ключа и цвета,
    def generator(self):
        for i in list(dict.items(self)):
            yield (i[0], Gdk.RGBA(*i[1]))

    def __setattr__(self, key, value):
        raise AttributeError("This class can not assign any attributes")  # нельзя присваивать никаких аттрибутов


# Закидываем в словарь значения
DefaultColors = __DefaultColorDictionary(
    red=(1.0, 0.0, 0.0, 1.0),
    blue=(0.0, 0.0, 1.0, 1.0),
    green=(0.0, 1.0, 0.0, 1.0)
)


# виджет GTK ListBoxRow, для возможности добавления нужных в проекте строк
class TraectoryListBoxRow(Gtk.ListBoxRow):
    def __init__(self, text):
        Gtk.ListBoxRow.__init__(self)  # инициализируем родителя
        self.checkButton = Gtk.CheckButton()  # входящий в строку checkButton
        self.checkButton.set_label('')  # checkButton специально без текста, если текст помещать в нее
        # она захватывает большую часть пространства
        self.checkButton.set_property("margin_left", 5)  # ставим отступы со всех сторон
        self.checkButton.set_property("margin_top", 2)
        self.checkButton.set_property("margin_bottom", 2)

        self.label = Gtk.Label()
        self.label.set_text(text)
        self.label.set_property("margin_right", 5)
        self.label.set_property("margin_top", 2)
        self.label.set_property("margin_bottom", 2)

        # эти строки - плод страданий
        self.label.modify_font(Pango.FontDescription("Tahoma 10"))  # размер и стиль шрифта
        # self.label.set_property("max_width_chars", 25)  # максимальная ширина метки в символах
        self.label.set_property("ellipsize", Pango.EllipsizeMode.END)  # метка будет сжиматься в конце
        self.label.set_property("xalign", 0)  # метка выравнивается по левую сторону

        self.colorButton = Gtk.ColorButton()
        self.colorButton.set_property("margin_top", 2)
        self.colorButton.set_property("margin_bottom", 2)
        self.colorButton.connect("color-set", self.onColorChosen)   # вызывается ф-ия, при смене цвета

        image = Gtk.Image(stock=Gtk.STOCK_REMOVE)  # картинка на кнопку с удалением строки
        self.deleteRowButton = Gtk.Button(label=None, image=image)  # кнопка удаления строки
        self.deleteRowButton.set_property("margin_left", 5)  # ставим отступы со всех сторон
        self.deleteRowButton.set_property("margin_right", 5)
        self.deleteRowButton.set_property("margin_top", 2)
        self.deleteRowButton.set_property("margin_bottom", 2)
        self.deleteRowButton.connect("clicked", self.deleteRowButton_Click)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)  # коробка для внутреностей
        box.pack_start(self.checkButton, False, False, 0)  # упаковываем checkbutton и кнопку удаления
        box.pack_start(self.label, False, False, 0)
        box.pack_end(self.deleteRowButton, False, False, 0)  # пакуем с конца
        box.pack_end(self.colorButton, False, False, 0)  # упаковываем цветную метку
        self.add(box)  # добавляем коробку в строку

    def deleteRowButton_Click(self, w):
        return self.deleteRowCallBack(self, w)

    def deleteRowCallBack(self, row, w):  # калл-бэк ф-ия
        pass

    def onColorChosen(self, userData):  # ф-ия вызывается при смене цвета
        pass


if __name__ == "__main__":
    print(DefaultColors.get("red"))
    generator = DefaultColors.generator()
    print(generator.__next__())
    print(generator.__next__())
    print(generator.__next__())
