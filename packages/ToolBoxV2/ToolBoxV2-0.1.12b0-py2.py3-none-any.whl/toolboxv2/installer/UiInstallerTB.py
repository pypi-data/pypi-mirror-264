import customtkinter as ctk
import subprocess
import sys
import paramiko

remote = False
ip = None
py = ""

username = None
ip = None
password = None


class ToolboxInstallerApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Toolbox Installer")
        self.root.geometry('275x325')
        self.create_widgets()


    def create_widgets(self):
        # Label für Toolbox-Version
        python_version = self.get_python_version()
        toolbox_version = self.get_toolbox_version()
        self.toolbox_version_label = ctk.CTkLabel(self.root, text=f"Toolbox Version: {toolbox_version}",
                                             font=("Helvetica", 12))
        self.toolbox_version_label.pack(pady=10)

        # Installierte Python-Version oder Button zum Installieren von Python 3.11

        if python_version:
            self.python_version_label = ctk.CTkLabel(self.root, text=f"Python-Version: {python_version}",
                                                font=("Helvetica", 12))
            self.python_version_label.pack()
        else:
            self.install_python_button = ctk.CTkButton(self.root, text="Python 3.11 installieren",
                                                  command=self.install_python_3_11)
            self.install_python_button.pack(pady=5)

        # Install Button
        self.install_button = ctk.CTkButton(self.root, text="Installieren", command=self.install_toolbox)
        self.install_button.pack(pady=5)

        # Update Button
        self.update_button = ctk.CTkButton(self.root, text="Aktualisieren", command=self.update_toolbox)
        self.update_button.pack(pady=5)

        # Uninstall Button
        self.uninstall_button = ctk.CTkButton(self.root, text="Deinstallieren", command=self.uninstall_toolbox)
        self.uninstall_button.pack(pady=5)

        if remote:
            # Go local
            self.remote_setup_button = ctk.CTkButton(self.root, text="Local Setup", command=self.stay_locla)
            self.remote_setup_button.pack(pady=5)
        else:
            # Remote Setup Button
            self.remote_setup_button = ctk.CTkButton(self.root, text="Remote Setup", command=self.remote_setup)
            self.remote_setup_button.pack(pady=5)

    def execute_command(self, command):
        print(f"{remote=}, {command}")
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
        print(py)
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
            py = "3.10"
            command = f"python{py} --version"
            res = self.execute_command(command)
        if "not found" in res.lower() or "nicht gefunden" in res.lower():
            py = "3.11"
            command = f"python{py} --version"
            res = self.execute_command(command)
        if "not found" in res.lower() or "nicht gefunden" in res.lower():
            py = "3"
            res = "404"
        return res

    def install_toolbox(self):
        output = self.execute_command(f"python{py} -m pip install ToolboxV2")
        ctk.CTkLabel(self.root, text=output, font=("Helvetica", 12)).pack()

    def update_toolbox(self):
        output = self.execute_command(f"python{py} -m pip install --upgrade ToolboxV2")
        ctk.CTkLabel(self.root, text=output, font=("Helvetica", 12)).pack()

    def uninstall_toolbox(self):
        output = self.execute_command(f"python{py} -m pip uninstall -y ToolboxV2")
        ctk.CTkLabel(self.root, text=output, font=("Helvetica", 12)).pack()

    def install_python_3_11(self):
        output = self.execute_command("apt-get install python3.11")
        ctk.CTkLabel(self.root, text=output, font=("Helvetica", 12)).pack()

    def remote_setup(self):
        self.refresh_ui()

        username_label = ctk.CTkLabel(self.root, text="Benutzername:")
        username_label.pack()
        self.username_entry = ctk.CTkEntry(self.root)
        self.username_entry.pack()

        ip_label = ctk.CTkLabel(self.root, text="IP-Adresse:")
        ip_label.pack()
        self.ip_entry = ctk.CTkEntry(self.root)
        self.ip_entry.pack()

        password_label = ctk.CTkLabel(self.root, text="Passwort:")
        password_label.pack()
        self.password_entry = ctk.CTkEntry(self.root, show="*")
        self.password_entry.pack()

        connect_button = ctk.CTkButton(self.root, text="Verbinden", command=self.connect_remote)
        connect_button.pack(pady=5)

    def stay_locla(self):
        global remote
        remote = False
        self.refresh_ui()
        self.create_widgets()

    def connect_remote(self):
        global username, ip, password, remote
        username = self.username_entry.get()
        ip = self.ip_entry.get()
        password = self.password_entry.get()

        if username and ip and password:
            remote = True
            self.refresh_ui()
            self.create_widgets()
        else:
            ctk.CTkLabel(self.root, text="Bitte füllen Sie alle Felder aus.")
            connect_button = ctk.CTkButton(self.root, text="Local bleiben", command=self.stay_locla)
            connect_button.pack(pady=5)

    def refresh_ui(self):
        # Löschen und Neuerstellen der Elemente
        for widget in self.root.winfo_children():
            widget.destroy()

    # Weitere Methoden wie zuvor

if __name__ == "__main__":
    root = ctk.CTk()
    app = ToolboxInstallerApp(root)
    root.mainloop()

    remote = False
    ip = None
    py = ""

    username = None
    ip = None
    password = None
