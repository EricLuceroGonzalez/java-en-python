package matrixmath;

// Para que la clase Main actúe como un GatewayServer:
import py4j.GatewayServer;

public class Main {
    public static void main(String[] args) {
        System.out.println("Servidor Py4J iniciando...");

        Main app = new Main();
        // Levantamos el servidor en el puerto por defecto (25333)
        GatewayServer server = new GatewayServer(app);
        server.start();

        System.out.println("Servidor Py4J listo para recibir conexiones de Python.");
    }

    // Método para que Python obtenga una instancia del servicio
    public MatrixDet getDetService() {
        return new MatrixDet();
    }

    public Matrix createMatrix(double[][] data) {
        return new Matrix(data);
    }
}

// double[][] data = { { 1, 2, 3 }, { 0, 1, 4 }, { 5, 6, 0 } };
// Matrix m = new Matrix(data);
// MatrixDet service = new MatrixDet();

// System.out.println("Matriz Original:");
// m.print();

// double det = service.calculateDeterminant(m);
// System.out.println("\nDeterminante: " + det);

// if (service.isInvertible(m)) {
// System.out.println("Matriz es invertible.\nInversa:");
// service.calculateInverse(m).print();
// } else {
// System.out.println("No es invertible.");
// }
// }
// }