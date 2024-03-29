from manim import *


class T2M(Scene):
    def __init__(self, t: str):
        config["pixel_width"] = 900
        config["pixel_height"] = 160

        super().__init__()
        t2c_dict: dict = {}
        for i, c in enumerate(t):
            if c != ' ':
                r_color = random_color()
                if str(r_color) == '#000000':
                    r_color = '#ffffff'

                t2c_dict['[{0}:{1}]'.format(i, i + 1)] = r_color

        mtext = Text(t, t2c=t2c_dict, fill_opacity=1, weight='BOLD')
        self.play(Create(mtext))
        self.play(mtext.animate.scale(2))

        self.wait()


def t2m(text: str, out_filename: str = "t2m", quality: str = "low_quality", out_format: str = 'gif',
        preview: bool = False):
    with tempconfig(
            {'output_file': out_filename, 'quality': quality, 'format': out_format, 'preview': preview}):
        scene = T2M(t=text)
        scene.render()


if __name__ == '__main__':
    t2m("BTC-USDT")
