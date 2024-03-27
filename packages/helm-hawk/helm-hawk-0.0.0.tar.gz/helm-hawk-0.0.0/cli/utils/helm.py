import subprocess
import difflib
from .kubectl import Kubectl
import os
import re
from colorama import Fore,Style
class Helm():
    def __init__(self,context,namespace) -> None:
        self.context=context
        self.namespace=namespace
        pass
    


    def extend_context_and_namespace(self,command:list)-> list:
            if self.context: 
                command.extend([ "--kube-context" ,self.context])
            if  self.namespace: 
                command.extend(["--namespace" ,self.namespace])
            return command

    def get_values(self,**kwargs):
        try:
            release_name=kwargs.get("release_name")
            revision=kwargs.get("revision")
            if not revision:
                values_command = ["helm", "get" ,"values",release_name]
            else:
                values_command = ["helm" ,"get" ,"values", release_name,"--revision" ,revision]
            values_command = self.extend_context_and_namespace(command=values_command)
            values_command_output=subprocess.run(values_command, capture_output=True, text=True,check=True)
            return values_command_output.stdout
        except subprocess.CalledProcessError as e:
            print(e.stderr)

    def parse_values_command(self,values)-> list:
        try:
            value_files=[]
            for v in values:
                value_files.append('--values')
                value_files.append(v)
            return value_files
        except Exception as e:
            print("Error while  parsing values file command : ",e)
            raise(e)

    def history(self,release_name,max)->list:
        try:
            if max:
                helm_history_command=["helm","history",release_name,"--max",str(max)]
            else:
                helm_history_command=['helm','history',release_name]
            helm_history_command=self.extend_context_and_namespace(helm_history_command)
            output=subprocess.run(helm_history_command,capture_output=True,check=True)
            return output.stdout
        except subprocess.CalledProcessError as e:
            print(e.stderr)

    def set_env_from_context(self)-> str:
        try:
            kubectl=Kubectl(namespace=self.namespace,context=self.context)
            context=kubectl.get_current_kubecontext()
            prod_pattern = r"aks-dp-(ci|un)-p\d+"
            dev_pattern = r"aks-dp-(ci|un)-d\d+"
            branch="None"
            if re.match(prod_pattern,context):
                branch="master"
            elif re.match(dev_pattern,context):
                branch="develop"
            else:
                branch="None"
            return branch
        except Exception as e:
            print("Exception:-> ",e)

    def validate_chart(self,chart_path)->bool:
        try:
            HELM_BRANCH=self.set_env_from_context()
            original_dir = os.getcwd()
            os.chdir(chart_path)
            subprocess.run(["git", "fetch", "origin", "--tags"], check=True,capture_output=True)
            output=subprocess.run(["git", "checkout", HELM_BRANCH],capture_output=True ,check=True)
            print(output.stdout.decode("utf-8"))
            subprocess.run(["git", "pull", "origin", HELM_BRANCH], check=True,capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            return e.stderr
        finally:
            os.chdir(original_dir)


    def helm_template(self,release_name, chart_path,values)->list:
        '''This converts your  helm values into a k8s manifest files.'''
        try:
            value_files=self.parse_values_command(values)
            helm_template_command = ['helm', 'template', release_name, chart_path, *value_files]
            helm_template_command=self.extend_context_and_namespace(helm_template_command)
            helm_template_output = subprocess.run(helm_template_command, capture_output=True, text=True, check=True)
            return helm_template_output.stdout
        except subprocess.CalledProcessError as e:
            print(e.stderr)
    
    def diff(self,release_name,chart_path,values)->str:
        '''This outputs your diff using kubectl'''
        try:

            kubectl=Kubectl(context=self.context,namespace=self.namespace)
            template=self.helm_template(release_name,chart_path,values)
            return kubectl.diff(template)
        except subprocess.CalledProcessError as e:
            print(e.stderr)

    def diff_revison(self,release_name:str,old_revision:str,new_revision:str)->str:
        '''Outputs diff between value files of two revisions'''
        try:
            old_revision_values=self.get_values(release_name=release_name,revision=old_revision)
            new_revision_values=self.get_values(release_name=release_name,revision=new_revision)
            if old_revision_values is None:
                raise ValueError(f"Revision {old_revision} does not exist")
            elif new_revision_values is None:
                raise ValueError(f"Revision {new_revision} does not exist")

            differ = difflib.Differ()
            diff = list(differ.compare(old_revision_values.splitlines(), new_revision_values.splitlines()))
            added_color=Fore.GREEN
            removed_color=Fore.RED
            for line in diff:
                if line.startswith('+'):
                    print(added_color + line.strip() + Style.RESET_ALL, end='\n')
                elif line.startswith('-'):
                    print(removed_color + line.strip() + Style.RESET_ALL, end='\n')
                elif line.startswith('?'):
                    print(line.strip())
                else:
                    print(line.strip())
               
            # return '\n'.join(diff)
        except Exception as e:
            ''''''
            print(e)
    
    def status(self,release_name,show_desc,revision,output)->str:
        try:
            helm_status_command=['helm','status',release_name]
            if show_desc:
                helm_status_command.extend(['--show-desc'])
            if revision:
                helm_status_command.extend(["--revision",revision])
            if  output in ('json','yaml'):
                helm_status_command.extend(['-o',output])
            helm_status_command=self.extend_context_and_namespace(helm_status_command)
            helm_status_command_output=subprocess.run(helm_status_command, capture_output=True, check=True,text=True)
            return helm_status_command_output.stdout
        except  subprocess.CalledProcessError as e:
            print(e.stderr)
    
    def rollback(self,release_name,revision,dry_run,no_hooks) -> str:
        try:
            helm_rollback_command=['helm','rollback',release_name,revision]
            if  dry_run:
                helm_rollback_command.append('--dry-run')
            if no_hooks:
                helm_rollback_command.append('--no-hooks')
            helm_rollback_command=self.extend_context_and_namespace(helm_rollback_command)
            helm_rollback_command_output=subprocess.run(helm_rollback_command,capture_output=True,text=True,check=True)
            return helm_rollback_command_output.stdout
        except subprocess.CalledProcessError as e:
            print(e.stderr)

    def upgrade(self,release_name,chart_path,values,dry_run) -> str:
        try:
            values=self.parse_values_command(values)
            helm_upgrade_command=[
                'helm',
                'upgrade',
                '-i',
                release_name,
                chart_path,
                *values
            ]
            if  dry_run:
                helm_upgrade_command.append('--dry-run')
            helm_upgrade_command=self.extend_context_and_namespace(helm_upgrade_command)
            helm_upgrade_output=subprocess.run(
                    helm_upgrade_command,
                    capture_output=True,
                    text=True,
                    check=True
            )
            return helm_upgrade_output.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr
    
    def uninstall(self,release_name,dry_run) -> str:
        try:
            helm_uninstall_command=[
                'helm',
                'uninstall',
                release_name
            ]
            if  dry_run:
                helm_uninstall_command.append('--dry-run')
            helm_uninstall_command=self.extend_context_and_namespace(helm_uninstall_command)
            helm_uninstall = subprocess.run(
                helm_uninstall_command,
                    capture_output=True,
                    text=True,
                    check=True
            )
            return helm_uninstall.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr               