from lynx_gui.arrera_lynx import*
from src.create_conf import create_conf

def end(w:aTk):
    w.destroy()
    print("FIN")

def main():
    w = aTk(theme_file="asset/theme/theme_default.json")
    a = arrera_lynx(master=w,
                   conf_file="json_file/configLynx.json",
                   gest=create_conf(),
                    fnc_end=lambda : end(w))
    w.geometry(a.get_geometry())
    a.active()
    w.mainloop()


if __name__ == '__main__':
    main()
