#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <limits.h>

/*CS 223 - Hana Galijasevic, netid: hg343
 * Pset #2: Psched */

void mySort(int a[], int n);
int lw(int nProc, int tasks[], int numtasks);
int lwd(int nProc, int tasks[], int numtasks);
int bw(int nProc, int tasks[], int numtasks);
int bwd(int nProc, int tasks[], int numtasks);
int opt(int nProc, int tasks[], int numtasks, int currTask, int lower, int upper, int proc[], int prevTask, int procassigned);
int min(int a[], int size);
int max(int a[], int size);
int isoutbounds(char a[]);


int main(int argc, char *argv[])
{
    int numtasks = 0;
    int noflags = 0;
    int nProc = atoi(argv[1]);
    int Lw = -1, Lwd = -1, Bw = -1, Bwd = -1, Opt = -1;

    for (int i = 2; i <= argc; i++)//count tasks
    {
        if (i == argc) // edge case where no flags or non-integer values are given
            noflags = 1;
        else if (argv[i][0] == '-')
            break;

        else if (atoi(argv[i]) > 0 && !isoutbounds(argv[i]) && i != argc && argv[i][0] != '-')
            numtasks++;
    }
///
    int tasks[numtasks], sorted[numtasks]; // create list of tasks
    int counter = 0, ctargs = 2, sumtimes = 0;

    while (counter < numtasks && ctargs < argc)
    {
        if (atoi(argv[ctargs]) > 0 || (argv[ctargs] == 0 && argv[ctargs][0] != '-'))
        {
            tasks[counter] = atoi(argv[ctargs]);
            sorted[counter] = atoi(argv[ctargs]); // create a second list for opt to use and sort later
            sumtimes += tasks[counter];
            counter++;
            ctargs++;
        }
        else
            ctargs++;
    }
///
    if (!noflags) // NOT edge case w/ no flags
    {
        for (int i = numtasks+1; i < argc; i++) // handle flags accordingly
        {
            if (!strcmp(argv[i], "-opt"))
            {
                int lower, upper;
                if (Opt == -1)
                {
                    if (numtasks == 0) // cases of no given tasks
                        printf("-opt %d\n", 0);
                    else
                    {
                        lower = (sumtimes + nProc - 1)/nProc;
                        upper = lwd(nProc, tasks, numtasks);
                        mySort(sorted, numtasks);

                        int procs[nProc];
                        for (int i = 0; i < nProc; i++) //set all processors to 0 workload
                        {
                            procs[i] = 0;
                        }

                        Opt = opt(nProc, sorted, numtasks, 0, lower, upper, procs, 0, 0); //opt function
                        printf("-opt %d\n", Opt);
                    }
                }
                else //these save already calculated value of called flags, to decrease runtime
                {
                    printf("-opt %d\n", Opt);
                }
            }

            if (!strcmp(argv[i], "-lw"))
            {
                if (numtasks == 0)
                    printf("-lw  %d\n", 0);
                else if (Lw == -1)
                {
                    Lw = lw(nProc, tasks, numtasks);
                    printf("-lw  %d\n", Lw);
                }
                else
                    printf("-lw  %d\n", Lw);
            }

            else if (!strcmp(argv[i], "-lwd"))
            {
                if (numtasks == 0)
                    printf("-lwd %d\n", 0);
                else if (Lwd == -1)
                {
                    Lwd = lwd(nProc, tasks, numtasks);
                    printf("-lwd %d\n", Lwd);
                }
                else
                    printf("-lwd %d\n", Lwd);
            }
            else if (!strcmp(argv[i], "-bw"))
            {
                if (numtasks == 0)
                    printf("-bw  %d\n", 0);
                else if (Bw == -1)
                {
                    Bw = bw(nProc, tasks, numtasks);
                    printf("-bw  %d\n", Bw);
                }
                else
                    printf("-bw  %d\n", Bw);
            }
            else if (!strcmp(argv[i], "-bwd"))
            {
                if (numtasks == 0)
                    printf("-bwd %d\n", 0);
                else if (Bwd == -1)
                {
                    Bwd = bwd(nProc, tasks, numtasks);
                    printf("-bwd %d\n", Bwd);
                }
                else
                    printf("-bwd %d\n", Bwd);
            }
        }
    }

    return 0;
}

void mySort(int a[], int n)
{  //implement insertionsort for descending order
    int i, last, j;
    for (i = 1; i < n; i++)
    {
        last = a[i];
        j = i-1;
        while (j >= 0 && a[j] < last)
        {
            a[j+1] = a[j];
            j = j-1;
        }
        a[j+1] = last;
    }
}

int min(int a[], int size)
{
    int min = a[0];
    for (int i = 0; i < size; i++)
    {
        if (a[i] < min)
            min = a[i];
    }
    return min;
}

int max(int a[], int size)
{
    int max = a[0];
    for (int i = 0; i < size; i++)
    {
        if (a[i] > max)
            max = a[i];
    }
    return max;
}

/*  -lw   Use the Least-Workload heuristic:  Assign the tasks (i.e., the
    run-times) in the order in which they appear on the command line; and
    assign each task to a processor that has the least workload at the time
    of the assignment. */

int lw(int nProc, int tasks[], int numtasks)
{
    int procs[nProc];
    for (int i = 0; i < nProc; i++) //set all processors to 0 workload
    {
        procs[i] = 0;
    }
    for (int i = 0; i < numtasks; i++)
    {
        int Min = min(procs, nProc);
        for (int j = 0; j < nProc; j++)
        {
            if (procs[j] == Min)
            {
                procs[j] += tasks[i];
                break;
            }
        }
    }
    return max(procs, nProc);
}

/*           -lwd  Use the Least-Workload-Decreasing heuristic:  First sort the tasks in
    decreasing order of run-time and then assign them in that order using
    the Least-Workload heuristic. */

int lwd(int nProc, int tasks[], int numtasks)
{
    int new[numtasks];
    for (int i = 0; i < numtasks; i++)
    {
        new[i] = tasks[i];
    }
    mySort(new, numtasks);
    return lw(nProc, new, numtasks);
}

/*  -bw   Use the Best-Workload heuristic:  Assign the tasks in the order in
    which their run-times appear on the command line; and assign each task
    to a processor that has the least current workload, unless this
    assignment would NOT increase the maximum current workload, in which
    case assign that task to the busiest processor with this property. */

int bw(int nProc, int tasks[], int numtasks)
{
    int procs[nProc];
    for (int i = 0; i < nProc; i++) //set all processors to 0 workload
    {
        procs[i] = 0;
    }
    for (int i = 0; i < numtasks; i++)
    {
        int procused = min(procs, nProc);
        //int difference = max(procs, nProc) - tasks[i];

        if (tasks[i] > max(procs, nProc) - min(procs, nProc))
        {
            for (int j = 0; j < nProc; j++) //assigns to min of all tasks
            {
                if (procs[j] == procused)
                {
                    procs[j] += tasks[i];
                    break;
                }
            }
        }
        else
        {
            int sorted[nProc];
            for (int j = 0; j < nProc; j++)
            {
                sorted[j] = procs[j];
            }
            mySort(sorted, nProc);

            for (int j = 0; j < nProc; j++)
            {
                if (sorted[j] + tasks[i] <= max(procs, nProc))
                {
                    for (int k = 0; k < nProc; k++)
                    {
                        if (procs[k] == sorted[j])
                        {
                            procs[k] += tasks[i];
                            break;
                        }
                    }
                    break;
                }
            }
        }
    }
    return max(procs, nProc);
}

/*  -bwd  Use the Best-Workload-Decreasing heuristic:  First sort the tasks in
    decreasing order of run-time and then assign them in that order using
    the Best-Workload heuristic. */

int bwd(int nProc, int tasks[], int numtasks)
{
    int new[numtasks];
    for (int i = 0; i < numtasks; i++)
    {
        new[i] = tasks[i];
    }
    mySort(new, numtasks);
    return bw(nProc, new, numtasks);
}

/*    -opt  Use backtracking to find an assignment that minimizes the largest
    workload among the processors. */
int opt(int nProc, int tasks[], int numtasks, int currTask, int lower, int upper, int proc[], int prevTask, int procassigned)
{
    if (upper == lower)  //heuristic B
        return upper;
    else
    {
        int prevproc;
        if (currTask < numtasks)
        {
            if (tasks[currTask] != prevTask)
            {
                for (int i = 0; i < nProc; i++)
                {
                    prevproc = proc[i];

                        proc[i] += tasks[currTask]; ///

                        if (prevproc != proc[i-1]) //heuristic D
                        {
                            if (proc[i] >= upper) //heuristic C
                                proc[i] -= tasks[currTask];

                            else
                            {
                                upper = opt(nProc, tasks, numtasks, currTask+1, lower, upper, proc, tasks[currTask], i); ///
                                proc[i] -= tasks[currTask];
                            }
                        }
                        else
                            proc[i] -= tasks[currTask];
                }
            }
            else
            {
                for (int i = procassigned; i < nProc; i++) //loop equal to one above, except for starting point. easier to understand without extra variable
                {
                    prevproc = proc[i];

                    proc[i] += tasks[currTask]; ///

                    if (prevproc != proc[i-1]) //heuristic D
                    {
                        if (proc[i] >= upper) //heuristic C
                            proc[i] -= tasks[currTask];

                        else
                        {
                            upper = opt(nProc, tasks, numtasks, currTask+1, lower, upper, proc, tasks[currTask], i); ///
                            proc[i] -= tasks[currTask];
                        }
                    }
                    else
                        proc[i] -= tasks[currTask];
                }
            }
            return upper;
        }
        else
        {
            if (max(proc, nProc) < upper)
                return max(proc, nProc);
            else
                return upper;
        }
    }
}


int isoutbounds(char a[]) //credit for idea to stackoverflow; checks if |input value| is greater than INT_MAX
{
    errno = 0;

    long temp = strtol(a, NULL, 10);

    if ((errno == ERANGE) && (temp <= INT_MIN || temp >= INT_MAX))
        return 1;
    else
        return 0;
}
