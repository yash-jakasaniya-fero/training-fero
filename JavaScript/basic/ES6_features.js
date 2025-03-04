//Arrow functions
const materials = ["Hydrogen", "Helium", "Lithium", "Beryllium"];
console.log(materials.map((material) => material.length));
  
//Destructuring
let a, b, rest;
[a, b] = [10, 20];
[a, b, ...rest] = [10, 20, 30, 40, 50];
console.log(rest);

//Spread vs Rest operator
function abc1(a, ...rest) {
    return rest;
    }
    console.log(abc1(10, 1, 2, 3, 4, 5)); 

function abc2(a, b, c, d, e, f, g, h, i, j) {
    return a + b + c + d + e + f + g + h + i + j;
    }
    console.log(abc2(...[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])); 
