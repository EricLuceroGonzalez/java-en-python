package matrixmath;

public class Matrix {
    private double[][] data;
    private int size;

    public Matrix(double[][] data) {
        this.data = data;
        this.size = data.length;
    }

    public double[][] getData() {
        return data;
    }

    public int getSize() {
        return size;
    }

    public void print() {
        for (double[] row : data) {
            for (double val : row) {
                System.out.printf("%8.2f ", val);
            }
            System.out.println();
        }
    }
}