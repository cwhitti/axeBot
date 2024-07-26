import random 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 
from classes.CourseClass import Course


def create_figure(name, courses:list):

    # Check for empty courses list
    if not courses:
        raise ValueError("Courses list is empty.")

    # Initialize variables
    n = len(courses)

    print(n)

    # Calculate number of rows and columns for subplots
    cols = 5
    rows = max(1, (n + cols - 1) // cols)  # Ensure at least one row

    max_fig_width = 10
    max_fig_height = 5.5 * rows

    # Create subplots
    fig, axes = plt.subplots(rows, cols, figsize=(max_fig_width, max_fig_height))

    # Flatten axes array for easy iteration
    axes = axes.flatten()

    # Plotting each dataset
    for i, course in enumerate(courses):

        pf = course.grades.get("P")  # Use get() to avoid KeyError

        if pf is not None:

            labels = ["A", "B", "C", "D", "F"]
            colors = ["#15C259", "#BEF774", "#FCFC7A", "#FF835B", "#FF3636"]

            grades = f'''
            Grades
            A: {course.grades.get("A", 0)}   B: {course.grades.get("B", 0)}
            C: {course.grades.get("C", 0)}   D: {course.grades.get("D", 0)}
            F: {course.grades.get("F", 0)}
            '''
            print("This class is not P/f")
        else:

            labels = ["P", "F"]
            colors = ["#15C259", "#FF3636"]

            grades = f'''
            Grades
            Pass: {course.grades.get("P", 0)}
            Fail: {course.grades.get("F", 0)}
            '''
            print("This class IS P/F")

        # init size list
        sizes = [course.grades.get(label, 0) for label in labels]

        print(sizes)

        # create pie chart
        inst = f"{course.prof}"
        axes[i].pie(sizes, colors=colors, autopct='%1.1f%%', startangle=140)
        axes[i].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        axes[i].set_title(f'Section {course.section}', pad=20)
        axes[i].text(-1, 1.5, inst, ha='left', fontsize=10)
        axes[i].text(-1, -2.5, grades, ha='left', fontsize=10)

    # Remove any empty subplots if the number of datasets is not even
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Save the figure as a JPG file
    plt.savefig(name, format='jpg')

    print("Success?")
