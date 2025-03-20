#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

// cos(2x) [-2, 2]

double f_x(double x)
{
	return cos(2 * x);
}

double fDerivative2(double x)
{
	return -cos(2 * x);
}

void passingMethod(vector<double>& a, vector<double>& b, vector<double>& c, vector<double>& f, vector<double>& y, vector<double>& alf, vector<double>& bet)
{
	alf[0] = b[0] / c[0];
	bet[0] = f[0] / c[0];
	int n = c.size(); // Длина нашего вектора диагонали
	double delt = 0;
	//cout << alf[0] << " " << bet[0] << "\n";
	for (int i = 1; i < n - 1; i++)
	{
		delt = c[i] - a[i - 1] * alf[i - 1];
		alf[i] = b[i] / delt;
		bet[i] = (f[i] + a[i - 1] * bet[i - 1]) / delt;
		//cout << delt << " " << alf[i] << " " << bet[i] << "\n";
	}
	n--; // Уменьшаем на 1 чтобы n стало индексом последнего эл-та
	delt = c[n] - a[n - 1] * alf[n - 1];
	bet[n] = (f[n] + a[n - 1] * bet[n - 1]) / delt;
	//cout << delt  << " " << bet[n] << "\n";

	y[n] = bet[n];
	for (int i = n - 1; i >= 0; i--)
	{
		y[i] = alf[i] * y[i + 1] + bet[i];
	}
}

void createSplain(vector<vector<double>>& nodes, vector<double>& M, int n, double h, double start, double end)
{
	vector<double> a(n - 1, 0);
	vector<double> c(n, 0);
	vector<double> b(n - 1, 0);
	vector<double> f(n, 0);
	
	vector<double> alf(n - 1, 0);
	vector<double> bet(n, 0);

	c[0] = 1;
	c[n - 1] = 1;
	f[0] = fDerivative2(start);
	f[n - 1] = fDerivative2(end);
	for (int i = 1; i < n - 1; i++)
	{
		a[i - 1] = -(h / 6);
		c[i] = -((2 * h) / 3);
		b[i] = -(h / 6);
		f[i] = ((nodes[1][i + 1] - nodes[1][i]) / h) + ((nodes[1][i] - nodes[1][i - 1]) / h);
	}

	passingMethod(a, b, c, f, M, alf, bet);
}

double spline(vector<double>& M, double h, vector<vector<double>>& nodes, double x) {
	if (x <= nodes[0][0]) return nodes[1][0];
	if (x >= nodes[0].back()) return nodes[1].back();

	int left = 0;
	int right = nodes[0].size() - 2;
	int i;

	while (left <= right) {
		i = (left + right) / 2;
		if (x < nodes[0][i]) {
			right = i - 1;
		}
		else if (x > nodes[0][i + 1]) {
			left = i + 1;
		}
		else {
			break;
		}
	}

	double dx1 = nodes[0][i + 1] - x;
	double dx2 = x - nodes[0][i];

	return (M[i] * dx1 * dx1 * dx1 + M[i + 1] * dx2 * dx2 * dx2) / (6.0 * h) +
		(nodes[1][i] * dx1 + nodes[1][i + 1] * dx2) / h -
		(M[i] * dx1 + M[i + 1] * dx2) * h / 6.0;
}

int main()
{
	int n = 15;
	double a = -2;
	double b = 2;
	double h = (b - a) / n;
	vector<vector<double>> nodes(2, vector<double>(n, 0)); // 0 -- x 1 -- f(x)
	for (int i = 0; i < n; i++)
	{
		nodes[0][i] = a + i * h;
		nodes[1][i] = f_x(nodes[0][i]);
	}

	vector<double> M(n, 0);
	createSplain(nodes, M, n, h, a, b);

	vector<vector<double>> nodes_test(2, vector<double>(100, 0)); // 0 -- x 1 -- f(x)
	ofstream fout("S1_1.txt");
	for (int i = 0; i < 100; i++)
	{
		nodes_test[0][i] = a + (i * (b - a)) / 100;
		nodes_test[1][i] = spline(M, h, nodes, nodes_test[0][i]);
		fout << nodes_test[0][i] << " " << nodes_test[1][i] << "\n";
	}

	return 0;
}