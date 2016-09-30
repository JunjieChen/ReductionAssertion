In this package, there are two folders: code and results

In the folder 'code', there are our implementations of reduction techniques and prioritization techniques, and the scripts used in our empirical study.

In the folder 'results', there are complete results of our study. More specifically, there are two subfolders in this folder: correlation and comparison.

	correlation: 
		the complete results of our empirical study investigating the influence of assertions on coverage-based test suite reduction.

		dataCovRF refers to the results of the influence of the assertion coverage reduction on fault-detection capability loss

		dataCovRS refers to the results of the influence of the assertion coverage reduction on test suite size reduction

		dataNumRF refers to the results of the influence of the assertion count reduction on fault-detection capability loss

		dataNumRS refers to the results of the influence of the assertion count reduction on test suite size reduction

	comparison:
		the complete results of our study investigating whether our combination works

		comparison1: the results of comparison with the traditional coverage-based test suite reduction techniques
		comparison2: the results of comparison with the reduction techniques based on assertion coverage alone
		comparison3: the results of comparison with the reduction techniques based on the combination of different code coverage