from Data import Dataset, download, getrandomfile, NB_FILES
from Geometry import Shape, point
from Algorithms import AggregateFiles, GrahamAlgorithm, TriPixelAlgorithm, ToussaintAlgorithm, RitterAlgorithm, CONCATFILE
from os import walk, path
import numpy as np
import matplotlib.pyplot as plt
from random import randint

def runpipeline(index: int) -> tuple:
    filename = "samples/test-{0}.points".format(index)

    #AggregateFiles((index+1))

    (tripixelSet, tripixeltime) = TriPixelAlgorithm(filename)

    (convexhull, hulltime) = GrahamAlgorithm()

    (minrectangle, rectangletime) = ToussaintAlgorithm(convexhull)

    (boundingcircle, circletime) = RitterAlgorithm()

    return (tripixelSet, tripixeltime, convexhull, hulltime, minrectangle, rectangletime, boundingcircle, circletime)

def computequality(shapearea, hullarea):
    return (shapearea - hullarea) / hullarea

def getrandomnumber(max: int):
    return randint(1, max)

def main():
    nb_iter = NB_FILES
    download()

    samplesdir = "samples/"
    i = 0

    fig = plt.figure()
    efficacity = fig.add_subplot(2, 2, 1)
    time = fig.add_subplot(2, 2, 2)

    plot1 = fig.add_subplot(2,2,3)
    plot1.set_aspect("equal")
    toplot = randint(0, nb_iter)

    toussaintresults = np.empty(nb_iter, dtype=object)
    ritterresults = np.empty(nb_iter, dtype=object) 
    toussainttimes = np.empty(nb_iter, dtype=object)
    rittertimes = np.empty(nb_iter, dtype=object)
    for index in range(0, nb_iter):
        print(index)
        (tripixelSet, tripixeltime, hull, hulltime, rectangle, rectangletime, circle, circletime) = runpipeline(index)

        rectanglearea = rectangle.area()
        hullarea = hull.area()
        circlearea = circle.area()

        tripixeltimetoscale = tripixeltime * (10 ** 4)
        hulltimetoscale = hulltime * (10 ** 4)
        circletimetoscale = circletime * (10 ** 4)

        toussainttime = tripixeltimetoscale + hulltimetoscale + rectangletime
        rittertime = tripixeltimetoscale + circletimetoscale

        toussaintresults[index] = point(index, computequality(rectanglearea, hullarea))
        ritterresults[index] = point(index, computequality(circlearea, hullarea))
        toussainttimes[index] = point(index, toussainttime)
        rittertimes[index] = point(index, rittertime)

        if index == toplot:
            print("ici")
            hull.draw(plot1, "black", "graham")
            rectangle.draw(plot1, "red", "toussaint")
            circle.draw(plot1, "blue", "ritter")


    datasets = (Dataset(toussaintresults), Dataset(ritterresults), Dataset(toussainttimes), Dataset(rittertimes))
    colors = ("red", "blue", "red", "blue")
    labels = ("toussaint", "ritter", "toussaint_times", "ritter_times")
    plots = (efficacity, efficacity, time, time)

    for dataset, color, label, plot in zip(datasets, colors, labels, plots):
        dataset.draw(plot, color, label, withlines=True)

    efficacity.legend(loc=2)
    time.legend(loc=2)

    plt.show()

main()
