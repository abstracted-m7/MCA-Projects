package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.util.List;

import model.Student;
import util.DBConnection;

public class StudentDAO {

    public void syncToDatabase(List<Student> students) {
        try {
            Connection con = DBConnection.getConnection();

            // Clear table (Full Sync)
            PreparedStatement delete = con.prepareStatement("DELETE FROM student");
            delete.executeUpdate();

            // Insert all records
            for (Student s : students) {
                PreparedStatement ps = con.prepareStatement(
                    "INSERT INTO student VALUES (?, ?, ?)"
                );
                ps.setInt(1, s.getId());
                ps.setString(2, s.getName());
                ps.setInt(3, s.getAge());
                ps.executeUpdate();
            }

            System.out.println("Data Synced Successfully!");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}