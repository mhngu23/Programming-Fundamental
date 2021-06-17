# Assignment Final Assessment
# Minh Hoang Nguyen
# s3712611

"""Thank you for reading!
    The highest level that I have attempted in this assignment will be High Distinction
    Overview Reflection:
    The most challenging parts are:
    * Interpreting the Project Brief, specifically the High Distinction GPA and credit_point calculation.
    * Implementing Object Oriented Programming into the program is still very hard. Especially, designing the object,
    attribute, and method. But, I did realise a lot more than when I was working on assignment 2.
    * Still, I could have implement it better if more time is available.
    * Error can occur if there extra (blank) line at the end of the text file or if the blank line does not happen
    at the beginning of the file.
    * I use OSError for file input cannot be found to cover more exceptions. However, it would also cover some
    exceptions that do not need to be cover for file importing.
    """

import sys
from datetime import datetime


class Student:
    """Class Student was used to create student object.
    All attribute were set to private with getter/assessor method to create easier control over the specific attribute.
    ID, name, student_type will be read straight from input file.
    The rest of the attributes would require modify so their value would be assess using getter/assessor."""
    def __init__(self, ID, name, student_type):
        self.__ID = ID
        self.__name = name
        self.__student_type = student_type
        self.__number_of_course_enrol = 0
        self.__number_of_compulsory_course_enrol = 0
        self.__total_credit_point_earn = 0
        self.__credit_point_list_attempt = []
        self.__score = []
        self.__GPA = 0

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def student_type(self):
        return self.__student_type

    @student_type.setter
    def student_type(self, student_type):
        self.__student_type = student_type

    @property
    def number_of_course_enrol(self):
        return self.__number_of_course_enrol

    @number_of_course_enrol.setter
    def number_of_course_enrol(self, number_of_course_enrol):
        self.__number_of_course_enrol = number_of_course_enrol

    @property
    def number_of_compulsory_course_enrol(self):
        return self.__number_of_compulsory_course_enrol

    @number_of_compulsory_course_enrol.setter
    def number_of_compulsory_course_enrol(self, number_of_compulsory_course_enrol):
        self.__number_of_compulsory_course_enrol = number_of_compulsory_course_enrol

    @property
    def credit_point_list_attempt(self):
        return self.__credit_point_list_attempt

    @property
    def score(self):
        return self.__score

    @property
    def GPA(self):
        return self.__GPA

    @GPA.setter
    def GPA(self, GPA):
        self.__GPA = GPA

    @property
    def total_credit_point_earn(self):
        return self.__total_credit_point_earn

    @total_credit_point_earn.setter
    def total_credit_point_earn(self, total_credit_point_earn):
        """total_credit_point_earn will only be calculated if the score met the requirement."""
        self.__total_credit_point_earn += total_credit_point_earn

    def get_enrolment_status(self):
        """This method is used to check whether a student met the requirement for its study type.
        Full time need to attempt 3 compulsory course with credit point of 50.
        while part time required 2 compulsory course with credit point of 30.
        """
        if self.__student_type == 'FT' and self.__number_of_compulsory_course_enrol >= 3 and \
                self.__total_credit_point_earn >= 50:
            enrolment_status = 'Good'
        elif self.__student_type == 'PT' and self.__number_of_compulsory_course_enrol >= 2 and \
                self.__total_credit_point_earn >= 30:
            enrolment_status = 'Good'
        else:
            enrolment_status = 'Bad'
        return enrolment_status

    def GPA_calculation(self):
        """This method is used to calculate the average GPA of a student.
        The method will check the relevant student score and append the appropriate GPA to GPA_list.
        Count is an temporary variable to document the number of courses the student attempt."""
        GPA_list = []
        count = 0
        for score in self.__score:
            if 80 <= int(float(score)) <= 100:
                temp = 4
                count += 1
                GPA_list.append(temp)
            elif 70 <= int(float(score)) <= 79:
                temp = 3
                count += 1
                GPA_list.append(temp)
            elif 60 <= int(float(score)) <= 69:
                temp = 2
                count += 1
                GPA_list.append(temp)
            elif 50 <= int(float(score)) <= 59:
                temp = 1
                count += 1
                GPA_list.append(temp)
            elif int(float(score)) == 888 or int(float(score)) == -1:
                continue
            else:
                count += 1
        product_list = []
        if count > 0:
            for num1, num2 in zip(self.credit_point_list_attempt, GPA_list):
                product_list.append(num1 * num2)
            GPA = sum(product_list)/sum(self.credit_point_list_attempt)
        else:
            GPA = '       --'
        return GPA


class Course:
    """Class Course was used to create student object.
    All attribute were set to private with getter/assessor method to create easier control over the specific attribute.
    ID, name, student_type will be read straight from input file.
    The rest of the attributes would require modify so their value would be assess using getter/assessor."""
    def __init__(self, ID, title, course_type):
        self.__ID = ID
        self.__title = title
        self.__course_type = course_type
        self.__score = []

    @property
    def ID(self):
        return self.__ID

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def course_type(self):
        return self.__course_type

    @course_type.setter
    def course_type(self, course_type):
        """This setter is used to make sure that course type cannot be change between Elective and Compulsory Course
         But compulsory class level can still be changed"""
        if 1 <= len(course_type) <= 2:
            if self.__course_type[0] == 'C' and str(course_type[0]) == 'E':
                print('This is an compulsory course. It cannot be change to an elective course')
                return
            elif self.__course_type[0] == 'E' and str(course_type[0]) == 'C':
                print('This is an elective course. It cannot be change to an compulsory course')
                return
            elif self.__course_type[0] == 'E' and str(course_type[0]) == 'E':
                print('This is an elective course')
                return
            elif self.__course_type[0] == 'C' and str(course_type[0]) == 'C':
                temp = input('Do you want to update this course to the specify course level? [y or n]: ')
                if temp == 'y':
                    if course_type[1] <= 3:
                        self.__course_type = course_type
                    else:
                        print('This is not a valid update!')
                        return
                elif temp == 'n':
                    return
            else:
                print('This is not a valid update!')
                return
        else:
            print('This is not a valid update!')
            return

    @property
    def score(self):
        return self.__score

    def course_average_score(self):
        total = 0
        count = 0
        for score in self.score:
            if 0 <= score <= 100:
                total += score
                count += 1
            else:
                continue
        if count == 0:
            average = '     --'
        else:
            average = int(total / count)
        return average

    def number_of_student_enrol(self):
        """This method is used to count the number of student enrol in a specific course.
        Only score that is equal to -1 will not be included in this count"""
        count_student = 0
        for score in self.score:
            if 0 <= score <= 100 or score == 888:
                count_student += 1
        return count_student


class CompulsoryCourse(Course):
    """Compulsory Course class and Elective Course class inherit from Course class"""
    def __init__(self, ID, title, course_type, credit_point):
        super().__init__(ID, title, course_type)
        self.__credit_point = credit_point

    @property
    def credit_point(self):
        return self.__credit_point

    @credit_point.setter
    def credit_point(self, credit_point):
        self.__credit_point = credit_point


class ElectiveCourse(Course):
    """Compulsory Course class and Elective Course class inherit from Course class"""
    def __init__(self, ID, title, course_type, credit_point=6):
        """The default score for any Elective Course is automatically set to 6 by default"""
        super().__init__(ID, title, course_type)
        self.__credit_point = credit_point

    @property
    def credit_point(self):
        return self.__credit_point

    @credit_point.setter
    def credit_point(self, credit_point):
        self.__credit_point = credit_point


class School:
    """Class School is the main class that control the operation of this program.
    It is used mainly to read from input and write to output file and window"""
    def __init__(self):
        self.score_data_from_source = []
        self.course_data_from_source = []
        self.student_data_from_source = []
        self.student_list = []
        self.course_list = []
        self.score_list = []

    def read_score_file(self, file_name):
        """read_score_file method is used to read the data from score file.
        If the file path cannot be located the program will exit
        If the input file is empty (new school scenario) the program will still take input from course and student file.
        But there will be no score analyse."""
        try:
            score_file = open(file_name, 'r')
            score_file.seek(0, 0)
            new_school_check = score_file.readline()
            if not new_school_check:
                print('This is a new school so the score file are empty. No information will be printed. '
                      '\nYou can still load the other files but they will not have any score data.\n')
                return
            else:
                score_file.seek(0, 0)
                line_from_file = score_file.readline()
                while line_from_file != "":
                    fields_from_line = line_from_file.split()
                    self.score_data_from_source.append(fields_from_line)
                    line_from_file = score_file.readline()
                for i in range(1, len(self.score_data_from_source)):
                    for j in range(1, len(self.score_data_from_source[i])):
                        # All character in the score file will be changed to -1 apart from TBA will be changed to 888.
                        if self.score_data_from_source[i][j] == 'TBA':
                            self.score_data_from_source[i][j] = 888
                        else:
                            try:
                                self.score_data_from_source[i][j] = int(float(self.score_data_from_source[i][j]))
                                # Check if the input is a character or a number.
                            except ValueError:
                                self.score_data_from_source[i][j] = -1
                self.create_student_object_if_only_have_score_file()
                # Create student object if only score file is inputted to use for display in Pass level
                self.create_course_object_if_only_have_score_file()
                # Create course object if only score file is inputted to use for display in Pass level
                score_file.close()
        except OSError:
            print('ERROR: The', file_name, 'file cannot be read')
            print('Program will exit')
            sys.exit()

    def read_course_file(self, file_name):
        """read_course_file method is used to read the data from course file."""
        try:
            course_file = open(file_name, 'r')
            line_from_file = course_file.readline()
            while line_from_file != "":
                fields_from_line = line_from_file.split()
                self.course_data_from_source.append(fields_from_line)
                line_from_file = course_file.readline()
                self.create_course_object_full()
            course_file.close()
        except OSError:
            print('ERROR: The', file_name, 'file cannot be read')
            print('Program will exit')
            sys.exit()

    def read_students_file(self, file_name):
        """read_course_file method is used to read the data from student file."""
        try:
            student_file = open(file_name, 'r')
            line_from_file = student_file.readline()
            while line_from_file != "":
                fields_from_line = line_from_file.split()
                self.student_data_from_source.append(fields_from_line)
                line_from_file = student_file.readline()
                self.create_student_object_full()
            student_file.close()
        except OSError:
            print('ERROR: The', file_name, 'file cannot be read. Only course_report.txt will be generated')
            print('Program will exit')
            sys.exit()

    def create_course_object_if_only_have_score_file(self):
        for i in range(1, len(self.score_data_from_source[0])):
            ID = self.score_data_from_source[0][i]
            # If the course ID is listed in the score file then course object is created using only the course ID.
            course = Course(ID, None, None)
            self.course_list.append(course)

    def create_student_object_if_only_have_score_file(self):
        for i in range(1, len(self.score_data_from_source)):
            score_list_single_student = []
            ID = self.score_data_from_source[i][0]
            # If the student ID is listed in the score file then student object is created using only the student ID.
            student = Student(ID, None, None)
            self.student_list.append(student)
            for j in range(1, len(self.score_data_from_source[i])):
                score = int(float(self.score_data_from_source[i][j]))
                if (100 >= score >= -1) or (score == 888):
                    score_list_single_student.append(score)
                elif (score > 100 or score < -1) and score != 888:
                    print('[ERROR:] Please re-check the imputed <scores filet>\n'
                          'Score cannot be lower than 0 or higher than 100 or unless it is equal to 888 or -1\n'
                          'Score equals to 888 means the score of the student is not available\n'
                          'Score equals to -1 means the student did not enrol in that course')
                    sys.exit()
            self.score_list.append(score_list_single_student)

    def create_course_object_full(self):
        """Method create_course_object_full is called when a course file is provided"""
        self.course_list.clear()
        """This line is to clear out the list of object that was generated using only the score file so as not to mix up 
        with the new object"""
        for i in range(len(self.course_data_from_source)):
            """This block of code is used to classify compulsory and elective course and then create the appropriate
            object for it.
            All compulsory courses start with C in their IDs.
            All elective courses start with E in their IDs."""
            if str(self.course_data_from_source[i][2][0]).strip() == 'C':
                course = CompulsoryCourse(self.course_data_from_source[i][0], self.course_data_from_source[i][1],
                                          self.course_data_from_source[i][2], self.course_data_from_source[i][3])
                for score_list in self.score_list:
                    course.score.append(score_list[i])
                self.course_list.append(course)
            elif str(self.course_data_from_source[i][2][0]).strip() == 'E':
                course = ElectiveCourse(self.course_data_from_source[i][0], self.course_data_from_source[i][1],
                                        self.course_data_from_source[i][2], self.course_data_from_source[i][3])
                for score_list in self.score_list:
                    course.score.append(score_list[i])
                self.course_list.append(course)

    def create_student_object_full(self):
        """Method create_student_object_full is called when a student file is provided"""
        self.student_list.clear()
        """This line is to clear out the list of object that was generated using only the score file so as not to mix up 
                with the new object"""
        for i in self.student_data_from_source:
            student = Student(i[0], i[1], i[2])
            self.student_list.append(student)
        for student in self.student_list:
            for i in self.score_data_from_source:
                if str(student.ID) == str(i[0]):
                    number_of_course_enrol = 0
                    number_of_compulsory_course_enrol = 0
                    for j in range(1, len(i)):
                        student.score.append(i[j])
                        if i[j] != -1:
                            number_of_course_enrol += 1
                            if self.course_list[j - 1].course_type[0] == 'C':
                                # Checking whether the course is a compulsory course using j - 1 index. The index is
                                # j - 1 instead of i because the first index in each score line is the student ID
                                number_of_compulsory_course_enrol += 1
                            else:
                                continue
                        elif i[j] == -1:
                            continue
                    student.number_of_course_enrol = number_of_course_enrol
                    student.number_of_compulsory_course_enrol = number_of_compulsory_course_enrol
        for student in self.student_list:
            for i in range(len(student.score)):
                if student.score[i] != -1 and student.score[i] != 888:
                    student.credit_point_list_attempt.append(int(float(self.course_list[i].credit_point)))
                    if student.score[i] < 50:
                        continue
                    elif student.score[i] >= 50:
                        student.total_credit_point_earn = int(float(self.course_list[i].credit_point))
                else:
                    continue
            student.GPA = student.GPA_calculation()

    def top_student(self):
        """The top_student method is used to look for the student with the highest average
        As an output in the case only score file is available
        Function would return 2 values which are the highest average, and its index to search from the student list
        If score file is empty the value will be replace with Not Available string"""
        average_score_list = []
        for i in range(len(self.score_list)):
            total = 0
            count = 0
            for j in self.score_list[i]:
                if 0 <= j <= 100:
                    total += j
                    count += 1
                else:
                    continue
            if count == 0:
                average_score_list.append(0)
            elif count != 0:
                average_score_list.append(int(float(total) / count))
        if average_score_list:
            highest_average_score = max(average_score_list)
            return highest_average_score, average_score_list.index(highest_average_score)
        else:
            return 'Not Available', 'Not Available'

    def worst_course(self):
        """The worst_course method is used to look for the course with the lowest average score
                Function would return 2 values which are the ID of the course, and the minimum course average
                If score file is empty the value will be replace with Not Available string"""
        course_average_score_dictionary = {}
        for course in self.course_list:
            if course.course_average_score() == '     --':
                continue
            else:
                course_average_score_dictionary.update({course.ID: course.course_average_score()})
        if course_average_score_dictionary != {}:
            worst_course_score = min(course_average_score_dictionary.values())
            for ID, value in course_average_score_dictionary.items():
                if value == worst_course_score:
                    return ID, value
        else:
            return 'Not Available', 'Not Available'

    def display_score_table(self):
        course_list_display = []
        student_list_display = []
        line_list = []
        score_display = [[0 for i in range(len(self.course_list))] for j in range(len(self.student_list))]
        score_display = [[self.score_list[i][j] + score_display[i][j] for j in range(len(self.score_list[0]))] for i in
                         range(len(self.score_list))]
        for i in range(len(score_display)):
            for j in range(len(score_display[i])):
                if score_display[i][j] == -1:
                    score_display[i][j] = " "
                elif score_display[i][j] == 888:
                    score_display[i][j] = "--"
                else:
                    score_display[i][j] = str(score_display[i][j])
        for course in self.course_list:
            course_list_display.append(course.ID)
            line_list.append("-----")
        for student in self.student_list:
            student_list_display.append(student.ID)
        highest_average_score, highest_average_score_index = self.top_student()
        s = '{:7}|' + '  {:6}|' * (len(course_list_display) - 1) + '  {:6}'
        s2 = '{:7}|' + '  {:6}|' * (len(course_list_display) - 1) + '  {:6}'
        s3 = '{:7}|' + ' {:6} |' * (len(course_list_display) - 1) + '  {:6}'
        print(s.format(" ", *course_list_display))
        print(s3.format("-----", *line_list))
        for i in range(len(student_list_display)):
            print(s2.format(student_list_display[i], *score_display[i]))
        print(s3.format("-----", *line_list))
        print(str(len(student_list_display)) + " students, " + str(len(course_list_display)) + " courses, the top "
                                                                                               "student is " + str(
            student_list_display[highest_average_score_index]) + ", average " + str(highest_average_score))

    def display_course_report(self):
        worst_course, worst_course_score = self.worst_course()
        s = '{:10}' + '{:2}' + '{:15}' + '{:7}' + '{:7}' + '{:7}'
        s1 = '{:10}' + '{:2}' + '{:15}' + '{:5}' + '{:5}' + '{:7}'
        print(s.format("CID", " ", "Name", "Pt. ", "Enl. ", "Avg. "))
        print("-----------------------------------------------")
        for course in self.course_list:
            if course.course_type[0] == 'C':
                print(s1.format(course.ID, '*', course.title, course.credit_point, course.number_of_student_enrol(),
                                course.course_average_score()))
            if course.course_type[0] == 'E':
                print(s1.format(course.ID, '~', course.title, course.credit_point, course.number_of_student_enrol(),
                                course.course_average_score()))
        print("-----------------------------------------------")
        print('The worse performing course is', worst_course, 'with an average', worst_course_score)
        self.save_course()
        print('courses_report.txt generated!')

    def display_student_report(self):
        s = '{:10}' + '{:15}' + '{:10}' + '{:2}' + '     ' + '{:10}'
        s1 = '{:10}' + '{:15}' + '{:10}' + '{:2}' + ' ' + '{:10.2f}'
        s2 = '{:10}' + '{:15}' + '{:10}' + '{:2}' + '!' + '{:10.2f}'
        s3 = '{:10}' + '{:15}' + '{:10}' + '{:2}' + ' ' + '{:10}'
        s4 = '{:10}' + '{:15}' + '{:10}' + '{:2}' + '!' + '{:10}'
        print(s.format("SID", "Name", "Mode", "CrPt", "GPA"))
        print("----------------------------------------------------")
        self.student_list = sorted(self.student_list, key=lambda student: student.GPA, reverse=True)
        for student in self.student_list:
            enrolment_status = student.get_enrolment_status()
            if enrolment_status == 'Good' and student.GPA != '       --':
                print(s1.format(student.ID, student.name, student.student_type, student.total_credit_point_earn,
                                student.GPA))
            elif enrolment_status == 'Good' and student.GPA == '       --':
                print(s3.format(student.ID, student.name, student.student_type, student.total_credit_point_earn,
                                student.GPA))
            elif enrolment_status == 'Bad' and student.GPA != '       --':
                print(s2.format(student.ID, student.name, student.student_type, student.total_credit_point_earn,
                                student.GPA))
            elif enrolment_status == 'Bad' and student.GPA == '       --':
                print(s4.format(student.ID, student.name, student.student_type, student.total_credit_point_earn,
                                student.GPA))
        self.save_student()
        print('student_report.txt generated!')

    def save_student(self):
        """Method save_student() is used to save the student report to a text file.
        Everytime the method is called new report will be prepend on top of the old report in the same text file
        Try - except is used in the case the text file is not available then a new file is created"""
        s = '{:10}' + '{:15}' + '{:10}' + '{:2}' + '     ' + '{:10}' + "\n"
        s1 = '{:10}' + '{:15}' + '{:10}' + '{:2}' + ' ' + '{:10.2f}' + "\n"
        s2 = '{:10}' + '{:15}' + '{:10}' + '{:2}' + '!' + '{:10.2f}' + "\n"
        s3 = '{:10}' + '{:15}' + '{:10}' + '{:2}' + ' ' + '{:10}' + "\n"
        s4 = '{:10}' + '{:15}' + '{:10}' + '{:2}' + '!' + '{:10}' + "\n"
        try:
            file = open('student_report.txt', "r")
            temp = file.read()
            file.close()
            output_file = open('student_report.txt', "w")
            now = datetime.now()
            date_time_of_file_generate = now.strftime("%d/%m/%Y %H:%M")
            output_file.write(date_time_of_file_generate + '\n')
            output_file.write(s.format("SID", "Name", "Mode", "CrPt", "GPA"))
            output_file.write("---------------------------------------------------\n")
            for student in self.student_list:
                enrolment_status = student.get_enrolment_status()
                if enrolment_status == 'Good' and student.GPA != '       --':
                    output_file.write(s1.format(student.ID, student.name, student.student_type,
                                                student.total_credit_point_earn, student.GPA))
                elif enrolment_status == 'Good' and student.GPA == '       --':
                    output_file.write(s3.format(student.ID, student.name, student.student_type,
                                                student.total_credit_point_earn, student.GPA))
                elif enrolment_status == 'Bad' and student.GPA != '       --':
                    output_file.write(s2.format(student.ID, student.name, student.student_type,
                                                student.total_credit_point_earn, student.GPA))
                elif enrolment_status == 'Bad' and student.GPA == '       --':
                    output_file.write(s4.format(student.ID, student.name, student.student_type,
                                                student.total_credit_point_earn, student.GPA))
            output_file.write(temp + '\n')
            output_file.close()
        except OSError:
            output_file = open('student_report.txt', "w")
            now = datetime.now()
            date_time_of_file_generate = now.strftime("%d/%m/%Y %H:%M")
            output_file.write(date_time_of_file_generate + '\n')
            output_file.write(s.format("SID", "Name", "Mode", "CrPt", "GPA"))
            output_file.write("---------------------------------------------------\n")
            for student in self.student_list:
                enrolment_status = student.get_enrolment_status()
                if enrolment_status == 'Good' and student.GPA != '       --':
                    output_file.write(s1.format(student.ID, student.name, student.student_type,
                                                student.total_credit_point_earn, student.GPA))
                elif enrolment_status == 'Good' and student.GPA == '       --':
                    output_file.write(s3.format(student.ID, student.name, student.student_type,
                                                student.total_credit_point_earn, student.GPA))
                elif enrolment_status == 'Bad' and student.GPA != '       --':
                    output_file.write(s2.format(student.ID, student.name, student.student_type,
                                                student.total_credit_point_earn, student.GPA))
                elif enrolment_status == 'Bad' and student.GPA == '       --':
                    output_file.write(s4.format(student.ID, student.name, student.student_type,
                                                student.total_credit_point_earn, student.GPA))
            output_file.close()

    def save_course(self):
        """Method save_course() is used to save the course report to a text file.
        Everytime the method is called new report will be prepend on top of the old report in the same text file
        Try - except is used in the case the text file is not available then a new file is created"""
        worst_course, worst_course_score = self.worst_course()
        s = '{:10}' + '{:2}' + '{:15}' + '{:7}' + '{:7}' + '{:7}' + "\n"
        s1 = '{:10}' + '{:2}' + '{:15}' + '{:5}' + '{:5}' + '{:7}' + "\n"
        try:
            file = open('courses_report.txt', "r")
            temp = file.read()
            file.close()
            output_file = open('courses_report.txt', "w")
            now = datetime.now()
            date_time_of_file_generate = now.strftime("%d/%m/%Y %H:%M")
            output_file.write(date_time_of_file_generate + '\n')
            output_file.write(s.format("CID", " ", "Name", "Pt. ", "Enl. ", "Avg."))
            output_file.write("-----------------------------------------------\n")
            for course in self.course_list:
                if course.course_type[0] == 'C':
                    output_file.write(s1.format(course.ID, '*', course.title, course.credit_point,
                                                course.number_of_student_enrol(),
                                                course.course_average_score()))
                if course.course_type[0] == 'E':
                    output_file.write(
                        s1.format(course.ID, '~', course.title, course.credit_point, course.number_of_student_enrol(),
                                  course.course_average_score()))
            output_file.write("-----------------------------------------------\n")
            output_file.write(
                'The worse performing course is {} with an average {} \n'.format(worst_course, worst_course_score))
            output_file.write(temp + '\n')
            output_file.close()
        except OSError:
            output_file = open('courses_report.txt', "w")
            now = datetime.now()
            date_time_of_file_generate = now.strftime("%d/%m/%Y %H:%M")
            output_file.write(date_time_of_file_generate + '\n')
            output_file.write(s.format("CID", " ", "Name", "Pt. ", "Enl. ", "Avg."))
            output_file.write("-----------------------------------------------\n")
            for course in self.course_list:
                if course.course_type[0] == 'C':
                    output_file.write(s1.format(course.ID, '*', course.title, course.credit_point,
                                                course.number_of_student_enrol(),
                                                course.course_average_score()))
                if course.course_type[0] == 'E':
                    output_file.write(
                        s1.format(course.ID, '~', course.title, course.credit_point, course.number_of_student_enrol(),
                                  course.course_average_score()))
            output_file.write("-----------------------------------------------\n")
            output_file.write(
                'The worse performing course is {} with an average {} \n'.format(worst_course, worst_course_score))
            output_file.close()


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("ERROR: Please input text file as follow:  \n"
              "[Usage:] Python my_school.py <scores file> or \n"
              "         Python my_school.py <scores file> <courses file> or \n"
              "         Python my_school.py <scores file> <courses file> <students file>")
        sys.exit(0)
    elif 4 >= len(sys.argv) >= 2:
        school = School()
        if school.read_score_file(sys.argv[1]) is None and len(sys.argv) == 2:
            sys.exit()
        else:
            if len(sys.argv) == 2:
                school.display_score_table()
            elif len(sys.argv) > 2:
                school.read_course_file(sys.argv[2])
                if len(sys.argv) == 3:
                    school.display_course_report()
                elif len(sys.argv) == 4:
                    school.read_students_file(sys.argv[3])
                    school.display_student_report()
    else:
        print('This option is currently not available. Program will exit')
        sys.exit(0)
