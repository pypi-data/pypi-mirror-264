#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
import subprocess
import getpass
from bigdl.dllib.utils.utils import get_node_ip
from bigdl.dllib.utils.log4Error import *


# Assumption:
# 1. All hosts has oneCCL installed
# 2. The driver can ssh all hosts without password
# 3. All hosts have the same working directory.
# 4. All hosts have the same Python environment in the same location.
class MPIRunner:
    def __init__(self,
                 hosts=None,
                 processes_per_node=1,
                 env=None):
        driver_ip = get_node_ip()
        if hosts is None:  # Single node
            self.hosts = [driver_ip]
        elif hosts == "all":  # All executor nodes in the cluster
            def get_ip(iter):
                yield get_node_ip()

            from bigdl.dllib.utils.common import get_node_and_core_number
            from bigdl.orca import OrcaContext
            sc = OrcaContext.get_spark_context()
            node_num, core_num = get_node_and_core_number()
            total_cores = node_num * core_num
            self.hosts = list(set(sc.range(0, total_cores, numSlices=total_cores).barrier()
                                  .mapPartitions(get_ip).collect()))
        else:  # User specified hosts, assumed to be non-duplicate
            invalidInputError(isinstance(hosts, list), "expect hosts to be list")
            self.hosts = hosts

        self.master = self.hosts[0]
        print("Master: ", self.master)
        self.remote_hosts = []
        for host in self.hosts:
            if host != driver_ip:
                self.remote_hosts.append(host)
        print("Remote hosts: ", self.remote_hosts)
        print("Hosts: ", self.hosts)
        invalidInputError(processes_per_node > 0, "processes_per_node must be greater than 0")
        self.processes_per_node = processes_per_node
        self.env = env if env else {}
        self.user = getpass.getuser()

    def run(self, file, mpi_options=None, **kwargs):
        file_path = os.path.abspath(file)
        invalidInputError(os.path.exists(file_path), "file_path doesn't exist")
        file_dir = "/".join(file_path.split("/")[:-1])
        self.scp_file(file_path, file_dir)

        # cmd = ["mpiexec.openmpi"]
        cmd = ["mpiexec.hydra"]
        # -l would label the output with process rank. -l/-ppn not available for openmpi.
        # mpi_config = "-np {} ".format(
        mpi_config = ["-np", self.processes_per_node * len(self.hosts),
                      "-ppn", self.processes_per_node, "-l"]
        mpi_env = os.environ.copy()
        mpi_env.update(self.env)
        if "I_MPI_PIN_DOMAIN" in mpi_env:
            invalidInputError(mpi_env["I_MPI_PIN_DOMAIN"] in ['numa', 'core', 'node'],
                              "I_MPI_PIN_DOMAIN must be one of 'numa', 'core', 'node'")
            mpi_config.extend(["-genv", "I_MPI_PIN_DOMAIN={}".format(mpi_env["I_MPI_PIN_DOMAIN"])])
        if "OMP_NUM_THREADS" in mpi_env:
            invalidInputError(str.isdigit(mpi_env["OMP_NUM_THREADS"]),
                              "OMP_NUM_THREADS must be a positive integer")
            mpi_config.extend(["-genv", "OMP_NUM_THREADS={}".format(mpi_env["OMP_NUM_THREADS"])])
        if len(self.remote_hosts) > 0:
            mpi_config.extend(["-hosts", ",".join(self.hosts)])
        if mpi_options:
            mpi_config += mpi_options
        cmd.extend(mpi_config.split())
        # cmd.append("ls")
        cmd.append(sys.executable)
        cmd.append("-u")  # This can print as the program runs
        cmd.append(file_path)
        for k, v in kwargs.items():
            cmd.append("--{}={}".format(str(k), str(v)))
        print(cmd)

        if len(self.remote_hosts) > 0:
            mpi_env["MASTER_ADDR"] = str(self.master)
        else:  # Single node
            mpi_env["MASTER_ADDR"] = "127.0.0.1"
        # print(mpi_env)
        process = subprocess.Popen(cmd, env=mpi_env)
        process.wait()

    def scp_file(self, file, remote_dir):
        for host in self.remote_hosts:
            p = subprocess.Popen(["scp", file,
                                  "{}@{}:{}/".format(self.user, host, remote_dir)])
            os.waitpid(p.pid, 0)

    def launch_plasma(self, object_store_memory="2g"):
        import atexit
        atexit.register(self.shutdown_plasma)
        # TODO: Or can use spark to launch plasma
        from bigdl.orca.ray.utils import resource_to_bytes
        self.plasma_path = "/".join(sys.executable.split("/")[:-1] + ["plasma_store"])
        self.object_store_memory = resource_to_bytes(object_store_memory)
        self.object_store_address = "/tmp/bigdl_plasma"
        command = "{} -m {} -s {}".format(
            self.plasma_path, self.object_store_memory, self.object_store_address)
        for host in self.hosts:
            if host != get_node_ip():
                p = subprocess.Popen(["ssh", "root@{}".format(host), command])
            else:
                p = subprocess.Popen(command.split())
            print("Plasma launched on {}".format(host))
        return self.object_store_address

    def shutdown_plasma(self):
        for host in self.hosts:
            if host != get_node_ip():
                p = subprocess.Popen(["ssh", "root@{}".format(host), "pkill plasma"])
            else:
                p = subprocess.Popen(["pkill", "plasma"])
            os.waitpid(p.pid, 0)
