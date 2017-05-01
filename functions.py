from standardized import *
import nltk
import rdflib
g = rdflib.Graph()
g.load("./newtotal.ttl",format="turtle")


courses=set([])
for row in g.query(
            'select ?x where { ?s a foaf:Course . ?s foo:courseName ?x}'
            ):
        courses = courses.union(set(dic[str(row.x)]))

students=set([])
for row in g.query(
            'select ?x where { ?s a foaf:Student . ?s foaf:givenName ?x}'
            ):
        students = students.union([str(row.x).lower()])

faculties=set([])
for row in g.query(
            'select ?x where { ?s a foaf:Faculty . ?s foaf:givenName ?x}'
            ):
        faculties = faculties.union([str(row.x).lower()])

var=['a','b','c','d','e','f','g','h','i','j','k']
sol = 'x'

def getID(name,type,variable):
    return "?"+variable+ " " + type + " " + '"' + name + '"' + " . "  

def allEntities(entity,variable): #like all students/all Registrations etc
    return "?" + variable + " a foaf:" + entity + " . "

def cond(variable1,type,variable2):
    return "?" + variable1 + " " + type + " ?" + variable2 + " . " 

def idtosolution(variable1,soltype,variable2):
    return "?" + variable1 + " " + soltype + " ?" + variable2 + " . "

def getNer(query):
    try:
        query = nltk.word_tokenize(query.lower())
    except:
        nltk.download('punkt')
        query = nltk.word_tokenize(query.lower())
    a = {'Student':[],'Faculty':[],'Course':[],'attributes':[]}
    m = (faculties)
    x=[1 for x in query if x in fac_words] #x to distinguish between student and faculty 
    f = m.union(students)
    k = f.union(courses)
    for i in k:
        if i in query:
            if i in courses:
                for key in dic:
                    if i in dic[key]:
                        a['Course'].append(key.title())
            if i in students:
                if x==[]:
                    a['Student'].append(i.title())
            if i in faculties:
                if x==[1]:
                    a['Faculty'].append(i.title())

    for key in attributes:
        for m in attributes[key]:
            if m.split(":")[1] in query:
                a['attributes'].append(m)
            if m.split(":")[1] in dic.keys():
                for word in dic[m.split(":")[1]]:
                    if word in query:
                        a['attributes'].append(m)
    return a
def getFaculty(ner):       #Faculty of Course
    for course in ner['Course']:
        rdfquery=''
        rdfquery=rdfquery+getID(course,"foo:courseName",var[0])
        rdfquery=rdfquery+idtosolution(var[0],"foo:faculty",var[1])
        rdfquery=rdfquery+allEntities("Faculty",var[1])
        rdfquery=rdfquery+idtosolution(var[1],"foaf:givenName",sol)
        rdfquery=rdfquery+idtosolution(var[1],"foaf:familyName",'y')
        finalquery='select ?x ?y where { ' + rdfquery + " }"
        st="Faculty of "+ course+ ": "
        a=[]
        for row in g.query(finalquery):
            a.append(row.x+" "+row.y)
        a=",".join(a)
        return st+a
def getEmail_Student(ner):  #Email of student
    emails=[]
    for student in ner['Student']:
        if 'foo:email' in ner['attributes']:
            rdfquery=''
            rdfquery=rdfquery+getID(student,"foaf:givenName",var[0])
            rdfquery=rdfquery+idtosolution(var[0],"foo:email",sol)
            finalquery='select ?x where { ' + rdfquery + " }"
            for row in g.query(finalquery):
                emails.append("Email of "+student+" : "+row.x)
    return emails
def getrollno_Student(ner):
    rollnos=[]
    for student in ner['Student']:
        if 'rdf:rollno' in ner['attributes']:
            rdfquery=''
            rdfquery=rdfquery+getID(student,"foaf:givenName",var[0])
            rdfquery=rdfquery+idtosolution(var[0],"rdf:rollno",sol)
            finalquery='select ?x where { ' + rdfquery + " }"
            for row in g.query(finalquery):
                rollnos.append("Roll Number of "+student+" : "+row.x)
    return rollnos


def get_coursesby(ner): #All courses taught by faculty
    faculty_courses={}
    for faculty in ner['Faculty']:
        rdfquery=''
        rdfquery=rdfquery+getID(faculty,"foaf:givenName",var[0])
        rdfquery=rdfquery+idtosolution(var[1],"foo:faculty",var[0])
        rdfquery=rdfquery+idtosolution(var[1],"foo:courseName",sol)
        finalquery='select ?x ?y where { ' + rdfquery + " }"
        courses=[]
        for row in g.query(finalquery):
            courses.append(row.x)
        faculty_courses[faculty]=courses
    return faculty_courses

if __name__=="__main__":
    nl_query = input("Enter the query: ")
    print("Standardization:")
    ner = getNer(nl_query.lower())    
    print(ner)
    functions = []
    for i in ner['attributes']:
        if ':' in i:
            for key in attributes:
                if i in attributes[key]:
                    functions = attributes[key][:]
    # #Get Faculty of course
    # faculty=getFaculty(ner)
    # print(faculty)
    #The email of student 
    emails=getEmail_Student(ner)
    print('\n'.join(emails))
    rollnos=getrollno_Student(ner)
    print(rollnos)
    print('\n'.join(rollnos))
    fac_courses=get_coursesby(ner)
    for fac in fac_courses.keys():
        print("Courses taught by "+fac+'\n'+' , '.join(fac_courses[fac]))


    #tokens = nltk.pos_tag(nltk.word_tokenize(nl_query.lower()))

"""
#marks of Students in Courses
for student in ner['Student']:
    for course in ner['Course']:
        rdfquery=''
        rdfquery=rdfquery + getID(student,"foaf:givenName",var[0])
        rdfquery=rdfquery + getID(course,"foo:courseName",var[1])
        rdfquery=rdfquery + allEntities("Registration",var[2])
        rdfquery=rdfquery + cond(var[2],"foo:courseid",var[1])
        rdfquery=rdfquery + cond(var[2],"foo:studentid",var[0])
        rdfquery=rdfquery + idtosolution(var[2],ner["attributes"][0],sol)


        finalquery='select ?x where { ' + rdfquery + " }"
        print("Query: ", student,' in the course ',course)
        rows = g.query(finalquery)
        if len(rows)<=0:
            print('Marks not Available')

        for row in rows:
            print(row.x)


#All courses of Student

for student in ner['Student']:
    rdfquery=''
    rdfquery=rdfquery + getID(student,"foaf:givenName",var[0])
    rdfquery=rdfquery + allEntities("Course",var[1])
    rdfquery=rdfquery + allEntities("Registration",var[2])
    rdfquery=rdfquery + cond(var[2],"foo:courseid",var[1])
    rdfquery=rdfquery + cond(var[2],"foo:studentid",var[0])
    rdfquery=rdfquery + idtosolution(var[1],"foo:courseName",sol)


    finalquery='select ?x where { ' + rdfquery + " }"
    for row in g.query(finalquery):
        print(row.x)
"""

#
#
#
#


#
