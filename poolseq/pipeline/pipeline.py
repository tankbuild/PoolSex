from collections import defaultdict
from poolseq.parameters import Parser, get_parameters
from poolseq.data import Data, variables
from poolseq.scheduler import Scheduler
from poolseq.modules import create_modules
from poolseq.pipeline import init, clean


class Pipeline():

    def __init__(self, arguments):

        self.parser = Parser(arguments)
        self.data = Data(self.parser.arguments.input_folder)
        self.parameters = get_parameters(self.data)
        self.scheduler = Scheduler(self.parameters[variables.parameters.scheduler], self.data)
        self.modules = create_modules(self.data)
        self.run_commands = {variables.commands.init: self.init,
                             variables.commands.run: self.run,
                             variables.commands.clean: self.clean,
                             variables.commands.restart: self.restart}
        self.run_commands[self.parser.arguments.command]()

    def init(self):
        init.generate_directories(self.data)
        init.generate_settings_file(self.data, self.parameters)

    def run(self):
        self.generate_pipeline_shell_files()
        self.submit_jobs()

    def clean(self, step=variables.modules.index):
        clean.remove_modules_files(self.modules, step=variables.modules.index)

    def restart(self):
        if not self.parser.arguments.step:
            for step, module in self.modules.items():
                success = module.was_successful(self.data)
                if not success:
                    break
        else:
            step = self.parser.arguments.step
        print('Restarting from step: ' + step)
        self.clean(step=step)
        self.generate_pipeline_shell_files(step=step)
        self.submit_jobs(step=step)

    def generate_pipeline_shell_files(self, step=variables.modules.index):
        generate = False
        for name, module in self.modules.items():
            if name == step:
                generate = True
            if generate:
                for instance in module.instances.keys():
                    self.scheduler.write_shell_file(module, instance, self.data, self.parameters)

    def submit_jobs(self, step=variables.modules.index):
        submit = False
        if self.parser.arguments.dry_run:
            return
        hold_ids = defaultdict(lambda: defaultdict(str))
        for name, module in self.modules.items():
            if name == step:
                submit = True
            if submit:
                for instance, instance_data in module.instances.items():
                    job_id = self.scheduler.submit(instance_data, hold_ids=hold_ids[module.data[variables.modules_options.dependencies]])
                    if not job_id:
                        exit(1)
                        pass
                    hold_ids[name][instance_data[variables.instance_options.name]] = job_id
