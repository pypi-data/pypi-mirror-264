import json
import subprocess
import os
import shutil
import sys
from superide import __container_engine__

class Toolchain:
    def __init__(self, image_name, project_directory):
        check_container_engine_availability()
        self.image_name = image_name
        self.project_directory = project_directory
        self.contain_project_directory = "/app/project"
        self.check_image()
        
        
    def check_image(self):
        try:
            output = subprocess.check_output([__container_engine__, "images", "-q", self.image_name])
            if output:
                return
            else:
                print(f"The image '{self.image_name}' does not exist locally, will be pulled.")
                # 拉取镜像
                subprocess.run([__container_engine__, 'pull', self.image_name])

        except subprocess.CalledProcessError:
            print("Failed to get image.")
            sys.exit(1)

    def init_project(self):
        # 文件夹非空则不能创建项目
        if(len(os.listdir(self.project_directory)) != 0):
            print("can't init project in Non empty folder")
            sys.exit(1)
        container_name = 'CopyExampleProjectDemo'
        source_path = '/app/ExampleProject'
        destination_path = self.project_directory
        try:
            # 创建容器
            create_command = [__container_engine__, 'create', '--name', container_name, self.image_name]
            subprocess.run(create_command)

            # 复制文件
            copy_command = [__container_engine__, 'cp', f'{container_name}:{source_path}', destination_path]
            subprocess.run(copy_command)

            # 删除容器（可选）
            delete_command = [__container_engine__, 'rm', container_name]
            subprocess.run(delete_command)

            # 移动到项目目录
            source_path = destination_path + '/ExampleProject/'
            for file in os.listdir(source_path):
                src_file = os.path.join(source_path, file)
                dst_file = os.path.join(destination_path, file)
                shutil.move(src_file, dst_file)
            clear_command = ['rm', '-rf', source_path]
            subprocess.run(clear_command)
        except Exception:
            print("init project failed")
            sys.exit(1)

    def _get_tools(self):
        with open(f'{self.project_directory}/.vscode/tasks.json') as file:
            config = json.load(file)
        for task in config['tasks']:
            if task['label'] == 'Build':
                self.build_task = task
            if task['label'] == 'Check':
                self.check_task = task
            if task['label'] == 'Run':
                self.run_task = task

    def build(self):
        self._get_tools()
        build_command = self.build_task["command"]+ " " + " ".join(self.build_task["args"])
        return self.container_command(build_command)

    def check(self):
        self._get_tools()
        check_command = self.check_task["command"]+ " " + " ".join(self.check_task["args"])
        return self.container_command(check_command)
    
    def run(self):
        self._get_tools()
        run_command = self.run_task["command"]+ " " + " ".join(self.run_task["args"])
        return self.container_command(run_command)

    def container_command(self, command):
        return " ".join([__container_engine__, "run","-it","--rm", "-v", self.project_directory+":"+self.contain_project_directory, self.image_name, command])
    

def get_container_engine_path():
    try:
        path = subprocess.check_output(['which', __container_engine__]).decode().strip()
        return path
    except subprocess.CalledProcessError:
        return None

def check_container_engine_availability():
    path = get_container_engine_path()
    if path:
        try:
            subprocess.run([path, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print(f"{__container_engine__} is not available.")
            sys.exit(1)
    else:
        print(f"{__container_engine__} not found on the system.")
        sys.exit(1)