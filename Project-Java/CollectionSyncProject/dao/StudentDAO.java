package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.util.List;

import model.Student;
import util.DBConnection;

public class StudentDAO {

    public void syncToDatabase(List<Student> students) {

        String deleteQuery = "DELETE FROM student";
        String insertQuery = "INSERT INTO student VALUES (?, ?, ?)";

        try (
            Connection con = DBConnection.getConnection();
            PreparedStatement deleteStmt = con.prepareStatement(deleteQuery);
            PreparedStatement insertStmt = con.prepareStatement(insertQuery);
        ) {

            // Step 1: Clear old data
            deleteStmt.executeUpdate();

            // Step 2: Insert new data
            for (Student s : students) {
                insertStmt.setInt(1, s.getId());
                insertStmt.setString(2, s.getName());
                insertStmt.setInt(3, s.getAge());
                insertStmt.executeUpdate();
            }

            System.out.println("✅ Data Synced Successfully!");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}