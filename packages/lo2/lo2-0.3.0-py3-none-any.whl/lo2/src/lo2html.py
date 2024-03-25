import jinja2
import os

# from  numpy import inf
from .lo2parser import NodeState


def create_directory(directory_path):
    # 判断目录是否存在
    if not os.path.exists(directory_path):
        # 如果不存在，则创建目录
        os.makedirs(directory_path)
        print(f"目录 {directory_path} 创建成功")
    else:
        print(f"目录 {directory_path} 已存在")


class MVC:
    def __init__(self):
        self.data = {}
        self._view = {}

    def model(self, data):
        self.data = data
        return self

    def _to_overview(self):
        self._view["overview"] = self.data

    def _to_timeline(self):
        self._view["timeline"] = self.data

    def to_controller(self, view_type):
        """
        timeline
        overview
        """
        if view_type == "timeline":
            self._to_timeline()
        elif view_type == "overview":
            self._to_overview()
        return self

    # get this file directory
    def _get_path(self):
        return os.path.dirname(os.path.realpath(__file__))

    # 获取path2相对于path1的相对路径
    def _get_relative_path(self, path1, path2):
        return os.path.relpath(path2, path1)

    def _to_index_html(self, path):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
        # 从path相对路径获取模板
        temp = env.get_template(
            self._get_relative_path(
                path, f"{self._get_path()}/template/statics/index.html"
            )
        )
        out_dir = os.path.join(path, "html-out")
        create_directory(out_dir)

        out = temp.render(views=self._view.keys())
        with open(
            os.path.join(path, out_dir, f"index.html"), "w", encoding="utf-8"
        ) as f:
            f.writelines(out)
            f.close()

    def _result_to_overview_html(self, result, path):
        pass

    def _result_to_timeline_html(self, result, path):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))
        # 从path相对路径获取模板
        temp = env.get_template(
            self._get_relative_path(
                path, f"{self._get_path()}/template/statics/timeline.html"
            )
        )

        out_dir = os.path.join(path, "html-out")

        create_directory(out_dir)
        out = temp.render(**self._view["timeline"])
        with open(
            os.path.join(path, out_dir, f"timeline.html"), "w", encoding="utf-8"
        ) as f:
            f.writelines(out)
            f.close()

    def _resource_copy(self, path):
        # 复制静态资源
        static_dir = os.path.join(path, "html-out")
        create_directory(static_dir)
        # 复制 png 图片到 static_dir
        for file in os.listdir(os.path.join(self._get_path(), "template", "statics")):
            if file.endswith(".png"):
                os.system(
                    f"cp -r {self._get_path()}/template/statics/{file} {static_dir}"
                )

    def to_html(self, outdir="./"):
        print(self._view.keys())
        for k, v in self._view.items():
            if k == "timeline":
                self._result_to_timeline_html(v, outdir)
            elif k == "overview":
                self._result_to_overview_html(v, outdir)

        self._to_index_html(outdir)
        self._resource_copy(outdir)
        return self
