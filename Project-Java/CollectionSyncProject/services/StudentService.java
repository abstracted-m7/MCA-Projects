package services;

import model.Student;
import java.util.ArrayList;
import java.util.List;

public class StudentService {

    private List<Student> students = new ArrayList<>();

    public void addStudent(Student s) {
        students.add(s);
    }

    public void updateStudent(int id, String name, int age) {
        for (Student s : students) {
            if (s.getId() == id) {
                s.setName(name);
                s.setAge(age);
            }
        }
    }

    public void deleteStudent(int id) {
        students.removeIf(s -> s.getId() == id);
    }

    public void viewStudents() {
        for (Student s : students) {
            System.out.println(s.getId() + " " + s.getName() + " " + s.getAge());
        }
    }

    public List<Student> getAllStudents() {
        return students;
    }
}