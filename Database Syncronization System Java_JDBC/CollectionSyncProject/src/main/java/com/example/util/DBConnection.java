package com.example.util;

import java.sql.Connection;
import java.sql.DriverManager;

public class DBConnection {

    private static final String URL="jdbc:mysql://localhost:3306/collectiondb";
    private static final String USER="root";
    private static final String PASSWORD="";

    public static Connection getConnection() throws Exception{

        Connection con=DriverManager.getConnection(URL,USER,PASSWORD);

        return con;
    }
}