package main;

import java.util.Scanner;

import services.StudentService;
import dao.StudentDAO;
import model.Student;

public class MainApp {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        StudentService service = new StudentService();
        StudentDAO dao = new StudentDAO();

        while (true) {
            System.out.println("\n1. Add\n2. Update\n3. Delete\n4. View\n5. Sync with DB\n6. Exit");
            int choice = sc.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter ID Name Age: ");
                    service.addStudent(new Student(
                        sc.nextInt(), sc.next(), sc.nextInt()
                    ));
                    break;

                case 2:
                    System.out.print("Enter ID to update: ");
                    int uid = sc.nextInt();
                    System.out.print("Enter new Name & Age: ");
                    service.updateStudent(uid, sc.next(), sc.nextInt());
                    break;

                case 3:
                    System.out.print("Enter ID to delete: ");
                    service.deleteStudent(sc.nextInt());
                    break;

                case 4:
                    service.viewStudents();
                    break;

                case 5:
                    dao.syncToDatabase(service.getAllStudents());
                    break;

                case 6:
                    System.exit(0);
            }
        }
    }
}