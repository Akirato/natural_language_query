from standardized import *
import nltk.word_tokenize
import rdflib
g = rdflib.Graph()
g.load("./newtotal.ttl",format="turtle")

NER=['Natural Language Processing','Operating Systems PG','Natural Language Applications','Topics in Information Retrieval']

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
    query = nltk.word_tokenize(query.lower())
    a = {'Student':[],'Faculty':[],'Course':[],'attributes':[]}
    m = (faculties)
    f = m.union(students)
    k = f.union(courses)
    for i in k:
        if i in query:
            if i in courses:
                for key in dic:
                    if i in dic[key]:
                        a['Course'].append(key.title())
            if i in students:
                a['Student'].append(i.title())
            if i in faculties:
                a['Faculty'].append(i.title())

    for key in attributes:
        for m in attributes[key]:
            if m.split(":")[1] in query:
                a['attributes'].append(m)
    return a


if __name__=="__main__":
    nl_query = input("Enter the query: ")
    ner = getNer(nl_query)    
    functions = []
    print(ner)
    for i in ner['attributes']:
        if ':' in i:
            for key in attributes:
                if i in attributes[key]:
                    functions = attributes[key][:]

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

