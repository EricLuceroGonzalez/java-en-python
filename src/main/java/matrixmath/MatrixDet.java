package matrixmath;

public class MatrixDet {

    public double calculateDeterminant(Matrix m) {
        double[][] matrix = m.getData();
        int n = m.getSize();
        if (n == 2) {
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
        } else if (n == 3) {
            return matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
                    matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
                    matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]);
        }
        double det = 0;
        for (int i = 0; i < n; i++) {
            // Creamos la submatriz (menor) eliminando fila 0 y columna i
            Matrix submatriz = crearSubmatriz(matrix, 0, i);
            det += Math.pow(-1, i) * matrix[0][i] * calculateDeterminant(submatriz);
        }
        return det;
    }

    public boolean isInvertible(Matrix m) {
        return calculateDeterminant(m) != 0;
    }

    public Matrix calculateInverse(Matrix m) {
        double det = calculateDeterminant(m);
        if (det == 0)
            return null;

        double[][] d = m.getData();
        double[][] inv = new double[m.getSize()][m.getSize()];

        if (m.getSize() == 2) {
            inv[0][0] = d[1][1] / det;
            inv[0][1] = -d[0][1] / det;
            inv[1][0] = -d[1][0] / det;
            inv[1][1] = d[0][0] / det;
        } else {
            // Simplificado para el ejemplo: Adjunta traspuesta / determinante
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    inv[j][i] = ((d[(i + 1) % 3][(j + 1) % 3] * d[(i + 2) % 3][(j + 2) % 3]) -
                            (d[(i + 1) % 3][(j + 2) % 3] * d[(i + 2) % 3][(j + 1) % 3])) / det;
                }
            }
        }
        return new Matrix(inv);
    }

    public Matrix crearSubmatriz(double[][] matrizOriginal, int filaEliminar, int colEliminar) {
        int n = matrizOriginal.length;
        double[][] datosSub = new double[n - 1][n - 1];
        int filaDestino = 0;

        for (int i = 0; i < n; i++) {
            if (i == filaEliminar)
                continue; // Saltamos la fila tachada
            int colDestino = 0;
            for (int j = 0; j < n; j++) {
                if (j == colEliminar)
                    continue; // Saltamos la columna tachada
                datosSub[filaDestino][colDestino] = matrizOriginal[i][j];
                colDestino++;
            }
            filaDestino++;
        }
        // Usamos tu constructor de Matrix definido en Main.java
        return new Matrix(datosSub);
    }
}