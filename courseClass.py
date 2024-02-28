class Course:

    def __init__(self, name, desc, units, desig, semesters,
                        course_id, term, url, prereqs, offered):
        self.name = name
        self.desc = desc
        self.units = units
        self.desig = desig
        self.semesters = semesters
        self.id = course_id
        self.term = term
        self.url = url
        self.prereqs = prereqs
        self.offered = offered
        self.total = None
        self.A = None
        self.B = None
        self.C = None
        self.D = None
        self.F = None
        self.AU = None
        self.P = None
        self.NG = None
        self.W = None
        self.I = None
        self.IP = None
        self.Pen = None

    def update_grades( self, A, B, C, D, F, AU, P, NG, W, I, IP, Pen, total ):

        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.F = F
        self.AU = AU
        self.P = P
        self.NG = NG
        self.W = W
        self.I = I
        self.IP = IP
        self.Pen = Pen
        self.total = total
