---
status: testing
---

GPU Exercise 1.2: Running a GPU job
===================================

When moving the job to be run on a GPU, all we have to do is update two lines
in the submit file: set `request_gpus` to `1` and specify a GPU enabled
container image for `+SingularityImage`. The updated submit file can be found
in `gpu-job.submit` with the contents:


    universe = vanilla

    # Job requirements - ensure we are running on a Singularity enabled
    # node and have enough resources to execute our code
    # Tensorflow also requires AVX instruction set and a newer host kernel
    Requirements = HAS_SINGULARITY == True && HAS_AVX2 == True && OSG_HOST_KERNEL_VERSION >= 31000
    request_cpus = 1
    request_gpus = 1
    request_memory = 1 GB
    request_disk = 1 GB

    # Container image to run the job in
    +SingularityImage = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/tensorflow-gpu:2.3"

    # Executable is the program your job will run It's often useful
    # to create a shell script to "wrap" your actual work.
    Executable = job-wrapper.sh
    Arguments =

    # Inputs/outputs - in this case we just need our python code.
    # If you leave out transfer_output_files, all generated files comes back
    transfer_input_files = test.py
    #transfer_output_files =

    # Error and output are the error and output channels from your job
    # that HTCondor returns from the remote host.
    Error = $(Cluster).$(Process).error
    Output = $(Cluster).$(Process).output

    # The LOG file is where HTCondor places information about your
    # job's status, success, and resource consumption.
    Log = $(Cluster).log

    # Send the job to Held state on failure.
    #on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)

    # Periodically retry the jobs every 1 hour, up to a maximum of 5 retries.
    #periodic_release =  (NumJobStarts < 5) && ((CurrentTime - EnteredCurrentStatus) > 60*60)

    # queue is the "start button" - it launches any jobs that have been
    # specified thus far.
    queue 1


Submit a job with `condor_submit gpu-job.submit`. Once the job is complete, check
the `.out` file for a line stating the code was run under a GPU. Something similar
to:


    2021-02-02 23:25:19.022467: I tensorflow/core/common_runtime/eager/execute.cc:611] Executing op MatMul in device /job:localhost/replica:0/task:0/device:GPU:0


The `GPU:0` parts shows that a GPU was found and used for the computation.



