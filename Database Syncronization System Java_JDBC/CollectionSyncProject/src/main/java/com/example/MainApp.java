package com.example;

import com.example.model.*;
import com.example.services.*;

import java.util.Scanner;

public class MainApp {

    public static void main(String[] args){

        Scanner sc = new Scanner(System.in);
        StudentService service = new StudentService();

        while(true){

            System.out.println("\n1 Add Student");
            System.out.println("2 View Students");
            System.out.println("3 Update Student");
            System.out.println("4 Delete Student");
            System.out.println("5 Sync To Database");
            System.out.println("6 Exit");

            int choice = sc.nextInt();

            switch(choice){

                case 1:

                    System.out.println("Enter Student ID:");
                    int id = sc.nextInt();
                    sc.nextLine();

                    System.out.println("Enter Student Name:");
                    String studentName = sc.nextLine();

                    System.out.println("Enter Department:");
                    String studentDept = sc.nextLine();

                    service.addStudent(new Student(id, studentName, studentDept));

                    System.out.println("Student added successfully");
                    break;

                case 2:

                    service.viewStudents();
                    break;

                case 3:

                    System.out.println("Enter Student ID to update:");
                    int uid = sc.nextInt();
                    sc.nextLine();

                    System.out.println("What do you want to update?");
                    System.out.println("1 Update Name");
                    System.out.println("2 Update Department");
                    System.out.println("3 Update Name and Department");

                    int ch = sc.nextInt();
                    sc.nextLine();

                    if (ch == 1) {

                        System.out.println("Enter new name:");
                        String newName = sc.nextLine();

                        service.updateStudent(uid, ch, newName, null);

                    } 
                    else if (ch == 2) {

                        System.out.println("Enter new department:");
                        String newDept = sc.nextLine();

                        service.updateStudent(uid, ch, newDept, null);

                    } 
                    else if (ch == 3) {

                        System.out.println("Enter new name:");
                        String newName = sc.nextLine();

                        System.out.println("Enter new department:");
                        String newDept = sc.nextLine();

                        service.updateStudent(uid, ch, newName, newDept);
                    }
                    else {
                        System.out.println("Invalid choice");
                    }

                    break;

                case 4:

                    System.out.println("Enter student ID to delete:");
                    int did = sc.nextInt();

                    service.deleteStudent(did);
                    break;

                case 5:

                    service.syncToDatabase();
                    break;

                case 6:

                    System.out.println("Program exited.");
                    sc.close();
                    System.exit(0);

                default:

                    System.out.println("Invalid choice. Try again.");
            }
        }
    }
}