# computer_vision_learning
## Numerical Data Augmentation
1. **Uniform Random Generation** : This really naive method consists of creating a new instance based on the min and max of the existing ones, the value of each feature is generated randomly with a uniform probability. (The mins and maxs are calculated from the values of the concerned feature of the concerned class each time)
2. **Normal Random Generation** : Same as Uniform but the probability is now a gaussian curve. Which is of course less naive since generated value fit the initial data distribution.
3. **Adding Noise** : This method is a little bit different since it consists of cloning initial values, but each time adding some noise to it. This methods aims to strengthen the models and prevent overfitting.
