# -*- coding: utf-8 -*-
from . import helpers
import subprocess
import uuid


class RCClient:
    def __init__(self, rc_binary_path, instance_name: str = "RC1") -> None:
        if instance_name:
            self.id = instance_name.replace(" ", "_")
        else:
            self.id = str(uuid.uuid1())
        self.rc_binary_path = rc_binary_path
        print("launching named instance " + instance_name)
        if not self.check_for_instance:
            self.launch_named_instance(instance_name)

    def execute_rc_commands(self, commands):
        prepared_commands = []
        for idx, com in enumerate(commands):
            command = "-" + com [0]
            value = com [1]
            prepared_commands.append(command)
            prepared_commands.append(value)

        prepared_commands.insert(0, self.rc_binary_path)
        return subprocess.Popen(prepared_commands, stdout = subprocess.PIPE, universal_newlines = True)
        # return subprocess.run(commands)

    def execute_delegate_commands(self, commands):
        commands.insert(0, ("waitCompleted", self.id))
        commands.insert(0, ("delegateTo", self.id))
        self.execute_rc_commands(commands)

    def check_for_instance(self):
        self.execute_rc_commands(["getStatus", self.id])

    def launch_named_instance(self, instance_name):
        command = ("setInstanceName", self.id)
        self.execute_rc_commands([command])

    def add_image(self, image_path):
        add_image_command = ("add", image_path)
        self.execute_delegate_commands([add_image_command])

    def begin_draft_alignment(self):
        begin_alignment_command = ("draft", "")
        self.execute_delegate_commands([begin_alignment_command])
