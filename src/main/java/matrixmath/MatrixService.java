package matrixmath;

public class MatrixService {

    public double calculateDeterminant(Matrix m) {
        double[][] d = m.getData();
        if (m.getSize() == 2) {
            return d[0][0] * d[1][1] - d[0][1] * d[1][0];
        } else if (m.getSize() == 3) {
            return d[0][0] * (d[1][1] * d[2][2] - d[1][2] * d[2][1]) -
                    d[0][1] * (d[1][0] * d[2][2] - d[1][2] * d[2][0]) +
                    d[0][2] * (d[1][0] * d[2][1] - d[1][1] * d[2][0]);
        }
        return 0;
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
}