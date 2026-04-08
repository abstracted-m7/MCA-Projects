package com.example.services;

import java.util.ArrayList;

import com.example.model.Student;
import com.example.util.DBConnection;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class StudentService {

    private ArrayList<Student> students=new ArrayList<>(); //vector

    public void addStudent(Student s){
        students.add(s);
    }

    // View student data
    //only interact with arraylist
    // for(Student s:students){
    //         System.out.println(s);
    // }
    //direct view from database
    public void viewStudents() {
        try {

            Connection con = DBConnection.getConnection();

            String sql = "SELECT * FROM students";

            PreparedStatement ps = con.prepareStatement(sql);

            ResultSet rs = ps.executeQuery();

            System.out.println("\nStudents List:");

            while (rs.next()) {

                int id = rs.getInt("id");
                String name = rs.getString("name");
                String dept = rs.getString("department");

                System.out.println(id + " " + name + " " + dept);
            }

            con.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    //Update Student data
    //only in arraylist
    // for(Student s:students){

    //     if(s.getId()==id){
    //         s.setName(name);
    //         s.setDepartment(dept);
    //     }
    // }
    //interect direct database
    public void updateStudent(int id, int choice, String value1, String value2) {
        try {

            Connection con = DBConnection.getConnection();

            String sql = "";

            PreparedStatement ps;

            if (choice == 1) {

                sql = "UPDATE students SET name=? WHERE id=?";
                ps = con.prepareStatement(sql);

                ps.setString(1, value1);
                ps.setInt(2, id);

            } 
            else if (choice == 2) {

                sql = "UPDATE students SET department=? WHERE id=?";
                ps = con.prepareStatement(sql);

                ps.setString(1, value1);
                ps.setInt(2, id);

            } 
            else {

                sql = "UPDATE students SET name=?, department=? WHERE id=?";
                ps = con.prepareStatement(sql);

                ps.setString(1, value1);
                ps.setString(2, value2);
                ps.setInt(3, id);
            }

            int rows = ps.executeUpdate();

            if (rows > 0)
                System.out.println("Student updated successfully");
            else
                System.out.println("Student not found");

            con.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    //delete student data

    //from only arraylist
    // public void deleteStudent(int id){
    //     students.removeIf(s->s.getId()==id);
    // }
    //from direct database
    public void deleteStudent(int id) {
        try {

            Connection con = DBConnection.getConnection();

            String sql = "DELETE FROM students WHERE id=?";

            PreparedStatement ps = con.prepareStatement(sql);

            ps.setInt(1, id);

            int rows = ps.executeUpdate();

            if (rows > 0)
                System.out.println("Student deleted successfully");
            else
                System.out.println("Student not found");

            con.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    //sync to database
    public void syncToDatabase(){

        try{

            Connection con=DBConnection.getConnection();

            String sql = "INSERT INTO students (id,name,department) VALUES (?,?,?) "
                   + "ON DUPLICATE KEY UPDATE name=VALUES(name), department=VALUES(department)";

            PreparedStatement ps=con.prepareStatement(sql);

            for(Student s:students){

                ps.setInt(1,s.getId());
                ps.setString(2,s.getName());
                ps.setString(3,s.getDepartment());

                ps.executeUpdate();
            }

            System.out.println("Data synced to database");

            students.clear();

            con.close();

        }catch(Exception e){
            e.printStackTrace();
        }
    }
}