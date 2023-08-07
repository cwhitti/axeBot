from class_lookup import *

input_course_code = input("Look up class: ")
class_dict = get_class_dict(input_course_code)

if class_dict:
    for course_id, course_data in class_dict.items():
        # Print the extracted information
        #print()

        course_name = course_data[0]
        course_description = course_data[1]
        course_units = course_data[2]
        course_prerequisites = course_data[3]

        print("Course ID:", course_id)
        print("Course Name:",course_name)
        print("Course Description:", course_description)
        print("Course Units:", course_units)
        print("Course Prerequisites:",course_prerequisites)

        print()
        print('=' * 10)
        print()
else:
    print("No course exists")
