from .jsontools import JsonVPL
from .check import Check
from .remote_md import RemoteMd, Title, RemoteCfg
from .html import HTML
from .cases import Cases
from .log import Log
from .tree import Tree
from .mdpp import Mdpp

from typing import Optional
import subprocess
import os
import shutil

def norm_join(*args):
    return os.path.normpath(os.path.join(*args))

class Actions:
    def __init__(self, source_dir, remote_config: Optional[str]=None):
        self.cache = norm_join(source_dir, ".cache")
        self.target = norm_join(self.cache, "mapi.json")
        self.source_dir = source_dir
        self.hook = os.path.basename(os.path.abspath(source_dir))
        Log.debug("hook", self.hook)
        self.source_readme = norm_join(self.source_dir, "Readme.md")
        self.remote_readme = norm_join(self.cache, "Readme.md")
        self.target_html = norm_join(self.cache, "q.html")
        self.title = ""
        self.cases = norm_join(self.cache, "q.tio")
        self.config_json = norm_join(self.source_dir, "config.json")
        self.mapi_json = norm_join(self.cache, "mapi.json")
        self.draft_tree = {}
        self.cache_src = norm_join(self.cache, "lang")
        self.vpl = None
        self.remote_config: Optional[str] = remote_config

    def validate(self):
        if not os.path.isdir(self.source_dir):
            print(f"fail: {self.source_dir} is not a directory")
            return False
        if not os.path.isfile(self.source_readme):
            print(f"fail: {self.source_readme} not found")
            return False
        return True

    def load_title(self):
        self.title = Title.extract_title(self.source_readme)

    def create_cache(self):
        if not os.path.exists(self.cache):
            os.makedirs(self.cache)
        return self
    
    def recreate_cache(self):
        shutil.rmtree(self.cache)
        os.makedirs(self.cache)
        return self
    
    def check_rebuild(self):
        [_path, changes_found] = Check.check_rebuild(self.source_dir, self.target)
        return changes_found
    
    def remote_md(self, disable_preamble=False):
        cfg = RemoteCfg()
        if self.remote_config is not None:
            cfg.read(self.remote_config)
        else:
            cfg_path = RemoteCfg.search_cfg_path(self.source_dir)
            if cfg_path is None:
                Log.write("fail: no remote.cfg found in the parent folders")
                exit()
            cfg.read(cfg_path)
        RemoteMd.run(cfg, self.source_readme, self.remote_readme, self.hook, disable_preamble)
        Log.write("RemoteMd ")
    
    # uses pandoc to generate html from markdown
    def html(self):
        title = Title.extract_title(self.source_readme)
        HTML.generate_html(title, self.remote_readme, self.target_html, True)
        Log.write("HTML ")

    # uses tko to generate cases file
    def build_cases(self):
        Cases.run(self.cases, self.source_readme, self.source_dir)
        Log.write("Cases ")

    def copy_drafts(self):
        source_src = norm_join(self.source_dir, "src")
        if os.path.isdir(source_src):
            Tree.deep_filter_copy(source_src, self.cache_src, self.draft_tree, 5)
            Log.debug("Drafts ", self.draft_tree)

    def run_local_sh(self):
        local_sh = norm_join(self.source_dir, "local.sh")
        actual_chdir = os.getcwd()
        if os.path.isfile(local_sh):
            os.chdir(self.source_dir)
            subprocess.run("bash local.sh", shell=True)
            os.chdir(actual_chdir)

    def init_vpl(self):
        self.vpl = JsonVPL(self.title, open(self.target_html).read())
        self.vpl.set_cases(self.cases)
        if self.vpl.load_config_json(self.config_json, self.source_dir):
            Log.write("Required ")
        if self.vpl.load_draft_tree(self.draft_tree, self.cache_src):
            Log.write("Drafts ")
        Log.write("] ")

    def create_mapi(self):
        open(self.mapi_json, "w").write(str(self.vpl) + "\n")
        Log.write("DONE")

    def clean(self):
        os.remove(self.cases)
        os.remove(self.target_html)

    # run mdpp script on source readme
    def update_markdown(self):
        Mdpp.update_file(self.source_readme)
