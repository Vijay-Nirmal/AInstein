from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

def getAllPageUrl():
    """Get the list of all pages
    
    Returns
    -------
    allPageUrl : `list`
        List of all pages
    """

    allPageUrl = []
    allPageUrl.append("https://www.amrita.edu/faculty?field_faculty_department_tid=38&field_faculty_designation_tid=All&field_faculty_campus_tid=All&field_faculty_department_main_tid=All")

    for i in range(1, 27):
        allPageUrl.append("https://www.amrita.edu/faculty?field_faculty_department_tid=38&field_faculty_designation_tid=All&field_faculty_campus_tid=All&field_faculty_department_main_tid=All&page=" + str(i))

    return allPageUrl

def getFacultyLink(allPageUrl):
    """Get the list of faculty links from all the pages
    
    Parameters
    ----------
    allPageUrl : `list`
        List of all pages
    
    Returns
    -------
    facultyLink : `list`
        List of all faculties

    """

    facultyLink = []

    print("Getting the list of faculties ...", end="\r")
    for pageUrl in allPageUrl:
        soup = BeautifulSoup(urlopen(pageUrl), "lxml")
        facultys = soup.find("div", {"class": "view-content"}).findChildren("div" , recursive=False)
        for faculty in facultys:
            facultyLink.append("https://www.amrita.edu" + faculty.find("a", href=True)['href'])

    return facultyLink

def populateFacultyDetailsJSON(facultyLink):
    """Create FacultyDetails.json file with all faculty details
    
    Parameters
    ----------
    facultyLink : `list`
       List of all faculties
    
    """
    jsonData = {}

    for i, faculty in enumerate(facultyLink, 1):
        print("Getting the details of faculty " + str(i) + " in " + str(len(facultyLink)) + " -> Progress {:3.1%}".format(i / len(facultyLink)), end="\r")

        soup = BeautifulSoup(urlopen(faculty), "lxml")

        namePre = str(soup.find("div", {"class": "row page-header"}).find("h1"))
        name = namePre[4:namePre.find("<br")].strip()

        positionsSoup = soup.find("div", {"class": "view-content"}).findChildren("div" , recursive=False)
        positions = []
        for position in positionsSoup:
            positions.append(position.text.strip())

        image = soup.find("div", {"class": "container mainContent"}).find("div", {"class": "container-fluid"}).find("img")["src"]

        emailSoup = soup.find("div", {"class": "field field-name-field-faculty-email field-type-text field-label-hidden"})
        email = "NULL"
        if emailSoup is not None:
            email = emailSoup.text.strip()

        qualificationSoup = soup.find("div", {"class": "field field-name-field-faculty-qualification field-type-taxonomy-term-reference field-label-inline clearfix"})
        qualification = "NULL"
        if qualificationSoup is not None:
            qualification = qualificationSoup.findChildren()[1].text.strip()

        mainContentSoup = soup.find("div", {"class": "field field-name-body field-type-text-with-summary field-label-hidden"})
        
        description = ""
        for tags in mainContentSoup.findChild().findChild().findChildren(recursive=False):
            if tags.name != 'p':
                break
            description += tags.text + ""

        publicationsSoup = mainContentSoup.findChild().findChild().find("div", {"class": ['view', 'view-biblio-views', 'view-id-biblio_views', 'view-display-id-block_1']})
        publications = []
        if publicationsSoup is not None:
            for table in publicationsSoup.findChildren("tbody"):
                for rows in table.findChildren(recursive=False):
                    publications.append(rows.findChildren(recursive=False)[2].text.strip())

        interest = []
        interestSoup = soup.find("div", {"class": "field field-name-field-faculty-research-interest field-type-taxonomy-term-reference field-label-inline clearfix"})
        if interestSoup is not None:
            interest = interestSoup.findChildren(recursive=False)[1].text.split(",")

        jsonData[str(i)] = {"name": name, "Email": email, "positions": positions, "Qualification": qualification, "image": image, "description": description.strip(), "Publications": publications, "Interest": interest}

    with open('KnowledgeEngine/Data/FacultyDetails.json', 'w', encoding='utf-8') as outputfile:
        json.dump(jsonData, outputfile, ensure_ascii=False)

def getFacultyDetails():
    """Main function to create faculty details database
    
    """
    allPageUrl = getAllPageUrl()
    facultyLink = getFacultyLink(allPageUrl)
    populateFacultyDetailsJSON(facultyLink)
    print(",,,,,,.....................,,,,,,,,,, Completed ,,,,,,,,,,.....................,,,,,,")

if __name__ == '__main__':
    getFacultyDetails()