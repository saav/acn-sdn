import java.util.*;

// Created by Joshua Lee
// Usage:
// javac PingToCSV.java
// cat ping.txt | java PingToCSV > ping.csv
// 
// Input is meant to be something like this:
// 64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=21.1 ms
// 
// Output:
// Ping Counter, Ping Time (ms)
// 1, 21.1

class PingToCSV {
    public static void main(String[] args) {
        System.out.println("Ping Counter, Ping Time (ms)");
        Scanner sc = new Scanner(System.in);
        while(sc.hasNextLine()) {
            String input = sc.nextLine();
            if (input.isEmpty()) {
                System.exit(0);
            }
            String[] inputs = input.split(" ");
            System.out.println(inputs[4].substring(9, inputs[4].length()) + ", " + inputs[6].substring(5, inputs[6].length()));
        }
    }
}