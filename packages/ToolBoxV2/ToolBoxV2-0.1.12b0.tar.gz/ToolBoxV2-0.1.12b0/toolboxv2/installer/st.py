import streamlit as st
import subprocess
import sys
import paramiko

class Installer:
    def __init__(self):
        self.root = st
        self.create_widgets()

    def create_widgets(self):
        python_version = self.get_python_version()
        toolbox_version = self.get_toolbox_version()
        self.root.write(f"Toolbox Version: {toolbox_version}")
        if python_version:
            self.root.write(f"Python-Version: {python_version}")
        else:
            if st.button("Python 3.11 installieren"):
                self.install_python_3_11()
        if st.button("Installieren"):
            self.install_toolbox()
        if st.button("Aktualisieren"):
            self.update_toolbox()
        if st.button("Deinstallieren"):
            self.uninstall_toolbox()

        if st.checkbox("Remote Setup"):
            self.remote_setup()

    def glo_logac(self):
        global remote
        remote = False

    def execute_command(self, command):
        with st.spinner(f"Executing command: {remote=} {command}"):
            if remote:
                try:
                    ssh_client = paramiko.SSHClient()
                    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh_client.connect(hostname=ip, username=username, password=password)
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(command)
                    output = ssh_stdout.read().decode().strip()
                    error = ssh_stderr.read().decode().strip()
                    if error:
                        raise Exception(error)
                    return output
                except Exception as e:
                    return str(e)
            else:
                try:
                    result = subprocess.run(command, shell=True, check=True, capture_output=True)
                    output = result.stdout.decode().strip()
                    return output
                except subprocess.CalledProcessError as e:
                    return f"Fehler: {e.stderr.decode().strip()}"

    def get_toolbox_version(self):
        global py
        command = f'python{py} -c "import toolboxv2; print(toolboxv2.__version__)"'
        v = self.execute_command(command)
        if "not found" in v.lower() or "nicht gefunden" in v.lower():
            v = "404"
        return v.split('\n')[-1]

    def get_python_version(self):
        global py
        command = f"python{py} --version"
        res = self.execute_command(command)
        if "not found" in res.lower() or "nicht gefunden" in res.lower():
            py = "3"
            command = f"python{py} --version"
            res = self.execute_command(command)
        if "not found" in res.lower() or "nicht gefunden" in res.lower():
            py = "3"
            res = "404"
        return res

    def install_toolbox(self):
        output = self.execute_command(f"python{py} -m pip install ToolboxV2")
        st.write(output)

    def update_toolbox(self):
        output = self.execute_command(f"python{py} -m pip install --upgrade ToolboxV2")
        st.write(output)

    def uninstall_toolbox(self):
        output = self.execute_command(f"python{py} -m pip uninstall -y ToolboxV2")
        st.write(output)

    def install_python_3_11(self):
        output = self.execute_command("apt-get install python3.11")
        st.write(output)

    def remote_setup(self):
        global username, password, ip
        st.write("Benutzername:")
        username = st.text_input("Benutzername:")
        st.write("IP-Adresse:")
        ip = st.text_input("IP-Adresse:")
        st.write("Passwort:")
        password = st.text_input("Passwort:", type="password")
        if st.button("Verbinden"):
            self.connect_remote()

    def connect_remote(self):
        global remote
        if username and ip and password:
            remote = True

            st.write("Verbunden.")
            python_version = self.get_python_version()
            toolbox_version = self.get_toolbox_version()
            self.root.write(f"RM Toolbox Version: {toolbox_version}")
            if python_version:
                self.root.write(f"RM Python-Version: {python_version}")
            else:
                if st.button("RM Python 3.11 installieren"):
                    self.install_python_3_11()
            if st.button("Installieren RM"):
                self.install_toolbox()
            if st.button("Aktualisieren RM"):
                self.update_toolbox()
            if st.button("Deinstallieren RM"):
                self.uninstall_toolbox()

            if st.button("Local Setup"):
                self.glo_logac()
        else:
            st.write("Bitte alle Felder ausfüllen.")

    def refresh_ui(self):
        st.empty()

remote = False
ip = None
py = ""

username = None
ip = None
password = None

app = Installer()
