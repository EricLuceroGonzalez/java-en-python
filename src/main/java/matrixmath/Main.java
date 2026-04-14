package matrixmath;

import py4j.GatewayServer;

public class Main {
    // Estas instancias se reutilizan para no crear objetos basura en memoria
    private final MatrixDet service = new MatrixDet();

    public MatrixDet getService() {
        return service;
    }

    public Matrix createMatrix(double[][] data) {
        return new Matrix(data);
    }

    public static void main(String[] args) {
        // Este main solo se usa para Py4J
        Main app = new Main();
        GatewayServer server = new GatewayServer(app);
        server.start();
        System.out.println(">>> Servidor Py4J listo (Puerto 25333) <<<");
    }
}