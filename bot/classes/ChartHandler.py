
import shutil
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from config import PIE_CHART_FILE as FILENAME

SEPERATE = 0

# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY

# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY
# I HATE NUMPY

# I HATE NUMPY
# I HATE NUMPY

# dont ask me to explain the numpy code please i will explode
# - claire

class ChartHandler():

    def __init__(self) -> None:
        pass

    def combine_images(self, image_files, output_file):
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

    def create_figure(self, searchInfo, records):

        # initialize variables
        class_dict = {}

        # check if records are pass/fail
        if (records[0].P == '0' ):
            
            type = "PASS/FAIL"
            labels = [ "P", "F"]

        # not pass/fail
        else:
            type = "FULL"
            labels = ['A', 'B', 'C', 'D', 'F']
        
        # Run though all courses
        for course in records:
            
            # add to the dictionary
            if type == "PASS/FAIL":
                class_dict[ f"Sect. {course.section}" ] = [
                                                            int(course.P),
                                                            int(course.F)
                                                            ]
            # add to the dictionary
            else:
                class_dict[ f"Sect. {course.section}" ] = [
                                                            int(course.A),
                                                            int(course.B),
                                                            int(course.C),
                                                            int(course.D),
                                                            int(course.F)
                ]
            #class_dict[ f"Sect. {course.section}" ] = [ int(course.grades[label]) for label in labels ]

        fig, ax = self.survey(class_dict, labels, f"Grade Distribution for {searchInfo.search_code} ({searchInfo.calculate_year_and_season( course.term )}) " )
        fig.savefig( FILENAME )

        return FILENAME

    def survey(self, results, category_names, title=""):
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

        # Base height per bar and minimum figure height
        base_height_per_bar = 0.3
        min_height = 5
        fig_height = max(min_height, len(labels) * base_height_per_bar)

        fig, ax = plt.subplots(figsize=(9.5, fig_height))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        bar_height = 0.8

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

# def survey(results, category_names, title=""):
#     """
#     Parameters
#     ----------
#     results : dict
#         A mapping from question labels to a list of answers per category.
#         It is assumed all lists contain the same number of entries and that
#         it matches the length of *category_names*.
#     category_names : list of str
#         The category labels.
#     """
#     labels = list(results.keys())
#     data = np.array(list(results.values()))
#     data_cum = data.cumsum(axis=1)

#     category_colors = plt.colormaps['RdYlGn'](
#         np.linspace(0.15, 0.85, data.shape[1]))[::-1]

#     fig, ax = plt.subplots(figsize=(9.5, 5))
#     ax.invert_yaxis()
#     ax.xaxis.set_visible(False)
#     ax.set_xlim(0, np.sum(data, axis=1).max())

    
#     bar_height = .8 # Minimum height for the bars
    

#     for i, (colname, color) in enumerate(zip(category_names, category_colors)):
#         widths = data[:, i]
#         starts = data_cum[:, i] - widths
#         rects = ax.barh(labels, widths, left=starts, height=bar_height,
#                         label=colname, color=color)

#         r, g, b, _ = color
#         text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
#         ax.bar_label(rects, label_type='center', color=text_color)

#     ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
#               loc='lower left', fontsize='small')

#     ax.set_title(title, loc='left', pad=28.5)

#     return fig, ax