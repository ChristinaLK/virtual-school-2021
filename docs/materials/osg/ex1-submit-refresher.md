---
status: testing
---

OSG Exercise 1: Refresher – Submitting Multiple Jobs
=====================================================

The goal of this exercise is to map the physical locations of some worker servers in our local cluster.
To do this, you will write a simple submit file that will queue multiple jobs and then manually collate the results.

Where in the world are my jobs?
-------------------------------

To find the physical location of the computers your jobs our running on, you will use a method called *geolocation*.
Geolocation uses a registry to match a computer’s network address to an approximate latitude and longitude.

### Geolocating several servers

Now, let’s try to remember some basic HTCondor ideas from the HTC exercises:

1.  Log in to `learn.chtc.wisc.edu`
1.  Create and change into a new folder for this exercise, for example `osg-ex1`
1.  Download the geolocation code:

        :::console
        user@learn $ wget http://proxy.chtc.wisc.edu/SQUID/osgschool20/location-wrapper.sh \
                     http://proxy.chtc.wisc.edu/SQUID/osgschool20/wn-geoip.tar.gz

    You will be using `location-wrapper.sh` as your executable and `wn-geoip.tar.gz` as an input file.

1.  Create a submit file that generates **fifty** jobs that run `location-wrapper.sh`, transfers `wn-geoip.tar.gz` as an
    input file, and uses the `$(Process)` macro to write different `output` and `error` files.
    Also, add the following requirement to the submit file (it's not important to know what it does):

        Requirements = (HAS_CVMFS_oasis_opensciencegrid_org =?= TRUE)

    Try to do this step without looking at materials from the earlier exercises.
    But if you are stuck, see [HTC Exercise 2.2](../htcondor/part2-ex2-queue-n.md).

1.  Submit your jobs and wait for the results

### Collating your results

Now that you have your results, it's time to summarize them.
Rather than inspecting each output file individually, you can use the `cat` command to print the results from all of
your output files at once.
If all of your output files have the format `location-#.out` (e.g., `location-10.out`), your command will look something
like this:

``` console
user@learn $ cat location-*.out
```

The `*` is a wildcard so the above cat command runs on all files that start with `location-` and end in `.out`.
Additionally, you can use `cat` in combination with the `sort` and `uniq` commands using "pipes" (`|`) to print only
the unique results:

``` console
user@learn $ cat location-*.out | sort | uniq
```

Mapping your results
--------------------

To visualize the locations of the servers that your jobs ran on, you will be using <http://www.mapcustomizer.com/>.
Copy and paste the collated results into the text box that pops up when clicking on the 'Bulk Entry' button on the
right-hand side.
Where did your jobs run?

Next exercise
-------------

Once completed, move onto the next exercise: [Logging in to the OSG submit server](ex2-login-scp.md)

