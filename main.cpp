#include <iostream>
#include <vector>

using namespace std;

// cos(2x) [-2, 2]

double f(double x)
{
	return cos(2 * x);
}

double fDerivative2(double x)
{
	return -cos(2 * x);
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
		nodes[1][i] = f(nodes[0][i]);
	}


	return 0;
}