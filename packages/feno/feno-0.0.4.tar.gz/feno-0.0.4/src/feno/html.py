import subprocess
from subprocess import PIPE

from .css_style import CssStyle

class HTML:
    @staticmethod
    def generate_html(title: str, input_file: str, output_file: str, enable_latex: bool):
        fulltitle = title.replace('!', '\\!').replace('?', '\\?')
        cmd = ["pandoc", input_file, '--css', CssStyle.get_file(), '--metadata', 'pagetitle=' + fulltitle,
            '-s', '-o', output_file]
        if enable_latex:
            cmd.append("--mathjax")
        try:
            p = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            stdout, stderr = p.communicate()
            if stdout != "" or stderr != "":
                print(stdout)
                print(stderr)
        except Exception as e:
            print("Erro no comando pandoc:", e)
            exit(1)

