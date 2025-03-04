//For Each
const arr1 = [100, 200, 300];
arr1.forEach((item, index) => {
  console.log(index, item);
});

//For map
const arr2 = [1, 2, 3];
const doubled = arr2.map(item => item * 2);
console.log(doubled);

//For Filters
const arr3 = [1, 2, 3, 4, 5];
const evenNumbers = arr3.filter(item => item % 2 === 0);
console.log(evenNumbers);

//For Some
const arr4 = [1, 2, 3];
const hasEven = arr4.some(item => item % 2 === 0);
console.log(hasEven);

//For every
const arr5 = [2, 4, 6];
const allEven = arr5.every(item => item % 2 === 0);
console.log(allEven);

//For find
const arr6 = [1, 2, 3, 4];
const found = arr6.find(item => item > 2);
console.log(found);

//For findIndex
const arr7 = [1, 2, 3, 4];
const index = arr7.findIndex(item => item > 2);
console.log(index);

//For split
const str = "apple,banana,orange";
const arr8 = str.split(",");
console.log(arr8);

//For includes
const arr9 = [1, 2, 3];
const containsTwo = arr9.includes(20);
console.log(containsTwo);