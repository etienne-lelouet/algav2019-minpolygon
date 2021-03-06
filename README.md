# Objective

Implementation of the AKL-Toussaint and Ritter algorithm (minimum polygons) for [this college project](https://www-apr.lip6.fr/~buixuan/files/algav2019/projet_indiv2.pdf) (Sorbonne university, Master of Computer Science, 2019)

# HOW TO

For a first run on a Linux system : 
- ensure you have python3 and python3-tk (tkinter, to show the matplotlib graph) installed
- run the initialize.sh file
- And then `make` and `python3 src/mainbyaggrer.py` or `python3 src/mainfilebyfile.py` to run the project in aggregation mode (we gradually increase the entry size) or file by file mode (we execute the dataset algorithms on each file).
- If you want to adjust the number of dataset the program is running on, you can do so by editing the nb_files value of the main function in src/main.py

# How to run the C utilities as separate programs : 

The utilities assume a POSIX-compliant system.

The implementation of the pixel cleaning, the Graham quickhull scan, and the Ritter minimum sphere are made in C99.

You need a C compiler, and any implementation of the C standard library (stdio.h, stdlib.h, math.h) :

``` shell
gcc -Wall -O2 tripixel.c -lm -o tripixel
gcc -Wall -O2 graham.c -lm -o graham
gcc -Wall -O2 ritter.c -lm -o ritter
```

These three utilities can only read from standard input, and only write to standard output.

They output the result, plus the time taken for the execution on the last line. To get rid of that last line (for a proper shell piping, for instance), just filter the output through `head -n -1`.

The parser for those three utilities assumes  one point per line (x then y), separated by a space. It won't work if the input doesn't comply.

The tripixel utility only works if the entries with same reference coordinate are adjacent.

The graham utility assumes that the entry with the lowest y coordinate (the leftmost of them if there are several) is the first entry.

The following POSIX shell command should prepare everything correctly :

``` shell
cat $input | sort -S 80% --parallel=8 -n | uniq | /path/to/tripixel | head -n -1 | awk '{print $2, $1}' | sort -S 80% --parallel=8 -n | /path/to/tripixel | awk '{print $2, $1}' > cleandata
```

The -S and --parallel options are not specified by POSIX, so may not be present on your version of sort. They do speed up the process considerably.

The following command should print the convex hull to standard output, one point per line (CW) :

``` shell
cat $cleandata | /path/to/graham "$(wc -l $cleandata | awk '{print $1}')" | head -n -1
```

The following command should print a nearly optimal bounding sphere (x, y and radius, in double precision floating numbers) to the standard output :

``` shell
cat $cleandata | /path/to/ritter "$(wc -l $cleandata | awk '{print $1}')" | head -n -1
```

The results vary if you decide to run it on the full subset of unique cleaned points or only on the convex hull, because of the fondamentally probabilistic nature of the algorithm. Running on the convex hull is valid (by definition of convexity), and slightly better, and also runs quicker.

You will need of course the following unix commands :
- sort (GNU version preferably, remove -S and --parallel option if non-GNU)
- uniq
- awk
- cat
- wc

All these commands are supposed to be installed on a POSIX system.