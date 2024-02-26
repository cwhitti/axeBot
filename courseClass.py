class Course:

    def __init__(self, name, desc, units, desig, semesters, course_id, term, url,
                prereqs):

        self.name = name
        self.desc = desc
        self.units = units
        self.desig = desig
        self.semesters = semesters
        self.id = course_id
        self.term = term
        self.url = url
        self.prereqs = prereqs
