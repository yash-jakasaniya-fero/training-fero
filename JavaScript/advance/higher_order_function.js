function multiplyBy(num) {
    return function (x) {
      return x * num;
    };
  }
  
  const double = multiplyBy(2);
  console.log(double(10));
  