
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from classes.CourseClass import Course


def combine_images(image_files, output_file):
    # Open all images and determine their sizes
    images = [Image.open(image_file) for image_file in image_files]
    
    # Assume all images have the same size
    width, height = images[0].size

    # Create a new image with the combined size (stack images vertically)
    combined_image = Image.new('RGB', (width, height * len(images)))

    # Paste each image into the combined image
    for index, image in enumerate(images):
        combined_image.paste(image, (0, index * height))

    # Save the combined image
    combined_image.save(output_file)

def create_figure(name, courses:list):

    profs = {}
    imgs = []

    # check if pass/fail
    if (courses[0].grades["P"] != '0' ):
        
        labels = [ "P", "F"]

    # not pass/fail
    else:
        labels = ['A', 'B', 'C', 'D', 'F']


    # category_names = ['Strongly disagree', 'Disagree',
    #               'Neither agree nor disagree', 'Agree', 'Strongly agree']
    
    for course in courses:

        prof = course.prof

        if prof not in profs:
            profs[ prof ] = []

        profs[ prof ].append( course )

    # seperate graphs by prof
    for prof, courses in profs.items():

        class_dict = {}

        # seperate profs by course
        for course in courses:  

            class_dict[ f"Sect. {course.section}" ] = [ int(course.grades[label]) for label in labels ]

        fig, ax = survey(class_dict, labels, prof )
        filename = f"imgs/{prof}_{course.name}.png"
        fig.savefig(filename)
        imgs.append(filename)

    print(name)
    combine_images( imgs, name )


    # results = {
    #     'Question 1': [10, 15, 17, 32, 26],
    #     'Question 2': [26, 22, 29, 10, 13],
    #     'Question 3': [35, 37, 7, 2, 19],
    #     'Question 4': [32, 11, 9, 15, 33],
    #     'Question 5': [21, 29, 5, 5, 40],
    #     'Question 6': [8, 19, 5, 30, 38]
    # }

    # fig, ax = survey(class_dict, labels)

    # fig.savefig( name, format=name[-3:])

    return True


def create_stacked_figures(figs, filename='combined.png'):
    pass


def survey(results, category_names, title):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)

    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))[::-1]


    fig, ax = plt.subplots(figsize=(9.5, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    min_height = 20  # Minimum height for the bars
    bar_height = min_height / 100.0  # Adjust this to fit your plot's scale

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=bar_height,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)

    ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
            loc='lower left', fontsize='small')
    
    ax.set_title(title, loc='left', pad=28.5)

    return fig, ax