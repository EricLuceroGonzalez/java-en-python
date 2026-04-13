package math;

public class Main {
    public static void main(String[] args) {
        double[][] data = { { 1, 2, 3 }, { 0, 1, 4 }, { 5, 6, 0 } };
        Matrix m = new Matrix(data);
        MatrixService service = new MatrixService();

        System.out.println("Matriz Original:");
        m.print();

        double det = service.calculateDeterminant(m);
        System.out.println("\nDeterminante: " + det);

        if (service.isInvertible(m)) {
            System.out.println("Es invertible. Inversa:");
            service.calculateInverse(m).print();
        } else {
            System.out.println("No es invertible.");
        }
    }
}